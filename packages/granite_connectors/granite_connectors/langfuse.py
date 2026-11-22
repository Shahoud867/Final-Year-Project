"""Langfuse: read traces and observations, send Granite runs, and write verdicts back as scores.

Written against the documented Langfuse public API (Basic auth with the project's public and secret key):

* ``GET  /api/public/health``                       liveness;
* ``GET  /api/public/traces``             page-numbered list (``page``, ``limit``, ``name``, ``fromTimestamp``);
* ``GET  /api/public/observations?traceId=``        the observations of a trace (page-numbered; works on Cloud and
  self-hosted v3 alike, unlike the cursor-based v2 endpoint which is Cloud-only at the time of writing);
* ``POST /api/public/ingestion``                    batched ``trace-create`` / ``span-create`` / ``generation-create``
  events (HTTP 207 with per-event ``errors``);
* ``POST /api/public/scores``                       a score on a trace or an observation; the same ``id`` updates it.

Unlike the Phoenix connector this module has not been run against a live Langfuse instance in this repository;
``scripts/check_connectors_live.py`` exercises it once keys are available (integrations strategy, section 7).
"""

from __future__ import annotations

import base64
from collections.abc import Iterator
from datetime import datetime
from typing import Any

from .export import hex_id
from .http import ConnectorError, HttpClient, Transport
from .spans import SpanKind, SpanRecord

RUNTIME = "langfuse"
PAGE = 100
_FROM_TYPE: dict[str, SpanKind] = {
    "GENERATION": "llm", "TOOL": "tool", "RETRIEVER": "retriever", "AGENT": "agent", "CHAIN": "chain",
    "SPAN": "other", "EVENT": "other",
}


def _iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def from_langfuse(obs: dict[str, Any]) -> SpanRecord:
    """A Langfuse observation as a neutral record (metadata becomes attributes, so ``granite.reads`` survives)."""
    meta = obs.get("metadata")
    attrs: dict[str, Any] = dict(meta) if isinstance(meta, dict) else {}
    if obs.get("model"):
        attrs["llm.model_name"] = obs["model"]
    error = str(obs.get("level", "")).upper() == "ERROR"
    return SpanRecord(
        span_id=str(obs["id"]), trace_id=str(obs["traceId"]), parent_id=obs.get("parentObservationId"),
        name=obs.get("name") or str(obs.get("type", "observation")).lower(),
        kind=_FROM_TYPE.get(str(obs.get("type", "")).upper(), "other"),
        start=obs.get("startTime"), end=obs.get("endTime"), input=obs.get("input"), output=obs.get("output"),
        status="error" if error else "ok", error=(obs.get("statusMessage") or "error") if error else None,
        attributes=attrs,
    )


def to_ingestion(records: list[SpanRecord], trace_name: str) -> list[dict[str, Any]]:
    """Ingestion events for one trace: the root record becomes the trace, the others observations under it."""
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
        self.http.get("/api/public/traces", {"limit": 1})
        return dict(health)

    def trace_ids(self, *, since: datetime | None = None, name: str | None = None, limit: int = 20) -> list[str]:
        """Ids of the newest traces (optionally only those with ``name``)."""
        ids: list[str] = []
        page = 1
        while len(ids) < limit:
            body = self.http.get("/api/public/traces", {
                "page": page, "limit": min(PAGE, limit), "name": name, "fromTimestamp": _iso(since),
            }) or {}
            ids += [str(t["id"]) for t in body.get("data") or []]
            if page >= int((body.get("meta") or {}).get("totalPages", page)) or not body.get("data"):
                break
            page += 1
        return ids[:limit]

    def observations(self, trace_id: str) -> Iterator[SpanRecord]:
        """Every observation of one trace."""
        page = 1
        while True:
            body = self.http.get("/api/public/observations", {"traceId": trace_id, "page": page, "limit": PAGE}) or {}
            for obs in body.get("data") or []:
                yield from_langfuse(obs)
            if page >= int((body.get("meta") or {}).get("totalPages", page)) or not body.get("data"):
                return
            page += 1

    def trace(self, trace_id: str) -> list[SpanRecord]:
        """One trace: its observations plus a root record built from the trace itself (input, output, name)."""
        doc = self.http.get(f"/api/public/traces/{trace_id}") or {}
        root = SpanRecord(span_id=f"trace:{trace_id}", trace_id=trace_id, name=doc.get("name") or "trace",
                          kind="chain", start=doc.get("timestamp"), input=doc.get("input"), output=doc.get("output"),
                          attributes=dict(doc.get("metadata") or {}) if isinstance(doc.get("metadata"), dict) else {})
        records = [root]
        for rec in self.observations(trace_id):
            records.append(rec.model_copy(update={"parent_id": rec.parent_id or root.span_id}))
        return records

    def traces(self, *, since: datetime | None = None, name: str | None = None,
               limit: int = 20) -> list[list[SpanRecord]]:
        """Complete traces, newest first."""
        return [self.trace(t) for t in self.trace_ids(since=since, name=name, limit=limit)]

    def send(self, records: list[SpanRecord], trace_name: str) -> int:
        """Ingest one trace; returns how many events Langfuse accepted. Re-sending the same ids updates them."""
        body = self.http.post("/api/public/ingestion", {"batch": to_ingestion(records, trace_name)}) or {}
        errors = body.get("errors") or []
        if errors:
            first = errors[0]
            raise ConnectorError(f"Langfuse rejected {len(errors)} event(s): {first.get('message', first)}", 207)
        return len(body.get("successes") or [])

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


__all__ = ["RUNTIME", "LangfuseClient", "from_langfuse", "to_ingestion"]
