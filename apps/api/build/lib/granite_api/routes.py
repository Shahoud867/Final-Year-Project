"""HTTP endpoints. Handlers stay thin: validation here, behaviour in services."""

from __future__ import annotations

import secrets
from collections.abc import Iterator
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import PlainTextResponse
from granite_core.llm import LLMRequest
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import __version__
from .config import Settings
from .db import session_scope
from .errors import ProblemError
from .jobs import JobRunner
from .llm_factory import build_provider, live_available, resolve_mode
from .models import Evidence, Experiment, Finding, Job, Run
from .registry import WORKFLOWS
from .schemas import (
    Accepted,
    EvidenceOut,
    ExperimentCreate,
    ExperimentOut,
    FindingDetail,
    FindingSummary,
    JobOut,
    ReviewCreate,
    ReviewOut,
    RunCreate,
    RunDetail,
    RunSummary,
)
from .services import experiments as exp_service
from .services import reviews as review_service
from .services import runs as run_service
from .services.report import finding_report
from .views import (
    count_by_status,
    evidence_out,
    experiment_out,
    finding_detail,
    finding_summary,
    graph,
    run_detail,
    run_summary,
)


def get_settings(request: Request) -> Settings:
    settings: Settings = request.app.state.settings
    return settings


def get_runner(request: Request) -> JobRunner:
    runner: JobRunner = request.app.state.runner
    return runner


def get_session(request: Request) -> Iterator[Session]:
    with session_scope(request.app.state.session_factory) as session:
        yield session


def require_token(
    settings: Annotated[Settings, Depends(get_settings)], authorization: Annotated[str | None, Header()] = None
) -> None:
    if not settings.api_token:
        return
    supplied = (authorization or "").removeprefix("Bearer ").strip()
    if not secrets.compare_digest(supplied, settings.api_token):
        raise ProblemError(401, "Authentication required", "Send the access token in an Authorization Bearer header.")


Db = Annotated[Session, Depends(get_session)]
Cfg = Annotated[Settings, Depends(get_settings)]
Jobs = Annotated[JobRunner, Depends(get_runner)]
public = APIRouter(prefix="/api")
router = APIRouter(prefix="/api", dependencies=[Depends(require_token)])


@public.get("/health", tags=["system"])
def health(request: Request, settings: Cfg) -> dict[str, Any]:
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
    return run_service.entry_for(key).examples()


@router.post("/runs", status_code=202, tags=["runs"])
def create_run(body: RunCreate, db: Db, settings: Cfg, jobs: Jobs) -> Accepted:
    run = run_service.create_run(db, settings, body.workflow, body.task_input, body.fault, body.seed, body.mode)
    db.commit()
    job_id = jobs.submit("run", run.id, run_service.run_job(jobs.factory, settings, run.id))
    return Accepted(job_id=job_id, run_id=run.id)


@router.get("/runs", tags=["runs"])
def list_runs(
    db: Db,
    status: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[RunSummary]:
    query = db.query(Run).order_by(Run.created_at.desc())
    if status:
        query = query.filter(Run.status == status)
    return [run_summary(db, r) for r in query.offset(offset).limit(limit).all()]


def _run(db: Session, run_id: str) -> Run:
    run = db.get(Run, run_id)
    if run is None:
        raise ProblemError(404, "Run not found", f"There is no run {run_id}.")
    return run


@router.get("/runs/{run_id}", tags=["runs"])
def get_run(run_id: str, db: Db) -> RunDetail:
    return run_detail(_run(db, run_id))


@router.get("/runs/{run_id}/graph", tags=["runs"])
def get_graph(run_id: str, db: Db) -> dict[str, Any]:
    return graph(_run(db, run_id))


@router.get("/findings", tags=["findings"])
def list_findings(
    db: Db,
    status: str | None = None,
    run_id: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[FindingSummary]:
    query = db.query(Finding).order_by(Finding.created_at.desc())
    if status:
        query = query.filter(Finding.status == status)
    if run_id:
        query = query.filter(Finding.run_id == run_id)
    return [finding_summary(f) for f in query.offset(offset).limit(limit).all()]


def _finding(db: Session, finding_id: str) -> Finding:
    finding = db.get(Finding, finding_id)
    if finding is None:
        raise ProblemError(404, "Finding not found", f"There is no finding {finding_id}.")
    return finding


@router.get("/findings/summary", tags=["findings"])
def findings_summary(db: Db) -> dict[str, int]:
    return count_by_status(db)


@router.get("/findings/{finding_id}", tags=["findings"])
def get_finding(finding_id: str, db: Db) -> FindingDetail:
    return finding_detail(db, _finding(db, finding_id))


@router.get("/findings/{finding_id}/report", tags=["findings"], response_class=PlainTextResponse)
def get_report(finding_id: str, db: Db) -> PlainTextResponse:
    return PlainTextResponse(finding_report(db, _finding(db, finding_id)), media_type="text/markdown; charset=utf-8")


@router.post("/hypotheses/{hypothesis_id}/experiments", status_code=202, tags=["verification"])
def start_experiment(hypothesis_id: str, body: ExperimentCreate, db: Db, settings: Cfg, jobs: Jobs) -> Accepted:
    exp = exp_service.create_experiment(db, settings, hypothesis_id, body.n, body.m, body.mode, "analyst")
    db.commit()
    job_id = jobs.submit("experiment", exp.id, exp_service.experiment_job(jobs.factory, settings, exp.id))
    return Accepted(job_id=job_id, experiment_id=exp.id)


@router.get("/experiments/{experiment_id}", tags=["verification"])
def get_experiment(experiment_id: str, db: Db) -> ExperimentOut:
    exp = db.get(Experiment, experiment_id)
    if exp is None:
        raise ProblemError(404, "Experiment not found", f"There is no experiment {experiment_id}.")
    return experiment_out(exp)


@router.post("/findings/{finding_id}/reviews", status_code=201, tags=["findings"])
def post_review(finding_id: str, body: ReviewCreate, db: Db) -> ReviewOut:
    review = review_service.apply_review(db, finding_id, body.decision, body.comment, body.reviewer)
    return ReviewOut.model_validate(review)


@router.get("/evidence/{evidence_id}", tags=["evidence"])
def get_evidence(evidence_id: str, db: Db) -> EvidenceOut:
    ev = db.get(Evidence, evidence_id)
    if ev is None:
        raise ProblemError(404, "Evidence not found", f"There is no evidence record {evidence_id}.")
    return evidence_out(ev)


@router.get("/jobs/{job_id}", tags=["jobs"])
def get_job(job_id: str, db: Db) -> JobOut:
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
