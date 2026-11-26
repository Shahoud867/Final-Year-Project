"""Connections to Arize Phoenix and Langfuse: import traces, send runs, write verdicts back (F13, ADR-012).

Imported traces are analysed exactly like runs Granite executed: the workflow's checks run on them, findings open,
suspects are ranked. Replay verification needs a workflow Granite can execute, so a connection names one; a trace
whose steps do not match that workflow is skipped with a reason instead of being forced into it.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from granite_connectors import (
    ConnectorError,
    LangfuseClient,
    MappedTrace,
    PhoenixClient,
    Profile,
    SpanRecord,
    map_trace,
    trace_to_spans,
)
from granite_connectors.http import Transport
from granite_core.lifecycle import FindingStatus, verification_level
from granite_core.runner import RunOutcome
from sqlalchemy.orm import Session

from ..config import Settings
from ..errors import ProblemError
from ..models import Connection, Finding, Run, TraceLink, new_id
from .analysis import persist_outcome
from .common import audit
from .runs import ensure_project, entry_for

KINDS = ("phoenix", "langfuse")
MAX_IMPORT = 50
#: Tests replace this with an in-memory server; production uses urllib.
TRANSPORT: Transport | None = None
VERDICT_SCORE = {"confirmed": 1.0, "refuted": 0.0, "inconclusive": 0.5}


def client_for(conn: Connection, settings: Settings) -> PhoenixClient | LangfuseClient:
    """The platform client of a connection, authenticated with keys from the environment."""
    if conn.kind == "phoenix":
        return PhoenixClient(conn.base_url, conn.project, settings.phoenix_api_key or None, transport=TRANSPORT,
                             retries=2)
    if not (settings.langfuse_public_key and settings.langfuse_secret_key):
        raise ProblemError(409, "Langfuse keys missing",
                           "Set GRANITE_LANGFUSE_PUBLIC_KEY and GRANITE_LANGFUSE_SECRET_KEY on the server, then retry.")
    return LangfuseClient(conn.base_url, settings.langfuse_public_key, settings.langfuse_secret_key,
                          transport=TRANSPORT, retries=2)


def _platform_error(conn: Connection, exc: ConnectorError) -> ProblemError:
    hint = {401: " Check the API keys.", 403: " The keys lack permission.", 404: " Check the URL and project name."}
    return ProblemError(502, f"{conn.kind.title()} request failed", f"{exc}.{hint.get(exc.status, '')}")


def get_connection(session: Session, connection_id: str) -> Connection:
    """A connection, or a 404 problem."""
    conn = session.get(Connection, connection_id)
    if conn is None:
        raise ProblemError(404, "Connection not found", f"There is no connection {connection_id}.")
    return conn


def create_connection(session: Session, kind: str, name: str, base_url: str, project: str, workflow: str,
                      steps: dict[str, str]) -> Connection:
    """Store a connection (no secrets). The workflow must be one Granite can run."""
    if kind not in KINDS:
        raise ProblemError(422, "Unknown platform", f"Choose one of: {', '.join(KINDS)}.")
    if not base_url.startswith(("http://", "https://")):
        raise ProblemError(422, "Invalid URL", "The URL must start with http:// or https://.")
    if kind == "phoenix" and not project:
        raise ProblemError(422, "Project required", "Name the Phoenix project to read from and write to.")
    entry_for(workflow)
    conn = Connection(id=new_id("con"), kind=kind, name=name, base_url=base_url.rstrip("/"), project=project,
                      workflow_key=workflow, profile={"steps": steps})
    session.add(conn)
    session.flush()
    audit(session, "analyst", "connection_created", "connection", conn.id, kind=kind, url=conn.base_url)
    return conn


def test_connection(conn: Connection, settings: Settings) -> dict[str, Any]:
    """Reach the platform with the configured keys; returns what it said about itself."""
    client = client_for(conn, settings)
    try:
        return {"ok": True, "detail": client.ping()}
    except ConnectorError as exc:
        if isinstance(client, PhoenixClient) and exc.status == 404:
            try:  # the server answers, only the project is new: it is created when the first run is sent
                client.http.get("/v1/projects", {"limit": 1})
                note = (f"Project '{conn.project}' does not exist yet; it is created when the first run is sent. "
                        "Nothing can be imported until then.")
                return {"ok": True, "detail": {"note": note}}
            except ConnectorError:
                pass
        return {"ok": False, "detail": {"error": str(exc), "status": exc.status}}


def _profile(conn: Connection) -> Profile:
    return Profile(name=conn.name, steps=dict(conn.profile.get("steps") or {}), workflow=conn.workflow_key,
                   trace_name=conn.project or None)


def _fetch(conn: Connection, settings: Settings, limit: int) -> list[list[SpanRecord]]:
    client = client_for(conn, settings)
    try:
        if isinstance(client, PhoenixClient):
            return client.traces(limit=limit)
        return client.traces(limit=limit, name=conn.project or None)
    except ConnectorError as exc:
        raise _platform_error(conn, exc) from None


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _store_import(session: Session, conn: Connection, mapped: MappedTrace) -> Run:
    entry = entry_for(conn.workflow_key)
    attrs = mapped.run_attrs
    defn = entry.build(str(attrs.get("model") or "imported"))
    trace = mapped.trace
    run = Run(
        id=new_id("run"), project_id=ensure_project(session, entry).id, workflow_key=entry.key, status="running",
        llm_mode="imported", model=str(attrs.get("model") or "unknown"), seed=_int(attrs.get("seed"), 1),
        fault_type=None, task_input=trace.run.task_input,
    )
    session.add(run)
    session.flush()
    persist_outcome(session, run, defn, RunOutcome(trace=trace, fault=None, calls=[]))
    session.add(TraceLink(
        connection_id=conn.id, run_id=run.id, direction="imported", external_trace_id=trace.run.external_id or "",
        root_span_id=mapped.root_span_id or "", span_ids=mapped.span_ids,
        lineage=[e.model_dump() for e in mapped.lineage],
    ))
    return run


def import_traces(session: Session, settings: Settings, conn: Connection, limit: int) -> dict[str, Any]:
    """Import the newest traces not imported before; returns what was imported and what was skipped and why."""
    traces = _fetch(conn, settings, min(limit, MAX_IMPORT))
    known = {link.external_trace_id for link in session.query(TraceLink).filter_by(
        connection_id=conn.id, direction="imported")}
    expected = entry_for(conn.workflow_key).build("imported").step_ids()
    imported: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    profile = _profile(conn)
    for spans in traces:
        trace_id = spans[0].trace_id
        if trace_id in known:
            skipped.append({"trace_id": trace_id, "reason": "already imported"})
            continue
        try:
            mapped = map_trace(spans, profile, runtime=conn.kind)
        except ValueError as exc:
            skipped.append({"trace_id": trace_id, "reason": f"could not be mapped: {str(exc)[:200]}"})
            continue
        ids = [s.step_id for s in mapped.trace.steps]
        missing = [s for s in expected if s not in ids]
        if missing:
            skipped.append({"trace_id": trace_id, "reason": f"steps {', '.join(missing)} of {conn.workflow_key} "
                                                            f"are missing (found {', '.join(ids[:8])})"})
            continue
        run = _store_import(session, conn, mapped)
        tiers = sorted({e.tier for e in mapped.lineage})
        imported.append({"trace_id": trace_id, "run_id": run.id, "findings": len(run.findings),
                         "lineage": tiers, "status": run.status})
    conn.last_sync_at, conn.last_error = datetime.now(UTC), ""
    audit(session, "analyst", "traces_imported", "connection", conn.id, imported=len(imported), skipped=len(skipped))
    return {"connection_id": conn.id, "fetched": len(traces), "imported": imported, "skipped": skipped}


def export_run(session: Session, settings: Settings, conn: Connection, run: Run) -> dict[str, Any]:
    """Send a run's trace to the platform as spans (idempotent) and remember the span of each step."""
    if run.trace is None:
        raise ProblemError(409, "Run has no trace yet", "Wait for the run to finish, then send it.")
    from granite_core.trace import TraceV1

    trace = TraceV1.model_validate(run.trace)
    spans = trace_to_spans(trace, run.id, {"seed": run.seed, "model": run.model, "mode": run.llm_mode,
                                           "fault": run.fault_type})
    client = client_for(conn, settings)
    try:
        if isinstance(client, PhoenixClient):
            client.ensure_project()
            sent = client.send(spans)
        else:
            sent = client.send(spans, trace_name=conn.project or run.workflow_key)
    except ConnectorError as exc:
        raise _platform_error(conn, exc) from None
    step_spans = {str(s.attributes["granite.step_id"]): s.span_id for s in spans[1:]}
    link = session.query(TraceLink).filter_by(connection_id=conn.id, run_id=run.id, direction="exported").first()
    if link is None:
        session.add(TraceLink(connection_id=conn.id, run_id=run.id, direction="exported",
                              external_trace_id=spans[0].trace_id, root_span_id=spans[0].span_id,
                              span_ids=step_spans))
    audit(session, "analyst", "run_exported", "run", run.id, connection=conn.id, spans=sent)
    return {"connection_id": conn.id, "run_id": run.id, "trace_id": spans[0].trace_id, "spans_sent": sent,
            "spans_total": len(spans)}


def _verdict(finding: Finding) -> tuple[str, str | None, str, dict[str, Any]]:
    """(label, origin step, explanation, metadata) of a finding as it stands now."""
    status = FindingStatus(finding.status)
    level = verification_level(status)
    confirmed = next((h for h in finding.hypotheses if h.status == "confirmed"), None)
    top = confirmed or (finding.hypotheses[0] if finding.hypotheses else None)
    exp = next((e for h in finding.hypotheses for e in reversed(h.experiments) if e.verdict), None)
    label = confirmed and "confirmed" or (exp.verdict if exp and exp.verdict else status.value)
    parts = [f"{finding.title}.", f"Status {status.value}, verification level {level}."]
    if top is not None:
        parts.append(f"{'Confirmed origin' if confirmed else 'Top suspect'}: {top.agent} ({top.step_id}).")
    if exp is not None and exp.summary:
        s = exp.summary
        parts.append(f"Replays with the fix passed {s.get('k_pass', '?')}/{s.get('n_completed', '?')}, "
                     f"controls {s.get('c_pass', '?')}/{s.get('m_completed', '?')} ({exp.rule_version}).")
    meta = {"granite_finding_id": finding.id, "level": level, "check": finding.check_id or "",
            "status": status.value}
    return label, top.step_id if top else None, " ".join(parts), meta


def write_back(session: Session, settings: Settings, finding: Finding) -> dict[str, Any]:
    """Write the finding's verdict to every platform its run is linked to (annotation on the origin step's span)."""
    links = session.query(TraceLink).filter_by(run_id=finding.run_id).all()
    if not links:
        raise ProblemError(409, "Run is not linked to a platform",
                           "Import the run from, or send it to, Phoenix or Langfuse first.")
    label, step, explanation, meta = _verdict(finding)
    written: list[dict[str, Any]] = []
    for link in links:
        conn = session.get(Connection, link.connection_id)
        assert conn is not None
        span = link.span_ids.get(step or "", "") or link.root_span_id
        client = client_for(conn, settings)
        try:
            if isinstance(client, PhoenixClient):
                ref = client.annotate(span, "granite.verdict", label=label, score=VERDICT_SCORE.get(label),
                                      explanation=explanation, metadata=meta)
            else:
                obs = span if span in link.span_ids.values() else None
                ref = client.score(link.external_trace_id, obs, "granite.verdict", label=label,
                                   comment=explanation, metadata=meta)
        except ConnectorError as exc:
            conn.last_error = str(exc)[:500]
            raise _platform_error(conn, exc) from None
        written.append({"connection_id": conn.id, "kind": conn.kind, "span_id": span, "ref": ref})
    audit(session, "analyst", "verdict_written_back", "finding", finding.id, label=label, targets=len(written))
    return {"finding_id": finding.id, "label": label, "step_id": step, "explanation": explanation,
            "written": written}


def links_of(session: Session, run_id: str) -> list[TraceLink]:
    """Platform links of a run."""
    return session.query(TraceLink).filter_by(run_id=run_id).order_by(TraceLink.id).all()


__all__ = ["KINDS", "MAX_IMPORT", "client_for", "create_connection", "export_run", "get_connection",
           "import_traces", "links_of", "test_connection", "write_back"]
