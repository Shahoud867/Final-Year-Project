"""Turn database rows into API response objects (derived fields live here, not in the tables)."""

from __future__ import annotations

from typing import Any

from granite_core.evidence import EvidenceRecord, EvidenceType, verify_evidence
from granite_core.lifecycle import Event, FindingStatus, allowed_events, verification_level
from granite_core.lineage import edges
from granite_core.trace import TASK, TraceV1, split_read
from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import Evidence, Finding, Run
from .registry import WORKFLOWS
from .schemas import (
    EvidenceOut,
    ExperimentOut,
    FaultOut,
    FindingDetail,
    FindingSummary,
    HypothesisOut,
    ReplayOut,
    ReviewOut,
    RunDetail,
    RunSummary,
)
from .services.reviews import AWAITING_REVIEW

USER_ACTIONS = {
    Event.VERIFY_STARTED: "verify",
    Event.REVIEW_ACCEPT: "accept",
    Event.REVIEW_REJECT: "reject",
    Event.RESOLVE: "resolve",
    Event.WONT_FIX: "wont_fix",
}


# Evidence reads in the order an investigation unfolds: the failed check, the symptom, the candidates, the experiment.
EVIDENCE_ORDER = [t.value for t in (
    EvidenceType.CHECK_COMPUTATION, EvidenceType.STEP_SNAPSHOT, EvidenceType.PROVENANCE_PATH,
    EvidenceType.VERDICT_COMPUTATION, EvidenceType.REPLAY_OUTPUT, EvidenceType.DIFF, EvidenceType.REVIEWER_NOTE,
)]


def evidence_sort_key(e: Evidence) -> tuple[int, str, str]:
    rank = EVIDENCE_ORDER.index(e.type) if e.type in EVIDENCE_ORDER else len(EVIDENCE_ORDER)
    return rank, e.created_at.isoformat(), e.title


def finding_summary(f: Finding) -> FindingSummary:
    out = FindingSummary.model_validate(f)
    out.verification_level = verification_level(FindingStatus(f.status))
    return out


def run_summary(session: Session, run: Run) -> RunSummary:
    out = RunSummary.model_validate(run)
    out.finding_count = len(run.findings)
    out.failed_checks = sum(1 for c in run.check_results if c.status == "fail")
    return out


def run_detail(run: Run) -> RunDetail:
    base = RunSummary.model_validate(run).model_dump()
    detail = RunDetail.model_validate(
        {
            **base,
            "trace": run.trace,
            "trace_sha256": run.trace_sha256,
            "check_results": run.check_results,
            "findings": [finding_summary(f) for f in run.findings],
            "injected_fault": FaultOut.model_validate(run.fault) if run.fault else None,
        },
        from_attributes=True,
    )
    detail.finding_count = len(run.findings)
    detail.failed_checks = sum(1 for c in run.check_results if c.status == "fail")
    return detail


def evidence_out(e: Evidence) -> EvidenceOut:
    out = EvidenceOut.model_validate(e)
    out.hash_valid = verify_evidence(
        EvidenceRecord(type=EvidenceType(e.type), payload=e.payload, sha256=e.sha256, reproduce=e.reproduce)
    )
    return out


def experiment_out(e: Any) -> ExperimentOut:
    out = ExperimentOut.model_validate(e)
    out.replays = [ReplayOut.model_validate(r) for r in e.replays]
    return out


def finding_detail(session: Session, f: Finding) -> FindingDetail:
    status = FindingStatus(f.status)
    actions = [USER_ACTIONS[ev] for ev in allowed_events(status) if ev in USER_ACTIONS]
    if f.status in AWAITING_REVIEW:
        actions.append("request_info")
    entry = WORKFLOWS[f.run.workflow_key]
    repairs = entry.build(f.run.model).repairs
    hypotheses = []
    for h in f.hypotheses:
        ho = HypothesisOut.model_validate(h)
        ho.can_verify = bool(repairs.get(h.step_id))
        hypotheses.append(ho)
    ev_rows = sorted(session.query(Evidence).filter(Evidence.finding_id == f.id), key=evidence_sort_key)
    experiments = [experiment_out(e) for h in f.hypotheses for e in h.experiments]
    return FindingDetail.model_validate(
        {
            **finding_summary(f).model_dump(),
            "detail": f.detail,
            "hypotheses": hypotheses,
            "experiments": experiments,
            "reviews": [ReviewOut.model_validate(r) for r in f.reviews],
            "evidence": [evidence_out(e) for e in ev_rows],
            "allowed_actions": actions,
        }
    )


def graph(run: Run) -> dict[str, Any]:
    """Nodes and data-flow edges of one run, with each node's check status for colouring."""
    if run.trace is None:
        return {"nodes": [], "edges": []}
    trace = TraceV1.model_validate(run.trace)
    failed_steps = {c.step for c in run.check_results if c.status == "fail"}
    symptoms = {f.symptom_step for f in run.findings}
    nodes: list[dict[str, Any]] = [{"id": TASK, "label": "Task input", "kind": "input", "status": "ok"}]
    for s in trace.steps:
        status = "error" if s.error else "failed" if s.step_id in failed_steps else "ok"
        nodes.append(
            {"id": s.step_id, "label": s.agent, "kind": s.kind, "status": status, "symptom": s.step_id in symptoms}
        )
    out_edges = [{"source": e.src, "target": e.dst, "field": e.field} for e in edges(trace)]
    for s in trace.steps:
        fields = [split_read(r)[1] for r in s.reads if split_read(r)[0] == TASK]
        if fields:
            out_edges.append({"source": TASK, "target": s.step_id, "field": ", ".join(fields)})
    return {"nodes": nodes, "edges": out_edges}


def count_by_status(session: Session) -> dict[str, int]:
    rows = session.query(Finding.status, func.count()).group_by(Finding.status).all()
    return {status: n for status, n in rows}
