"""After a run: persist the trace, run the checks, open findings, rank origin hypotheses, record evidence."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from granite_core.attribution import attribute
from granite_core.checks import CheckResult, FindingSpec, derive_findings, evaluate_checks
from granite_core.evidence import EvidenceType, sha256_of
from granite_core.lifecycle import Event
from granite_core.runner import FaultRecord, RunOutcome, WorkflowDef
from granite_core.trace import TraceV1
from sqlalchemy.orm import Session

from ..models import CheckResultRow, FaultInjection, Finding, Hypothesis, Run, new_id
from .common import add_evidence, audit, move


def _result_row(run_id: str, r: CheckResult) -> CheckResultRow:
    return CheckResultRow(
        run_id=run_id, check_id=r.check_id, check_version=r.check_version, scope=r.scope, step=r.step, type=r.type,
        severity=r.severity, status=r.status.value, observed=r.observed, expected=r.expected, message=r.message,
        computation=r.computation,
    )


def _open_finding(
    session: Session, run: Run, defn: WorkflowDef, trace: TraceV1, results: list[CheckResult], spec: FindingSpec
) -> Finding:
    finding = Finding(
        id=new_id("fnd"), run_id=run.id, kind=spec.kind, severity=spec.severity, title=spec.title,
        detail=spec.detail, check_id=spec.check_id, symptom_step=spec.symptom_step,
    )
    session.add(finding)
    session.flush()
    audit(session, "system", "finding_opened", "finding", finding.id, check_id=spec.check_id, run_id=run.id)

    failing = next((r for r in results if r.check_id == spec.check_id), None)
    if failing is not None:
        add_evidence(
            session, run.id, finding.id, EvidenceType.CHECK_COMPUTATION, f"Check {failing.check_id} computation",
            {**failing.model_dump(mode="json"), "data_snapshot": defn.data_snapshot},
            reproduce=f"Re-evaluate check {failing.check_id} on run {run.id}; data snapshot {defn.data_snapshot}",
        )
    step = trace.step(spec.symptom_step)
    if step is not None:
        add_evidence(
            session, run.id, finding.id, EvidenceType.STEP_SNAPSHOT, f"Step {step.step_id} ({step.agent}) snapshot",
            {"step_id": step.step_id, "agent": step.agent, "inputs": step.inputs, "outputs": step.outputs,
             "error": step.error},
        )

    hypotheses = attribute(trace, results, spec.symptom_step)
    for h in hypotheses:
        session.add(Hypothesis(
            id=new_id("hyp"), finding_id=finding.id, rank=h.rank, step_id=h.step_id, agent=h.agent, method=h.method,
            evidence_kind=h.evidence_kind, score=h.score, rationale=h.rationale, evidence=h.evidence,
        ))
        add_evidence(
            session, run.id, finding.id, EvidenceType.PROVENANCE_PATH,
            f"Hypothesis {h.rank}: {h.agent} ({h.method})", h.model_dump(mode="json"),
            reproduce="Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
        )
    if hypotheses:
        move(session, finding, Event.HYPOTHESES_READY)
        top = hypotheses[0]
        if top.method == "provenance" and not defn.repairs.get(top.step_id):
            move(session, finding, Event.EVIDENCE_SUPPORTED)  # strong provenance evidence, but no replay is defined
    return finding


def _store_fault(run: Run, fault: FaultRecord | None) -> None:
    if fault is None:
        return
    run.fault = FaultInjection(
        run_id=run.id, fault_type=fault.fault_type, target_step=fault.target_step, field_path=fault.field_path,
        original_value=fault.original_value, injected_value=fault.injected_value, note=fault.note,
    )


def persist_outcome(session: Session, run: Run, defn: WorkflowDef, outcome: RunOutcome) -> list[Finding]:
    trace = outcome.trace
    doc: dict[str, Any] = trace.model_dump(mode="json")
    run.trace, run.trace_sha256 = doc, sha256_of(doc)
    run.status = trace.run.status
    run.finished_at = datetime.now(UTC)
    bad = next((s for s in trace.steps if s.error), None)
    run.error = f"{bad.agent}: {bad.error}" if bad else ""
    _store_fault(run, outcome.fault)

    results = evaluate_checks(trace, defn.checks, defn.truth())
    run.check_results = [_result_row(run.id, r) for r in results]
    session.flush()
    findings = [_open_finding(session, run, defn, trace, results, spec) for spec in derive_findings(trace, results)]
    audit(session, "system", "run_finished", "run", run.id, status=run.status, findings=len(findings))
    return findings
