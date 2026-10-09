"""LLM provider interface and the offline record/replay providers (master plan 21.2; FR-RUN-03/04).

The core never talks to a network. Real providers (Ollama, any OpenAI-compatible endpoint) are
implemented in the application layer against :class:`LLMProvider`. This module supplies:

* :class:`RecordedProvider`: answers from a *cassette* of responses that were really produced by a
  model earlier; a request that was never recorded raises :class:`RecordedMiss` (it never invents one);
* :class:`RecordingProvider`: wraps a live provider and writes every real response into a cassette.

A cassette entry is keyed by everything that determines the answer (model, parameters, seed,
messages), so changing a prompt or a seed correctly misses instead of silently reusing a stale answer.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol, runtime_checkable

from .evidence import sha256_of

Message = dict[str, str]


class ProviderUnavailable(Exception):
    """The model endpoint could not be reached, timed out or returned an error."""


class RecordedMiss(Exception):
    """Recorded mode was asked for a response that is not in the cassette."""


@dataclass
class LLMRequest:
    messages: list[Message]
    model: str
    temperature: float = 0.2
    max_tokens: int = 256
    seed: int | None = None
    json_mode: bool = False

    def params(self) -> dict[str, Any]:
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
            "json_mode": self.json_mode,
        }

    def key(self) -> str:
        return sha256_of({"model": self.model, "messages": self.messages, **self.params()})


@dataclass
class Completion:
    text: str
    model: str
    provider: str
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    recorded: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class LLMProvider(Protocol):
    name: str

    def complete(self, request: LLMRequest) -> Completion: ...


class Cassette:
    """A JSON file of recorded completions, safe to share between threads."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = os.fspath(path)
        self._lock = threading.Lock()
        self._entries: dict[str, dict[str, Any]] = {}
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as fh:
                self._entries = json.load(fh).get("entries", {})

    def get(self, key: str) -> dict[str, Any] | None:
        return self._entries.get(key)

    def put(self, key: str, completion: Completion, request: LLMRequest) -> None:
        with self._lock:
            self._entries[key] = {
                "completion": asdict(completion),
                "model": request.model,
                "params": request.params(),
                "last_user_message": request.messages[-1]["content"][:200] if request.messages else "",
            }
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(
                    {"format": "granite.cassette/v1", "entries": self._entries},
                    fh,
                    indent=1,
                    sort_keys=True,
                    ensure_ascii=False,
                )
            os.replace(tmp, self.path)

    def __len__(self) -> int:
        return len(self._entries)


class RecordedProvider:
    name = "recorded"

    def __init__(self, cassette: Cassette) -> None:
        self.cassette = cassette

    def complete(self, request: LLMRequest) -> Completion:
        entry = self.cassette.get(request.key())
        if entry is None:
            raise RecordedMiss(
                "this exact request was never recorded; run once in live mode with recording enabled "
                f"(model={request.model}, seed={request.seed})"
            )
        c = entry["completion"]
        return Completion(
            text=c["text"],
            model=c["model"],
            provider="recorded",
            tokens_in=c.get("tokens_in", 0),
            tokens_out=c.get("tokens_out", 0),
            latency_ms=c.get("latency_ms", 0),
            recorded=True,
            extra={"original_provider": c.get("provider")},
        )


class RecordingProvider:
    """Live provider that also records every response it returns.

    With ``reuse=False`` (default) every call goes to the live model, so a "live" run is really live and
    a re-run refreshes the cassette entry. ``reuse=True`` serves repeated requests from the cassette.
    """

    def __init__(self, live: LLMProvider, cassette: Cassette, reuse: bool = False) -> None:
        self.live, self.cassette, self.reuse = live, cassette, reuse
        self.name = f"{live.name}+recording"

    def complete(self, request: LLMRequest) -> Completion:
        key = request.key()
        if self.reuse and self.cassette.get(key) is not None:
            return RecordedProvider(self.cassette).complete(request)
        out = self.live.complete(request)
        self.cassette.put(key, out, request)
        return out
