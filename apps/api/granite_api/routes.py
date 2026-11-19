"""HTTP endpoints. Handlers stay thin: validation here, behaviour in services."""

from __future__ import annotations

import secrets
from collections.abc import Iterator
from datetime import datetime
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from granite_core.lifecycle import FindingStatus, verification_level
from granite_core.llm import LLMRequest
from sqlalchemy import String, cast, func, text
from sqlalchemy.orm import Session

from . import __version__
from .config import Settings
from .db import session_scope
from .errors import ProblemError
from .jobs import JobRunner
from .llm_factory import build_provider, live_available, resolve_mode
from .models import Batch, Connection, Evidence, Experiment, Finding, Investigation, Job, Run, TraceLink
from .registry import WORKFLOWS
from .schemas import (
    Accepted,
    BatchCreate,
    BatchOut,
    ConnectionCreate,
    ConnectionOut,
    EvidenceOut,
    ExperimentCreate,
    ExperimentOut,
    ExportRequest,
    FindingDetail,
    FindingSummary,
    ImportRequest,
    InvestigationCreate,
    InvestigationOut,
    JobOut,
    ReviewCreate,
    ReviewOut,
    RunCreate,
    RunDetail,
    RunSummary,
    TraceLinkOut,
)
from .services import batches as batch_service
from .services import connections as con_service
from .services import evaluations as eval_service
from .services import experiments as exp_service
from .services import investigations as inv_service
from .services import reviews as review_service
from .services import runs as run_service
from .services.regression import regression_zip
from .services.report import finding_report
from .views import (
    batch_out,
    count_by_status,
    evidence_out,
    experiment_out,
    finding_detail,
    finding_summary,
    graph,
    investigation_out,
    run_detail,
    run_summary,
)


def get_settings(request: Request) -> Settings:
    """The application's settings."""
    settings: Settings = request.app.state.settings
    return settings


def get_runner(request: Request) -> JobRunner:
    """The application's job runner."""
    runner: JobRunner = request.app.state.runner
    return runner


def get_session(request: Request) -> Iterator[Session]:
    """A database session for one request."""
    with session_scope(request.app.state.session_factory) as session:
        yield session


def require_token(
    settings: Annotated[Settings, Depends(get_settings)], authorization: Annotated[str | None, Header()] = None
) -> None:
    """Refuse the request unless it carries the configured access token (when one is configured)."""
    if not settings.api_token:
        return
    supplied = (authorization or "").removeprefix("Bearer ").strip()
    if not secrets.compare_digest(supplied.encode(), settings.api_token.encode()):  # bytes: str raises on non-ASCII
        raise ProblemError(401, "Authentication required", "Send the access token in an Authorization Bearer header.")


Db = Annotated[Session, Depends(get_session)]
Cfg = Annotated[Settings, Depends(get_settings)]
Jobs = Annotated[JobRunner, Depends(get_runner)]
public = APIRouter(prefix="/api")
router = APIRouter(prefix="/api", dependencies=[Depends(require_token)])


@public.get("/health", tags=["system"])
def health(request: Request, settings: Cfg) -> dict[str, Any]:
    """Report that the server and database are up, and whether a live model is reachable."""
    with session_scope(request.app.state.session_factory) as s:
        s.execute(text("select 1"))
    return {
        "status": "ok",
        "version": __version__,
        "llm_mode": settings.llm_mode,
        "live_model_reachable": live_available(settings),
        "auth_required": bool(settings.api_token),
    }


@router.get("/workflows", tags=["workflows"])
def list_workflows(settings: Cfg) -> list[dict[str, Any]]:
    """List the workflows that can be run, with their steps, checks and available faults."""
    out = []
    for e in WORKFLOWS.values():
        defn = e.build(settings.model)
        out.append(
            {
                "key": e.key, "title": e.title, "description": e.description, "faults": list(e.fault_types),
                "steps": [{"id": s.step_id, "agent": s.agent, "kind": s.kind, "name": s.name} for s in defn.steps],
                "checks": [{"id": c.id, "name": c.name, "scope": c.scope, "step": c.step} for c in defn.checks],
            }
        )
    return out


@router.get("/workflows/{key}/examples", tags=["workflows"])
def examples(key: str) -> list[dict[str, Any]]:
    """Ready-to-run example tasks for a workflow."""
    return run_service.entry_for(key).examples()


@router.post("/runs", status_code=202, tags=["runs"])
def create_run(body: RunCreate, db: Db, settings: Cfg, jobs: Jobs) -> Accepted:
    """Start a run of a workflow on a task, optionally with an injected fault. Returns a job to poll."""
    run = run_service.create_run(db, settings, body.workflow, body.task_input, body.fault, body.seed, body.mode)
    db.commit()
    job_id = jobs.submit("run", run.id, run_service.run_job(jobs.factory, settings, run.id))
    return Accepted(job_id=job_id, run_id=run.id)


PAGE = 25  # FR-HIS-01: paginated, 25 per page by default


@router.get("/runs", tags=["runs"])
def list_runs(
    db: Db,
    status: str | None = None,
    fault: str | None = Query(default=None, description="a fault name, or 'none' for clean runs"),
    q: Annotated[str | None, Query(max_length=100, description="text in the task")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = PAGE,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[RunSummary]:
    """List runs, newest first, optionally filtered by status, fault or text in the task."""
    query = db.query(Run).order_by(Run.created_at.desc())
    if status:
        query = query.filter(Run.status == status)
    if fault:
        query = query.filter(Run.fault_type.is_(None) if fault == "none" else Run.fault_type == fault)
    if q:
        query = query.filter(func.lower(cast(Run.task_input, String)).contains(q.lower()))
    return [run_summary(db, r) for r in query.offset(offset).limit(limit).all()]


def _run(db: Session, run_id: str) -> Run:
    run = db.get(Run, run_id)
    if run is None:
        raise ProblemError(404, "Run not found", f"There is no run {run_id}.")
    return run


@router.get("/runs/{run_id}", tags=["runs"])
def get_run(run_id: str, db: Db) -> RunDetail:
    """A run with its trace, check results, findings and (for evaluation only) the injected fault."""
    return run_detail(_run(db, run_id))


@router.get("/runs/{run_id}/graph", tags=["runs"])
def get_graph(run_id: str, db: Db) -> dict[str, Any]:
    """The run as a graph: steps, data-flow edges and each step's check status."""
    return graph(_run(db, run_id))


@router.get("/findings", tags=["findings"])
def list_findings(
    db: Db,
    status: str | None = None,
    severity: Literal["critical", "high", "medium", "low"] | None = None,
    level: Annotated[Literal["V0", "V1", "V2", "V3"] | None, Query(description="verification level")] = None,
    run_id: str | None = None,
    q: Annotated[str | None, Query(max_length=100, description="text in the title")] = None,
    created_after: datetime | None = None,
    created_before: datetime | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = PAGE,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[FindingSummary]:
    """List findings, newest first, filtered by status, severity, level, run, text or date."""
    query = db.query(Finding).order_by(Finding.created_at.desc())
    if status:
        query = query.filter(Finding.status == status)
    if severity:
        query = query.filter(Finding.severity == severity)
    if level:
        query = query.filter(Finding.status.in_([s.value for s in FindingStatus if verification_level(s) == level]))
    if run_id:
        query = query.filter(Finding.run_id == run_id)
    if q:
        query = query.filter(func.lower(Finding.title).contains(q.lower()))
    if created_after:
        query = query.filter(Finding.created_at >= created_after)
    if created_before:
        query = query.filter(Finding.created_at <= created_before)
    return [finding_summary(f) for f in query.offset(offset).limit(limit).all()]


def _finding(db: Session, finding_id: str) -> Finding:
    finding = db.get(Finding, finding_id)
    if finding is None:
        raise ProblemError(404, "Finding not found", f"There is no finding {finding_id}.")
    return finding


@router.get("/findings/summary", tags=["findings"])
def findings_summary(db: Db) -> dict[str, int]:
    """Number of findings in each status."""
    return count_by_status(db)


@router.get("/findings/{finding_id}", tags=["findings"])
def get_finding(finding_id: str, db: Db) -> FindingDetail:
    """A finding with its hypotheses, experiments, reviews, evidence and the actions allowed now."""
    return finding_detail(db, _finding(db, finding_id))


@router.get("/findings/{finding_id}/report", tags=["findings"], response_model=None)
def get_report(finding_id: str, db: Db, format: Literal["md", "json"] = "md") -> Response:
    """The investigation as a document: Markdown for people, JSON (with evidence hashes) for tools."""
    finding = _finding(db, finding_id)
    if format == "md":
        return PlainTextResponse(finding_report(db, finding), media_type="text/markdown; charset=utf-8")
    run = finding.run
    body = {
        "finding": finding_detail(db, finding).model_dump(mode="json"),
        "run": {"id": run.id, "workflow": run.workflow_key, "mode": run.llm_mode, "model": run.model, "seed": run.seed,
                "task_input": run.task_input, "trace_sha256": run.trace_sha256},
    }
    return JSONResponse(body)


@router.post("/hypotheses/{hypothesis_id}/experiments", status_code=202, tags=["verification"])
def start_experiment(hypothesis_id: str, body: ExperimentCreate, db: Db, settings: Cfg, jobs: Jobs) -> Accepted:
    """Verify a hypothesis with N replays that apply the fix and M controls. Returns a job to poll."""
    exp = exp_service.create_experiment(db, settings, hypothesis_id, body.n, body.m, body.mode, "analyst")
    db.commit()
    job_id = jobs.submit("experiment", exp.id, exp_service.experiment_job(jobs.factory, settings, exp.id))
    return Accepted(job_id=job_id, experiment_id=exp.id)


@router.post("/findings/{finding_id}/investigations", status_code=202, tags=["verification"])
def start_investigation(finding_id: str, body: InvestigationCreate, db: Db, settings: Cfg, jobs: Jobs) -> Accepted:
    """Verify the ranked suspects in order until one is confirmed or the replay budget is spent. Returns a job."""
    inv = inv_service.create_investigation(db, settings, finding_id, body.n, body.m, body.budget, body.mode, "analyst")
    db.commit()
    job_id = jobs.submit("investigation", inv.id, inv_service.investigation_job(jobs.factory, settings, inv.id))
    return Accepted(job_id=job_id, investigation_id=inv.id)


@router.get("/investigations/{investigation_id}", tags=["verification"])
def get_investigation(investigation_id: str, db: Db) -> InvestigationOut:
    """An investigation with its attempts so far."""
    inv = db.get(Investigation, investigation_id)
    if inv is None:
        raise ProblemError(404, "Investigation not found", f"There is no investigation {investigation_id}.")
    return investigation_out(inv)


@router.get("/findings/{finding_id}/regression", tags=["findings"], response_model=None)
def get_regression(finding_id: str, db: Db) -> Response:
    """A regression test for a confirmed finding: a zip with the case JSON, a pytest module and a README."""
    name, body = regression_zip(_finding(db, finding_id))
    disposition = {"Content-Disposition": f'attachment; filename="{name}"'}
    return Response(body, media_type="application/zip", headers=disposition)


@router.post("/batches", status_code=202, tags=["fault lab"])
def create_batch(body: BatchCreate, db: Db, settings: Cfg, jobs: Jobs) -> Accepted:
    """Generate one run per chosen fault (or clean) on each chosen example task. Returns a job to poll."""
    batch = batch_service.create_batch(db, settings, body.workflow, body.faults, body.task_ids, body.seed, body.mode)
    db.commit()
    job_id = jobs.submit("batch", batch.id, batch_service.batch_job(jobs.factory, settings, batch.id))
    return Accepted(job_id=job_id, batch_id=batch.id)


@router.get("/batches", tags=["fault lab"])
def list_batches(db: Db, limit: Annotated[int, Query(ge=1, le=50)] = 10) -> list[BatchOut]:
    """Recent batches, newest first, with their per-condition counts."""
    return [batch_out(db, b) for b in db.query(Batch).order_by(Batch.created_at.desc()).limit(limit)]


@router.get("/batches/{batch_id}", tags=["fault lab"])
def get_batch(batch_id: str, db: Db) -> BatchOut:
    """A batch with its runs and per-condition counts (detected, errored, false alarms on clean runs)."""
    batch = db.get(Batch, batch_id)
    if batch is None:
        raise ProblemError(404, "Batch not found", f"There is no batch {batch_id}.")
    return batch_out(db, batch)


@router.get("/evaluations", tags=["evaluation"])
def list_evaluations(settings: Cfg) -> list[dict[str, Any]]:
    """Benchmark results written by the evaluation harness, newest first (read-only)."""
    return eval_service.list_evaluations(settings.eval_dir)


@router.get("/evaluations/{evaluation_id}", tags=["evaluation"])
def get_evaluation(evaluation_id: str, settings: Cfg) -> dict[str, Any]:
    """One benchmark result in full: protocol, metrics with intervals, and every run."""
    return eval_service.get_evaluation(settings.eval_dir, evaluation_id)


@router.get("/experiments/{experiment_id}", tags=["verification"])
def get_experiment(experiment_id: str, db: Db) -> ExperimentOut:
    """An experiment with its replays, summary and verdict."""
    exp = db.get(Experiment, experiment_id)
    if exp is None:
        raise ProblemError(404, "Experiment not found", f"There is no experiment {experiment_id}.")
    return experiment_out(exp)


@router.post("/findings/{finding_id}/reviews", status_code=201, tags=["findings"])
def post_review(finding_id: str, body: ReviewCreate, db: Db) -> ReviewOut:
    """Record a decision on a finding: accept, reject, resolve, close, or ask for information."""
    review = review_service.apply_review(db, finding_id, body.decision, body.comment, body.reviewer)
    db.commit()  # before responding: the dependency's own commit runs after the response is sent
    return ReviewOut.model_validate(review)


@router.get("/evidence/{evidence_id}", tags=["evidence"])
def get_evidence(evidence_id: str, db: Db) -> EvidenceOut:
    """One evidence record; ``hash_valid`` is false if its content no longer matches its hash."""
    ev = db.get(Evidence, evidence_id)
    if ev is None:
        raise ProblemError(404, "Evidence not found", f"There is no evidence record {evidence_id}.")
    return evidence_out(ev)


@router.get("/jobs/{job_id}", tags=["jobs"])
def get_job(job_id: str, db: Db) -> JobOut:
    """Status and progress of a background job."""
    job = db.get(Job, job_id)
    if job is None:
        raise ProblemError(404, "Job not found", f"There is no job {job_id}.")
    return JobOut.model_validate(job)


@router.post("/settings/test-llm", tags=["system"])
def test_llm(settings: Cfg) -> dict[str, Any]:
    """One tiny request to the configured model, so a user can tell a setup problem from a workflow problem."""
    mode = resolve_mode(settings)
    if mode == "recorded":
        return {"ok": True, "mode": "recorded", "message": "Recorded mode: saved answers are used, no model needed."}
    ping = LLMRequest(
        messages=[{"role": "user", "content": "Reply with the single word ok"}],
        model=settings.model, max_tokens=8, temperature=0.0,
    )
    try:
        out = build_provider(settings, "live").complete(ping)
    except Exception as exc:
        return {"ok": False, "mode": "live", "message": str(exc)}
    return {"ok": True, "mode": "live", "message": f"{settings.model} answered in {out.latency_ms} ms."}


# ---- integrations: Arize Phoenix and Langfuse (F13, ADR-012) -------------------------------------------------------
def _connection_out(db: Session, settings: Settings, conn: Connection) -> ConnectionOut:
    out = ConnectionOut.model_validate(conn)
    links = db.query(TraceLink).filter_by(connection_id=conn.id).all()
    out.imported_runs = sum(1 for link in links if link.direction == "imported")
    out.exported_runs = sum(1 for link in links if link.direction == "exported")
    out.keys_configured = conn.kind == "phoenix" or bool(settings.langfuse_public_key and settings.langfuse_secret_key)
    return out


@router.get("/connections", tags=["integrations"])
def list_connections(db: Db, settings: Cfg) -> list[ConnectionOut]:
    """Connected Phoenix and Langfuse projects, newest first."""
    rows = db.query(Connection).order_by(Connection.created_at.desc()).all()
    return [_connection_out(db, settings, c) for c in rows]


@router.post("/connections", status_code=201, tags=["integrations"])
def create_connection(body: ConnectionCreate, db: Db, settings: Cfg) -> ConnectionOut:
    """Add a Phoenix or Langfuse project. Only the URL and names are stored; keys stay in the server environment."""
    conn = con_service.create_connection(db, body.kind, body.name, body.base_url, body.project, body.workflow,
                                         body.steps)
    db.commit()
    return _connection_out(db, settings, conn)


@router.post("/connections/{connection_id}/test", tags=["integrations"])
def test_connection(connection_id: str, db: Db, settings: Cfg) -> dict[str, Any]:
    """Reach the platform with the configured keys and report what it said."""
    return con_service.test_connection(con_service.get_connection(db, connection_id), settings)


@router.post("/connections/{connection_id}/import", tags=["integrations"])
def import_traces(connection_id: str, body: ImportRequest, db: Db, settings: Cfg) -> dict[str, Any]:
    """Import the newest traces not imported before, run the workflow's checks on them and open findings."""
    conn = con_service.get_connection(db, connection_id)
    result = con_service.import_traces(db, settings, conn, body.limit)
    db.commit()
    return result


@router.post("/runs/{run_id}/export", tags=["integrations"])
def export_run(run_id: str, body: ExportRequest, db: Db, settings: Cfg) -> dict[str, Any]:
    """Send a run to a connected platform as spans, so it can be seen there next to the team's other traces."""
    result = con_service.export_run(db, settings, con_service.get_connection(db, body.connection_id), _run(db, run_id))
    db.commit()
    return result


@router.get("/runs/{run_id}/links", tags=["integrations"])
def run_links(run_id: str, db: Db) -> list[TraceLinkOut]:
    """Platforms this run was imported from or sent to, with the span id of each step."""
    _run(db, run_id)
    return [TraceLinkOut.model_validate(link) for link in con_service.links_of(db, run_id)]


@router.post("/findings/{finding_id}/writeback", tags=["integrations"])
def write_back(finding_id: str, db: Db, settings: Cfg) -> dict[str, Any]:
    """Write the finding's verdict to the linked platforms: a span annotation (Phoenix) or a score (Langfuse)."""
    result = con_service.write_back(db, settings, _finding(db, finding_id))
    db.commit()
    return result
