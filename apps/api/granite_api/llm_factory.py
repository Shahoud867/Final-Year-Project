"""Choose how model answers are produced: live (Ollama or a hosted endpoint) or recorded (saved answers)."""

from __future__ import annotations

import time
import urllib.request

from granite_core.llm import Cassette, LLMProvider, RecordedProvider, RecordingProvider

from .config import Settings
from .providers import OllamaProvider, OpenAICompatProvider, check_endpoint

HOSTED_TIMEOUT_S = 30.0  # FR-RUN-04 default
LOCAL_TIMEOUT_S = 120.0  # a CPU-only 3B model takes 5 to 35 s per call; 30 s would fail runs that are only slow


PROBE_TIMEOUT_S = 0.6  # a local server answers in milliseconds; a closed port must not stall the caller
PROBE_TTL_S = 15.0  # the health endpoint is polled often, so remember the answer for a short time
_probe_cache: dict[str, tuple[float, bool]] = {}


def live_available(settings: Settings, max_age: float = PROBE_TTL_S) -> bool:
    """True if a live model endpoint answers (a hosted endpoint is assumed reachable).

    The answer is cached for ``max_age`` seconds per endpoint, so health checks stay fast when no model is running
    (on Windows a refused local connection can take about two seconds).
    """
    if settings.openai_base_url:
        return True  # cannot probe a hosted endpoint without spending a request; failures surface per run
    url = f"{settings.ollama_url.rstrip('/')}/api/tags"
    cached = _probe_cache.get(url)
    if cached and time.monotonic() - cached[0] < max_age:
        return cached[1]
    try:
        with urllib.request.urlopen(check_endpoint(url), timeout=PROBE_TIMEOUT_S):  # noqa: S310  # nosec B310
            reachable = True
    except Exception:
        reachable = False
    _probe_cache[url] = (time.monotonic(), reachable)
    return reachable


def resolve_mode(settings: Settings, requested: str | None = None) -> str:
    """Return 'live' or 'recorded'. 'auto' prefers live when a model endpoint answers."""
    mode = requested or settings.llm_mode
    if mode == "auto":
        return "live" if live_available(settings) else "recorded"
    return mode


def build_provider(settings: Settings, mode: str) -> LLMProvider:
    """Return the provider for a mode: recorded answers, or a live model (optionally recording)."""
    if mode == "recorded":
        return RecordedProvider(Cassette(settings.cassette_path))
    live: LLMProvider
    if settings.openai_base_url:
        live = OpenAICompatProvider(
            settings.openai_base_url, settings.openai_api_key, timeout=settings.llm_timeout_s or HOSTED_TIMEOUT_S
        )
    else:
        live = OllamaProvider(settings.ollama_url, timeout=settings.llm_timeout_s or LOCAL_TIMEOUT_S)
    return RecordingProvider(live, Cassette(settings.cassette_path)) if settings.record_live else live
