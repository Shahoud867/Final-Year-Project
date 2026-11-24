"""Langfuse: read traces and observations, send Granite runs, and write verdicts back as scores.

Written against the Langfuse public API v4 (Basic auth with the project's public and secret key):

* ``GET  /api/public/health``                              liveness;
* ``GET  /api/public/v2/observations?traceId=&fields=``    cursor-paginated observations (replaces the removed v1
  ``/traces`` and ``/observations`` endpoints);
* ``POST /api/public/otel/v1/traces``                      OTLP/HTTP JSON ingestion (replaces the removed
  ``/api/public/ingestion`` endpoint, which now accepts only ``score-create`` events);
* ``POST /api/public/scores``                              a score on a trace or an observation; the same ``id``
  updates it.

Verified live against Langfuse Cloud (v4.86.0, JP region) on 2026-11-25.
"""

from __future__ import annotations

import base64
import json
import time
from collections.abc import Iterator
from datetime import datetime
from typing import Any

from .export import hex_id
from .http import ConnectorError, HttpClient, Transport
from .spans import SpanKind, SpanRecord

RUNTIME = "langfuse"
PAGE = 200
_FROM_TYPE: dict[str, SpanKind] = {
    "GENERATION": "llm", "TOOL": "tool", "RETRIEVER": "retriever", "AGENT": "agent", "CHAIN": "chain",
    "SPAN": "other", "EVENT": "other",
}
_TO_OTLP_KIND: dict[str, int] = {
    "other": 1, "chain": 1, "llm": 3, "tool": 3, "retriever": 3, "agent": 1,
}


def _iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def _ns(dt: datetime | None) -> str:
    return str(int(dt.timestamp() * 1e9)) if dt else str(int(time.time() * 1e9))


def _parse_input(raw: Any) -> Any:
    """Parse a string input back to a dict/list if it looks like JSON."""
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (ValueError, TypeError):
            return raw
    return raw


def from_langfuse(obs: dict[str, Any]) -> SpanRecord:
    """A Langfuse v2 observation as a neutral record.

    In v2, metadata keys from OTLP ingestion arrive prefixed (``attributes.granite.reads``);
    we strip the ``attributes.`` prefix so downstream code sees the same keys as before.
    Input/output may live in the top-level fields or in metadata as ``langfuse.span.input``/``output``.
    """
    meta = obs.get("metadata")
    attrs: dict[str, Any] = {}
    lf_input: Any = None
    lf_output: Any = None
    if isinstance(meta, dict):
        for k, v in meta.items():
            clean = k.removeprefix("attributes.")
            if clean == "langfuse.span.input":
                lf_input = _parse_input(v)
                continue
            if clean == "langfuse.span.output":
                lf_output = _parse_input(v)
                continue
            if clean.startswith(("langfuse.", "scope.", "resourceAttributes.")):
                continue
            if isinstance(v, str) and v in ("True", "False"):
                attrs[clean] = v == "True"
            else:
                attrs[clean] = v
    if obs.get("model"):
        attrs["llm.model_name"] = obs["model"]
    elif obs.get("modelId"):
        attrs["llm.model_name"] = obs["modelId"]
    inp = _parse_input(obs.get("input")) if obs.get("input") is not None else lf_input
    outp = _parse_input(obs.get("output")) if obs.get("output") is not None else lf_output
    error = str(obs.get("level", "")).upper() == "ERROR"
    return SpanRecord(
        span_id=str(obs["id"]), trace_id=str(obs["traceId"]), parent_id=obs.get("parentObservationId"),
        name=obs.get("name") or str(obs.get("type", "observation")).lower(),
        kind=_FROM_TYPE.get(str(obs.get("type", "")).upper(), "other"),
        start=obs.get("startTime"), end=obs.get("endTime"),
        input=inp, output=outp,
        status="error" if error else "ok", error=(obs.get("statusMessage") or "error") if error else None,
        attributes=attrs,
    )


def to_ingestion(records: list[SpanRecord], trace_name: str) -> list[dict[str, Any]]:
    """Legacy ingestion events (kept for the in-memory test double)."""
    root = next(r for r in records if r.parent_id is None)
    events: list[dict[str, Any]] = [{
        "id": hex_id(f"evt:{root.trace_id}", 32), "type": "trace-create", "timestamp": _iso(root.start),
        "body": {"id": root.trace_id, "name": trace_name, "timestamp": _iso(root.start), "input": root.input,
                 "output": root.output, "metadata": root.attributes},
    }]
    for r in records:
        if r is root:
            continue
        body: dict[str, Any] = {
            "id": r.span_id, "traceId": r.trace_id, "name": r.name, "startTime": _iso(r.start),
            "endTime": _iso(r.end), "input": r.input, "output": r.output, "metadata": r.attributes,
            "level": "ERROR" if r.status == "error" else "DEFAULT", "statusMessage": r.error,
        }
        if r.parent_id != root.span_id:
            body["parentObservationId"] = r.parent_id
        kind = "generation-create" if r.kind == "llm" else "span-create"
        if kind == "generation-create" and r.attributes.get("llm.model_name"):
            body["model"] = r.attributes["llm.model_name"]
        events.append({"id": hex_id(f"evt:{r.span_id}", 32), "type": kind, "timestamp": _iso(r.start),
                       "body": body})
    return events


def to_otlp(records: list[SpanRecord], trace_name: str) -> dict[str, Any]:
    """OTLP/HTTP JSON payload (ExportTraceServiceRequest) for one trace."""
    root = next(r for r in records if r.parent_id is None)
    spans: list[dict[str, Any]] = []
    for r in records:
        otlp_attrs: list[dict[str, Any]] = [
            {"key": "langfuse.span.name", "value": {"stringValue": r.name}},
        ]
        if r is root:
            otlp_attrs.append({"key": "langfuse.trace.name", "value": {"stringValue": trace_name}})
        for k, v in r.attributes.items():
            otlp_attrs.append({"key": k, "value": {"stringValue": str(v) if not isinstance(v, str) else v}})
        if r.input is not None:
            otlp_attrs.append({"key": "langfuse.span.input", "value": {"stringValue": json.dumps(r.input, default=str)}})
        if r.output is not None:
            otlp_attrs.append({"key": "langfuse.span.output", "value": {"stringValue": json.dumps(r.output, default=str)}})
        if r.status == "error":
            otlp_attrs.append({"key": "langfuse.observation.level", "value": {"stringValue": "ERROR"}})
        if r.error:
            otlp_attrs.append({"key": "langfuse.status.message", "value": {"stringValue": r.error}})
        parent = r.parent_id or ("" if r is root else root.span_id)
        span: dict[str, Any] = {
            "traceId": r.trace_id,
            "spanId": r.span_id if len(r.span_id) == 16 else hex_id(f"otel:{r.span_id}", 16),
            "name": r.name,
            "kind": _TO_OTLP_KIND.get(r.kind, 1),
            "startTimeUnixNano": _ns(r.start),
            "endTimeUnixNano": _ns(r.end),
            "attributes": otlp_attrs,
            "status": {"code": 2 if r.status == "error" else 1},
        }
        if parent:
            span["parentSpanId"] = parent if len(parent) == 16 else hex_id(f"otel:{parent}", 16)
        spans.append(span)
    return {
        "resourceSpans": [{
            "resource": {"attributes": [
                {"key": "service.name", "value": {"stringValue": "granite-connectors"}},
            ]},
            "scopeSpans": [{"scope": {"name": "granite-connectors"}, "spans": spans}],
        }],
    }


class LangfuseClient:
    """One Langfuse project, addressed by its host and API key pair."""

    def __init__(self, host: str, public_key: str, secret_key: str, transport: Transport | None = None,
                 retries: int = 3) -> None:
        """Connect to ``host`` (``https://cloud.langfuse.com`` or a self-hosted URL)."""
        token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
        self.http = HttpClient(host, headers={"Authorization": f"Basic {token}"}, transport=transport,
                               retries=retries)

    def ping(self) -> dict[str, Any]:
        """Health check, then one authenticated call so wrong keys fail here and not during an import."""
        health = self.http.get("/api/public/health") or {}
        self.http.get("/api/public/v2/observations", {"limit": 1, "fields": "core"})
        return dict(health)

    def trace_ids(self, *, since: datetime | None = None, name: str | None = None, limit: int = 20) -> list[str]:
        """Ids of the newest traces (optionally only those with ``name``), via v2 observations."""
        ids: list[str] = []
        seen: set[str] = set()
        cursor: str | None = None
        while len(ids) < limit:
            params: dict[str, Any] = {"limit": min(PAGE, limit * 5), "fields": "core,basic"}
            if since:
                params["fromStartTime"] = _iso(since)
            if name:
                params["name"] = name
            if cursor:
                params["cursor"] = cursor
            body = self.http.get("/api/public/v2/observations", params) or {}
            for obs in body.get("data") or []:
                tid = str(obs["traceId"])
                if obs.get("isRootObservation") and tid not in seen:
                    seen.add(tid)
                    ids.append(tid)
            cursor = (body.get("meta") or {}).get("cursor")
            if not cursor or not body.get("data"):
                break
        return ids[:limit]

    def observations(self, trace_id: str) -> Iterator[SpanRecord]:
        """Every observation of one trace, via v2 observations."""
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {
                "traceId": trace_id, "limit": PAGE, "fields": "core,basic,io,metadata",
            }
            if cursor:
                params["cursor"] = cursor
            body = self.http.get("/api/public/v2/observations", params) or {}
            for obs in body.get("data") or []:
                yield from_langfuse(obs)
            cursor = (body.get("meta") or {}).get("cursor")
            if not cursor or not body.get("data"):
                return

    def trace(self, trace_id: str) -> list[SpanRecord]:
        """One trace: observations plus a synthetic root built from the root observation."""
        obs_records = list(self.observations(trace_id))
        root_obs = next((r for r in obs_records if r.parent_id is None or r.parent_id == ""), None)
        if root_obs:
            root = root_obs.model_copy(update={
                "span_id": f"trace:{trace_id}",
                "parent_id": None,
                "kind": "chain",
            })
            children = []
            for rec in obs_records:
                if rec is root_obs:
                    continue
                pid = rec.parent_id if rec.parent_id != root_obs.span_id else root.span_id
                children.append(rec.model_copy(update={"parent_id": pid or root.span_id}))
            return [root] + children
        root = SpanRecord(span_id=f"trace:{trace_id}", trace_id=trace_id, name="trace", kind="chain")
        return [root] + [r.model_copy(update={"parent_id": r.parent_id or root.span_id}) for r in obs_records]

    def traces(self, *, since: datetime | None = None, name: str | None = None,
               limit: int = 20) -> list[list[SpanRecord]]:
        """Complete traces, newest first."""
        return [self.trace(t) for t in self.trace_ids(since=since, name=name, limit=limit)]

    def send(self, records: list[SpanRecord], trace_name: str) -> int:
        """Ingest one trace via OTLP; returns the number of spans sent."""
        payload = to_otlp(records, trace_name)
        self.http.post("/api/public/otel/v1/traces", payload)
        return len(payload["resourceSpans"][0]["scopeSpans"][0]["spans"])

    def score(self, trace_id: str, observation_id: str | None, name: str, *, label: str,
              comment: str, metadata: dict[str, Any] | None = None) -> str:
        """Write (or update) a categorical Granite score; the id is stable per trace, observation and name."""
        score_id = hex_id(f"granite-score:{trace_id}:{observation_id}:{name}", 32)
        body: dict[str, Any] = {"id": score_id, "traceId": trace_id, "name": name, "value": label,
                                "dataType": "CATEGORICAL", "comment": comment[:2000], "metadata": metadata or {}}
        if observation_id:
            body["observationId"] = observation_id
        self.http.post("/api/public/scores", body)
        return score_id


__all__ = ["RUNTIME", "LangfuseClient", "from_langfuse", "to_ingestion", "to_otlp"]
