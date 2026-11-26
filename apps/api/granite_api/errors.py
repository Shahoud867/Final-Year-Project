"""RFC 7807 problem responses: every error the API returns has the same shape and never leaks internals."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from granite_core.lifecycle import IllegalTransition, allowed_events
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger("granite.api")
PROBLEM = "application/problem+json"


class ProblemError(Exception):
    """An error with an HTTP status and a message that is safe to show to the user."""
    def __init__(self, status: int, title: str, detail: str = "", **extra: Any) -> None:
        super().__init__(f"{status} {title}: {detail}")
        self.status, self.title, self.detail, self.extra = status, title, detail, extra


def problem(request: Request, status: int, title: str, detail: str = "", **extra: Any) -> JSONResponse:
    """Build an RFC 7807 problem response."""
    body = {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "instance": request.url.path,
        "request_id": getattr(request.state, "request_id", None),
        **extra,
    }
    return JSONResponse(body, status_code=status, media_type=PROBLEM)


def install_handlers(app: FastAPI) -> None:
    """Register handlers so that every error leaves the API as a problem response."""
    @app.exception_handler(ProblemError)
    async def _problem(request: Request, exc: ProblemError) -> JSONResponse:
        return problem(request, exc.status, exc.title, exc.detail, **exc.extra)

    @app.exception_handler(IllegalTransition)
    async def _illegal(request: Request, exc: IllegalTransition) -> JSONResponse:
        allowed = [e.value for e in allowed_events(exc.status)]
        return problem(request, 409, "Action not allowed in this state", str(exc), allowed_actions=allowed)

    @app.exception_handler(RequestValidationError)
    async def _invalid(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            {"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": str(e["msg"])}
            for e in exc.errors()
        ]
        return problem(request, 422, "Invalid request", "One or more fields are invalid.", errors=errors)

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        titles = {401: "Authentication required", 404: "Not found", 405: "Method not allowed"}
        return problem(request, exc.status_code, titles.get(exc.status_code, "Request failed"), str(exc.detail))

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception) -> JSONResponse:
        log.exception("unhandled error on %s", request.url.path)
        return problem(request, 500, "Internal error", "Something went wrong on the server. It has been logged.")
