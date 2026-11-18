"""In-memory stand-ins for the Phoenix and Langfuse REST endpoints the connectors use.

They follow the request and response shapes of the real servers (Phoenix 21 REST v1, Langfuse public API) closely
enough to test paging, idempotency and error handling; the live checks in scripts/check_connectors_live.py cover the
real servers.
"""

from __future__ import annotations

import json
import urllib.parse
from collections.abc import Mapping
from typing import Any

Reply = tuple[int, Mapping[str, str], bytes]


def _json(status: int, doc: Any) -> Reply:
    return status, {}, json.dumps(doc).encode()


def _flatten(prefix: str, value: Any, out: dict[str, Any]) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            _flatten(f"{prefix}.{k}" if prefix else k, v, out)
    else:
        out[prefix] = value


def _unflatten(attrs: dict[str, Any]) -> dict[str, Any]:
    root: dict[str, Any] = {}
    for key, value in attrs.items():
        node = root
        *parents, leaf = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[leaf] = value
    return root


class FakePhoenix:
    """Projects, spans (stored unflattened, returned flattened, like Phoenix) and span annotations."""

    def __init__(self, page: int = 1000) -> None:
        self.projects: dict[str, list[dict[str, Any]]] = {}
        self.annotations: dict[tuple[str, str, str], dict[str, Any]] = {}
        self.page = page
        self.calls: list[tuple[str, str]] = []
        self.headers: list[Mapping[str, str]] = []

    def __call__(self, method: str, url: str, headers: Mapping[str, str], body: bytes | None) -> Reply:
        """Answer one request as Phoenix would."""
        parts = urllib.parse.urlsplit(url)
        q = urllib.parse.parse_qs(parts.query)
        path = urllib.parse.unquote(parts.path)
        self.calls.append((method, path))
        self.headers.append(headers)
        doc: Any = json.loads(body) if body else None
        segs = path.strip("/").split("/")
        if segs == ["v1", "projects"] and method == "POST":
            self.projects.setdefault(doc["name"], [])
            return _json(200, {"data": {"id": "UHJvamVjdDox", "name": doc["name"]}})
        if segs == ["v1", "projects"]:
            return _json(200, {"data": [{"id": "UHJvamVjdDox", "name": p} for p in self.projects], "next_cursor": None})
        if segs == ["v1", "span_annotations"]:
            for a in doc["data"]:
                self.annotations[(a["span_id"], a["name"], a["identifier"])] = a
            return _json(200, {"data": [{"id": f"ann{len(self.annotations)}"} for _ in doc["data"]]})
        if segs[:2] != ["v1", "projects"] or len(segs) < 3:
            return _json(404, {"detail": "not found"})
        project = segs[2]
        if project not in self.projects:
            return _json(404, {"detail": f"Project {project} not found"})
        if len(segs) == 3:
            return _json(200, {"data": {"id": "UHJvamVjdDox", "name": project}})
        if segs[3] == "spans" and method == "POST":
            return self._create(project, doc["data"])
        if segs[3] == "spans":
            return self._list(project, q)
        return _json(404, {})

    def _create(self, project: str, spans: list[dict[str, Any]]) -> Reply:
        stored = self.projects[project]
        ids = {s["context"]["span_id"] for s in stored}
        if any(s["context"]["span_id"] in ids for s in spans):
            return _json(400, {"detail": "Request contains invalid or duplicate spans"})
        stored += [{**s, "attributes": _unflatten(s["attributes"])} for s in spans]
        return _json(202, {"total_received": len(spans), "total_queued": len(spans)})

    def _list(self, project: str, q: dict[str, list[str]]) -> Reply:
        spans = list(reversed(self.projects[project]))
        if "trace_id" in q:
            spans = [s for s in spans if s["context"]["trace_id"] in q["trace_id"]]
        start = int(q.get("cursor", ["0"])[0])
        chunk = spans[start:start + min(self.page, int(q.get("limit", ["100"])[0]))]
        nxt = start + len(chunk)
        out = []
        for s in chunk:
            flat: dict[str, Any] = {}
            _flatten("", s["attributes"], flat)
            out.append({**s, "attributes": flat})
        return _json(200, {"data": out, "next_cursor": str(nxt) if nxt < len(spans) else None})


class FakeLangfuse:
    """Traces and observations from ingestion events, page-numbered lists, and scores."""

    def __init__(self, page: int = 100) -> None:
        self.traces: dict[str, dict[str, Any]] = {}
        self.observations: dict[str, dict[str, Any]] = {}
        self.scores: dict[str, dict[str, Any]] = {}
        self.page = page
        self.reject: str | None = None

    def __call__(self, method: str, url: str, headers: Mapping[str, str], body: bytes | None) -> Reply:
        """Answer one request as Langfuse would."""
        if not headers.get("Authorization", "").startswith("Basic "):
            return 401, {}, b'{"message": "Unauthorized"}'
        parts = urllib.parse.urlsplit(url)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(parts.query).items()}
        path = parts.path
        doc: Any = json.loads(body) if body else None
        if path == "/api/public/health":
            return 200, {}, b'{"status": "OK", "version": "3.0.0"}'
        if path == "/api/public/ingestion":
            errors, ok = [], []
            for e in doc["batch"]:
                if self.reject and e["type"] == self.reject:
                    errors.append({"id": e["id"], "status": 400, "message": "invalid body"})
                    continue
                if e["type"] == "trace-create":
                    self.traces[e["body"]["id"]] = e["body"]
                else:
                    self.observations[e["body"]["id"]] = {**e["body"], "type": e["type"].split("-")[0].upper()}
                ok.append({"id": e["id"], "status": 201})
            return 207, {}, json.dumps({"successes": ok, "errors": errors}).encode()
        if path == "/api/public/scores":
            self.scores[doc["id"]] = doc
            return 200, {}, json.dumps({"id": doc["id"]}).encode()
        if path == "/api/public/traces":
            rows = [t for t in reversed(self.traces.values()) if "name" not in q or t["name"] == q["name"]]
            return self._page(rows, q)
        if path.startswith("/api/public/traces/"):
            tid = path.rsplit("/", 1)[1]
            return (200, {}, json.dumps(self.traces[tid]).encode()) if tid in self.traces else (404, {}, b"{}")
        if path == "/api/public/observations":
            rows = [o for o in self.observations.values() if o["traceId"] == q["traceId"]]
            return self._page(rows, q)
        return 404, {}, b"{}"

    def _page(self, rows: list[dict[str, Any]], q: dict[str, str]) -> Reply:
        limit = min(self.page, int(q.get("limit", "50")))
        page = int(q.get("page", "1"))
        total_pages = max(1, -(-len(rows) // limit))
        chunk = rows[(page - 1) * limit: page * limit]
        meta = {"page": page, "limit": limit, "totalItems": len(rows), "totalPages": total_pages}
        return 200, {}, json.dumps({"data": chunk, "meta": meta}).encode()
