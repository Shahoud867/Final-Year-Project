"""Application factory: wires settings, database, job runner, middleware and routes."""

from __future__ import annotations

import time
import uuid
from collections import defaultdict, deque
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import __version__
from .config import Settings
from .db import Base, make_engine, make_session_factory
from .errors import install_handlers, problem
from .jobs import JobRunner, recover_interrupted
from .routes import public, router

MUTATING = {"POST", "PUT", "PATCH", "DELETE"}
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:",
}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    settings.validate()
    engine = make_engine(settings.db_url)
    Base.metadata.create_all(engine)
    factory = make_session_factory(engine)
    recover_interrupted(factory)
    runner = JobRunner(factory, inline=settings.jobs_inline, max_workers=settings.max_workers)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        runner.shutdown()
        engine.dispose()

    app = FastAPI(
        title="Granite API",
        version=__version__,
        description="Run multi-agent workflows, detect silent failures, trace them to their origin, verify, review.",
        lifespan=lifespan,
    )
    app.state.settings, app.state.session_factory, app.state.runner = settings, factory, runner
    hits: dict[str, deque[float]] = defaultdict(deque)

    @app.middleware("http")
    async def guard(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request.state.request_id = uuid.uuid4().hex[:12]
        limit = settings.rate_limit_per_minute
        if limit and request.method in MUTATING and request.url.path.startswith("/api"):
            client = request.client.host if request.client else "unknown"
            window, t = hits[client], time.monotonic()
            while window and t - window[0] > 60:
                window.popleft()
            if len(window) >= limit:
                resp = problem(request, 429, "Too many requests", f"Limit is {limit} changes per minute; slow down.")
                resp.headers["Retry-After"] = "30"
                return resp
            window.append(t)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        for name, value in SECURITY_HEADERS.items():
            response.headers.setdefault(name, value)
        return response

    app.add_middleware(
        CORSMiddleware, allow_origins=list(settings.cors_origins), allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )
    install_handlers(app)
    app.include_router(public)
    app.include_router(router)

    static = settings.static_dir
    if static and (static / "index.html").exists():
        app.mount("/assets", StaticFiles(directory=static / "assets"), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def spa(path: str) -> FileResponse:
            target = (static / path).resolve()
            if path and target.is_file() and static.resolve() in target.parents:
                return FileResponse(target)
            return FileResponse(static / "index.html")

    return app


def app_from_env() -> FastAPI:
    """Entry point for uvicorn: uvicorn granite_api.main:app_from_env --factory"""
    return create_app()
