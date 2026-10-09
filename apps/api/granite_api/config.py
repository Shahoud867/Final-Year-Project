"""Runtime configuration, read once from environment variables (twelve-factor). No secrets have defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]  # apps/api
REPO_ROOT = APP_DIR.parents[1]


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    return default if raw is None else raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    db_url: str = f"sqlite:///{(APP_DIR / '.granite' / 'granite.db').as_posix()}"
    llm_mode: str = "auto"  # recorded: replay saved model answers | live: call the model | auto: live if reachable
    model: str = "llama3.2:3b"
    ollama_url: str = "http://127.0.0.1:11434"
    openai_base_url: str = ""  # set (with the key) to use a hosted OpenAI-compatible endpoint instead of Ollama
    openai_api_key: str = ""
    cassette_path: Path = REPO_ROOT / "data" / "cassettes" / "refund_desk_v1.json"
    record_live: bool = False  # in live mode also save every answer to the cassette
    api_token: str = ""  # when set, every /api request must send "Authorization: Bearer <token>"
    cors_origins: tuple[str, ...] = ("http://localhost:5173", "http://127.0.0.1:5173")
    rate_limit_per_minute: int = 120  # per client, mutating requests only; 0 disables
    jobs_inline: bool = False  # run jobs in the request thread (tests, tiny demos)
    max_workers: int = 2
    static_dir: Path | None = None
    llm_timeout_s: float | None = None  # per model call; default 30 s hosted, 120 s local Ollama (see change C-02g)
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> Settings:
        env = os.environ.get
        static = env("GRANITE_STATIC_DIR")
        timeout = env("GRANITE_LLM_TIMEOUT")
        defaults = cls()
        return cls(
            db_url=env("GRANITE_DB_URL", defaults.db_url),
            llm_mode=env("GRANITE_LLM_MODE", defaults.llm_mode),
            model=env("GRANITE_MODEL", defaults.model),
            ollama_url=env("GRANITE_OLLAMA_URL", defaults.ollama_url),
            openai_base_url=env("GRANITE_OPENAI_BASE_URL", ""),
            openai_api_key=env("GRANITE_OPENAI_API_KEY", ""),
            cassette_path=Path(env("GRANITE_CASSETTE", str(defaults.cassette_path))),
            record_live=_bool("GRANITE_RECORD", False),
            api_token=env("GRANITE_API_TOKEN", ""),
            cors_origins=tuple(o for o in env("GRANITE_CORS_ORIGINS", ",".join(defaults.cors_origins)).split(",") if o),
            rate_limit_per_minute=int(env("GRANITE_RATE_LIMIT", str(defaults.rate_limit_per_minute))),
            jobs_inline=_bool("GRANITE_JOBS_INLINE", False),
            max_workers=int(env("GRANITE_MAX_WORKERS", "2")),
            static_dir=Path(static) if static else None,
            llm_timeout_s=float(timeout) if timeout else None,
        )

    def validate(self) -> None:
        if self.llm_mode not in {"recorded", "live", "auto"}:
            raise ValueError(f"GRANITE_LLM_MODE must be recorded, live or auto (got '{self.llm_mode}')")
        for name, url in (("GRANITE_OLLAMA_URL", self.ollama_url), ("GRANITE_OPENAI_BASE_URL", self.openai_base_url)):
            if url and not url.startswith(("http://", "https://")):
                raise ValueError(f"{name} must start with http:// or https:// (got '{url}')")
        if bool(self.openai_base_url) != bool(self.openai_api_key):
            raise ValueError("set both GRANITE_OPENAI_BASE_URL and GRANITE_OPENAI_API_KEY, or neither")
