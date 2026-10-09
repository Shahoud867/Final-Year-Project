"""Choose how model answers are produced: live (Ollama or a hosted endpoint) or recorded (saved answers)."""

from __future__ import annotations

import urllib.request

from granite_core.llm import Cassette, LLMProvider, RecordedProvider, RecordingProvider

from .config import Settings
from .providers import OllamaProvider, OpenAICompatProvider


def live_available(settings: Settings) -> bool:
    if settings.openai_base_url:
        return True  # cannot probe a hosted endpoint without spending a request; failures surface per run
    try:
        with urllib.request.urlopen(f"{settings.ollama_url.rstrip('/')}/api/tags", timeout=1.5):  # noqa: S310
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
        live = OpenAICompatProvider(settings.openai_base_url, settings.openai_api_key, timeout=settings.llm_timeout_s)
    else:
        live = OllamaProvider(settings.ollama_url, timeout=settings.llm_timeout_s)
    return RecordingProvider(live, Cassette(settings.cassette_path)) if settings.record_live else live
