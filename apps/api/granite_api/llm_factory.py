"""Choose how model answers are produced: live (Ollama or a hosted endpoint) or recorded (saved answers)."""

from __future__ import annotations

import urllib.request

from granite_core.llm import Cassette, LLMProvider, RecordedProvider, RecordingProvider

from .config import Settings
from .providers import OllamaProvider, OpenAICompatProvider, check_endpoint

HOSTED_TIMEOUT_S = 30.0  # FR-RUN-04 default
LOCAL_TIMEOUT_S = 120.0  # a CPU-only 3B model takes 5 to 35 s per call; 30 s would fail runs that are only slow


def live_available(settings: Settings) -> bool:
    if settings.openai_base_url:
        return True  # cannot probe a hosted endpoint without spending a request; failures surface per run
    try:
        url = check_endpoint(f"{settings.ollama_url.rstrip('/')}/api/tags")
        with urllib.request.urlopen(url, timeout=1.5):  # noqa: S310  # nosec B310
            return True
    except Exception:
        return False


def resolve_mode(settings: Settings, requested: str | None = None) -> str:
    """Return 'live' or 'recorded'. 'auto' prefers live when a model endpoint answers."""
    mode = requested or settings.llm_mode
    if mode == "auto":
        return "live" if live_available(settings) else "recorded"
    return mode


def build_provider(settings: Settings, mode: str) -> LLMProvider:
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
