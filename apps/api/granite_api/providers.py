"""Network LLM providers (infrastructure layer): Ollama and any OpenAI-compatible endpoint.

Both implement :class:`granite_core.llm.LLMProvider`. Failures become :class:`ProviderUnavailable`, which the
runner records as an errored run with an actionable message instead of a stack trace (FR-RUN-04, NFR-04).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from granite_core.llm import Completion, LLMRequest, ProviderUnavailable


def check_endpoint(url: str) -> str:
    """Endpoints come from operator configuration; still refuse anything but http(s), so no file: or custom schemes."""
    if urllib.parse.urlparse(url).scheme not in {"http", "https"}:
        raise ProviderUnavailable("the model endpoint URL must start with http:// or https://")
    return url


def _post(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float) -> dict[str, Any]:
    check_endpoint(url)
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", **headers}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310  # nosec B310
            data: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:200]
        raise ProviderUnavailable(f"model endpoint returned HTTP {e.code}: {detail}") from None
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        raise ProviderUnavailable(f"model endpoint unreachable or too slow ({type(e).__name__}): {e}") from None
    except json.JSONDecodeError:
        raise ProviderUnavailable("model endpoint returned something that is not JSON") from None


@dataclass
class OllamaProvider:
    base_url: str = "http://127.0.0.1:11434"
    timeout: float = 120.0
    name: str = "ollama"

    def complete(self, request: LLMRequest) -> Completion:
        options: dict[str, Any] = {"temperature": request.temperature, "num_predict": request.max_tokens}
        if request.seed is not None:
            options["seed"] = request.seed
        payload: dict[str, Any] = {"model": request.model, "messages": request.messages, "stream": False,
                                   "options": options}
        if request.json_mode:
            payload["format"] = "json"
        t0 = time.monotonic()
        data = _post(f"{self.base_url.rstrip('/')}/api/chat", payload, {}, self.timeout)
        text = (data.get("message") or {}).get("content")
        if not isinstance(text, str):
            raise ProviderUnavailable("model endpoint returned no message")
        return Completion(
            text=text, model=request.model, provider=self.name, tokens_in=int(data.get("prompt_eval_count", 0)),
            tokens_out=int(data.get("eval_count", 0)), latency_ms=int((time.monotonic() - t0) * 1000),
        )


@dataclass
class OpenAICompatProvider:
    """Any OpenAI-compatible chat endpoint (Groq, Gemini's compatibility endpoint, vLLM, ...)."""

    base_url: str
    api_key: str = ""
    timeout: float = 60.0
    name: str = "openai-compatible"

    def complete(self, request: LLMRequest) -> Completion:
        payload: dict[str, Any] = {
            "model": request.model, "messages": request.messages, "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if request.seed is not None:
            payload["seed"] = request.seed
        if request.json_mode:
            payload["response_format"] = {"type": "json_object"}
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        t0 = time.monotonic()
        data = _post(f"{self.base_url.rstrip('/')}/chat/completions", payload, headers, self.timeout)
        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise ProviderUnavailable("model endpoint returned an unexpected response shape") from None
        usage = data.get("usage") or {}
        return Completion(
            text=str(text), model=request.model, provider=self.name, tokens_in=int(usage.get("prompt_tokens", 0)),
            tokens_out=int(usage.get("completion_tokens", 0)), latency_ms=int((time.monotonic() - t0) * 1000),
        )
