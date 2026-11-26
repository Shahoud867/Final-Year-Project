"""Arize Phoenix: read spans, send Granite runs as spans, and write verdicts back as span annotations.

Written against the Phoenix REST API v1 (checked against the arize-phoenix 21.0.0 server source):

* ``GET  /v1/projects/{project}/spans``        list spans (cursor ``next_cursor``, filters ``trace_id``, ``span_id``,
  ``start_time``); attributes come back flattened (``input.value``, ``granite.step_id``);
* ``POST /v1/projects/{project}/spans``        create spans (rejects the whole request if any span id exists);
* ``POST /v1/projects``                        create a project; ``GET /v1/projects/{project}`` reads one;
* ``POST /v1/span_annotations?sync=true``      annotate spans; same ``name`` and ``identifier`` updates in place.

Authentication, when the server has it on, is a bearer API key.
"""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterator
from datetime import datetime
from typing import Any

from .http import ConnectorError, HttpClient, Transport
from .spans import SpanKind, SpanRecord

RUNTIME = "phoenix"
PAGE = 500
ANNOTATOR = "granite"
_FROM_OI: dict[str, SpanKind] = {
    "LLM": "llm", "TOOL": "tool", "RETRIEVER": "retriever", "AGENT": "agent", "CHAIN": "chain",
}
_TO_OI = {"llm": "LLM", "tool": "TOOL", "retriever": "RETRIEVER", "agent": "AGENT", "chain": "CHAIN",
          "other": "UNKNOWN"}


def _iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def _value(attrs: dict[str, Any], key: str) -> Any:
    raw = attrs.get(f"{key}.value")
    if isinstance(raw, str) and attrs.get(f"{key}.mime_type", "application/json") == "application/json":
        try:
            return json.loads(raw)
        except ValueError:
            return raw
    return raw


def from_phoenix(span: dict[str, Any]) -> SpanRecord:
    """A Phoenix span (REST v1 JSON) as a neutral record."""
    attrs = dict(span.get("attributes") or {})
    status = "error" if str(span.get("status_code", "")).upper() == "ERROR" else "ok"
    granite = {k: v for k, v in attrs.items() if k.startswith(("granite.", "llm.model_name", "metadata."))}
    for k, v in list(granite.items()):  # an app can declare reads in metadata: metadata.granite.reads
        if k.startswith("metadata.granite."):
            granite[k.removeprefix("metadata.")] = v
    return SpanRecord(
        span_id=span["context"]["span_id"], trace_id=span["context"]["trace_id"], parent_id=span.get("parent_id"),
        name=span.get("name") or "span", kind=_FROM_OI.get(str(span.get("span_kind", "")).upper(), "other"),
        start=span.get("start_time"), end=span.get("end_time"), input=_value(attrs, "input"),
        output=_value(attrs, "output"), status=status,
        error=(span.get("status_message") or "error") if status == "error" else None, attributes=granite,
    )


def to_phoenix(record: SpanRecord) -> dict[str, Any]:
    """A neutral record as a Phoenix create-span body (OpenInference attributes, JSON input and output)."""
    attrs: dict[str, Any] = dict(record.attributes)
    for key, val in (("input", record.input), ("output", record.output)):
        if val is not None:
            attrs[f"{key}.value"] = json.dumps(val, default=str)
            attrs[f"{key}.mime_type"] = "application/json"
    return {
        "name": record.name, "context": {"trace_id": record.trace_id, "span_id": record.span_id},
        "span_kind": _TO_OI[record.kind], "parent_id": record.parent_id,
        "start_time": _iso(record.start), "end_time": _iso(record.end),
        "status_code": "ERROR" if record.status == "error" else "OK", "status_message": record.error or "",
        "attributes": attrs, "events": [],
    }


class PhoenixClient:
    """One Phoenix project: list, create and annotate spans."""

    def __init__(self, base_url: str, project: str, api_key: str | None = None,
                 transport: Transport | None = None, retries: int = 3) -> None:
        """Connect to ``base_url`` (``http://localhost:6006``) and work in ``project``."""
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.http = HttpClient(base_url, headers=headers, transport=transport, retries=retries)
        self.project = project

    # ---- reading ------------------------------------------------------------------------------------------------
    def ping(self) -> dict[str, Any]:
        """Check that the server answers and the project exists; returns the project."""
        body = self.http.get(f"/v1/projects/{self._p()}")
        return dict(body["data"])

    def spans(self, *, trace_ids: list[str] | None = None, since: datetime | None = None,
              max_spans: int = 5000) -> Iterator[SpanRecord]:
        """Spans of the project, newest first, optionally for given traces or after a time."""
        cursor, seen = None, 0
        while True:
            body = self.http.get(f"/v1/projects/{self._p()}/spans", {
                "limit": PAGE, "cursor": cursor, "trace_id": trace_ids, "start_time": _iso(since),
            })
            for span in body.get("data") or []:
                yield from_phoenix(span)
                seen += 1
                if seen >= max_spans:
                    return
            cursor = body.get("next_cursor")
            if not cursor:
                return

    def traces(self, *, since: datetime | None = None, limit: int = 20,
               trace_ids: list[str] | None = None) -> list[list[SpanRecord]]:
        """Complete traces, newest first: every span of up to ``limit`` traces."""
        by_trace: dict[str, list[SpanRecord]] = defaultdict(list)
        for record in self.spans(since=since, trace_ids=trace_ids):
            if record.trace_id not in by_trace and len(by_trace) >= limit:
                continue
            by_trace[record.trace_id].append(record)
        missing = [t for t in by_trace if not any(s.parent_id is None for s in by_trace[t])]
        if missing and trace_ids is None:  # a page boundary cut a trace: fetch those traces whole
            for record in self.spans(trace_ids=missing):
                if record.span_id not in {s.span_id for s in by_trace[record.trace_id]}:
                    by_trace[record.trace_id].append(record)
        return list(by_trace.values())

    # ---- writing ------------------------------------------------------------------------------------------------
    def ensure_project(self, description: str = "Runs sent by Granite") -> None:
        """Create the project if it does not exist yet."""
        try:
            self.ping()
        except ConnectorError as exc:
            if exc.status != 404:
                raise
            self.http.post("/v1/projects", {"name": self.project, "description": description})

    def send(self, records: list[SpanRecord]) -> int:
        """Create the spans that Phoenix does not have yet; returns how many were queued (0 if all existed)."""
        existing = {s.span_id for s in self.spans(trace_ids=sorted({r.trace_id for r in records}))}
        fresh = [r for r in records if r.span_id not in existing]
        if not fresh:
            return 0
        body = self.http.post(f"/v1/projects/{self._p()}/spans", {"data": [to_phoenix(r) for r in fresh]})
        return int((body or {}).get("total_queued", len(fresh)))

    def annotate(self, span_id: str, name: str, *, label: str, score: float | None, explanation: str,
                 metadata: dict[str, Any] | None = None) -> str:
        """Write (or update) one Granite annotation on a span; returns the annotation id."""
        body = self.http.post("/v1/span_annotations", {"data": [{
            "span_id": span_id, "name": name, "annotator_kind": "CODE", "identifier": ANNOTATOR,
            "result": {"label": label, "score": score, "explanation": explanation[:2000]},
            "metadata": metadata or {},
        }]}, params={"sync": "true"})
        data = (body or {}).get("data") or [{}]
        return str(data[0].get("id", ""))

    def annotations(self, span_ids: list[str]) -> list[dict[str, Any]]:
        """Annotations on the given spans (to show what Granite wrote)."""
        body = self.http.get(f"/v1/projects/{self._p()}/span_annotations", {"span_ids": span_ids, "limit": 1000})
        return list((body or {}).get("data") or [])

    def _p(self) -> str:
        from urllib.parse import quote
        return quote(self.project, safe="")


__all__ = ["ANNOTATOR", "RUNTIME", "PhoenixClient", "from_phoenix", "to_phoenix"]
