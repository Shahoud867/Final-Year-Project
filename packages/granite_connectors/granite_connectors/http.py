"""A small JSON-over-HTTP client with retries, built on the standard library so connectors add no dependencies.

Transient failures (connection errors, 429 and 5xx) are retried with exponential backoff, honouring
``Retry-After``. Everything else becomes a :class:`ConnectorError` whose message is safe to show to an analyst:
credentials never appear in it.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

#: (method, url, headers, body) -> (status, response headers, body). Tests pass a fake; production uses urllib.
Transport = Callable[[str, str, Mapping[str, str], bytes | None], tuple[int, Mapping[str, str], bytes]]
RETRY_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})
USER_AGENT = "granite-connectors/0.1"


class ConnectorError(Exception):
    """A request to a third-party platform failed; ``status`` is the HTTP status, or 0 if none was received."""

    def __init__(self, message: str, status: int = 0) -> None:
        super().__init__(message)
        self.status = status


def urllib_transport(timeout: float) -> Transport:
    """The production transport: one HTTP request through urllib (http and https only)."""
    def send(method: str, url: str, headers: Mapping[str, str], body: bytes | None) -> tuple[
            int, Mapping[str, str], bytes]:
        if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
            raise ConnectorError(f"only http and https URLs are allowed, not {url!r}")
        req = urllib.request.Request(url, data=body, method=method, headers=dict(headers))  # noqa: S310
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
                return resp.status, dict(resp.headers.items()), resp.read()
        except urllib.error.HTTPError as exc:
            return exc.code, dict(exc.headers.items()) if exc.headers else {}, exc.read()
    return send


@dataclass
class HttpClient:
    """JSON requests against one base URL with fixed headers (authentication goes here, never in the URL)."""

    base_url: str
    headers: dict[str, str] = field(default_factory=dict)
    timeout: float = 20.0
    retries: int = 3
    backoff: float = 0.5
    transport: Transport | None = None
    sleep: Callable[[float], None] = time.sleep

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        if self.transport is None:
            self.transport = urllib_transport(self.timeout)

    def url(self, path: str, params: Mapping[str, Any] | None = None) -> str:
        """Absolute URL for a path, with the non-empty query parameters encoded."""
        query = urllib.parse.urlencode(
            [(k, v) for k, v in (params or {}).items() if v is not None and v != ""], doseq=True)
        return f"{self.base_url}{path}" + (f"?{query}" if query else "")

    def request(self, method: str, path: str, params: Mapping[str, Any] | None = None, body: Any = None) -> Any:
        """Send one request and return the decoded JSON (None for an empty body); retries transient failures."""
        url = self.url(path, params)
        headers = {"Accept": "application/json", "User-Agent": USER_AGENT, **self.headers}
        data = None
        if body is not None:
            data = json.dumps(body, default=str).encode()
            headers["Content-Type"] = "application/json"
        assert self.transport is not None
        status, raw = 0, b""
        resp_headers: Mapping[str, str] = {}
        for attempt in range(self.retries + 1):
            try:
                status, resp_headers, raw = self.transport(method, url, headers, data)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                if attempt == self.retries:
                    raise ConnectorError(f"{method} {path}: could not reach {self.base_url} ({_reason(exc)})") from None
                self.sleep(self.backoff * 2 ** attempt)
                continue
            if status not in RETRY_STATUS or attempt == self.retries:
                break
            self.sleep(_retry_after(resp_headers) or self.backoff * 2 ** attempt)
        if status >= 400:
            raise ConnectorError(f"{method} {path} returned HTTP {status}: {_detail(raw)}", status)
        if not raw.strip():
            return None
        try:
            return json.loads(raw)
        except ValueError:
            raise ConnectorError(f"{method} {path} did not return JSON", status) from None

    def get(self, path: str, params: Mapping[str, Any] | None = None) -> Any:
        """GET and decode JSON."""
        return self.request("GET", path, params)

    def post(self, path: str, body: Any, params: Mapping[str, Any] | None = None) -> Any:
        """POST a JSON body and decode the JSON reply."""
        return self.request("POST", path, params, body)


def _reason(exc: BaseException) -> str:
    reason = getattr(exc, "reason", None)
    return str(reason or exc.__class__.__name__)[:200]


def _retry_after(headers: Mapping[str, str]) -> float | None:
    value = next((v for k, v in headers.items() if k.lower() == "retry-after"), None)
    try:
        return min(float(value), 30.0) if value is not None else None
    except ValueError:
        return None


def _detail(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace").strip()
    try:
        doc = json.loads(text)
        if isinstance(doc, dict):
            text = str(doc.get("detail") or doc.get("message") or doc.get("error") or text)
    except ValueError:
        pass
    return text[:300] or "no detail"


__all__ = ["ConnectorError", "HttpClient", "Transport", "urllib_transport"]
