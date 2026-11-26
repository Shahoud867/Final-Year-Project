"""A plain-text investigation report for one finding (Markdown), built only from stored records."""

from __future__ import annotations

from granite_core.lifecycle import FindingStatus, verification_level
from sqlalchemy.orm import Session

from ..models import Evidence, Finding

LEVELS = {
    "V0": "detected by a check, not yet reproduced",
    "V1": "supported by evidence (provenance), not replay-verified",
    "V2": "verified by controlled replays",
    "V3": "confirmed by a human reviewer",
}


def finding_report(session: Session, f: Finding) -> str:
    """Render the investigation of one finding as Markdown from stored records."""
    level = verification_level(FindingStatus(f.status))
    run = f.run
    lines = [
        f"# Finding {f.id}: {f.title}",
        "",
        f"- Status: **{f.status}** (verification level {level}: {LEVELS[level]})",
        f"- Severity: {f.severity}; kind: {f.kind.replace('_', ' ')}; failed check: {f.check_id or 'none'}",
        f"- Run: {run.id} ({run.workflow_key}, {run.llm_mode} mode, model {run.model}, seed {run.seed})",
        f"- Trace SHA-256: {run.trace_sha256}",
        f"- Task: {run.task_input.get('message', '')}",
        "",
        "## Origin hypotheses",
        "",
        "| Rank | Step | Method | Evidence | Score | Status |",
        "|---|---|---|---|---|---|",
    ]
    for h in f.hypotheses:
        lines.append(
            f"| {h.rank} | {h.agent} ({h.step_id}) | {h.method} | {h.evidence_kind} | {h.score:.2f} | {h.status} |"
        )
    for h in f.hypotheses:
        lines += ["", f"- Hypothesis {h.rank} ({h.agent}): {h.rationale}"]
    lines += ["", "## Verification experiments", ""]
    experiments = [e for h in f.hypotheses for e in h.experiments]
    if not experiments:
        lines.append("None run yet.")
    for e in experiments:
        s = e.summary or {}
        lines.append(
            f"- {e.id}: rule {e.rule_version}, {e.n} replays with the fix and {e.m} controls without it. "
            f"Verdict **{e.verdict or e.status}**. "
            + (f"{s.get('k_pass')}/{s.get('n_completed')} replays correct (95% CI "
               f"{s.get('ci_low')}-{s.get('ci_high')}), {s.get('c_pass')}/{s.get('m_completed')} controls correct. "
               f"{s.get('explanation', '')}" if s else e.error)
        )
    lines += ["", "## Review history", ""]
    lines += [
        f"- {r.created_at:%Y-%m-%d %H:%M} {r.reviewer}: {r.decision} ({r.from_status} to {r.to_status}). {r.comment}"
        for r in f.reviews
    ] or ["No review yet."]
    lines += ["", "## Evidence (SHA-256 of canonical JSON)", ""]
    ev = session.query(Evidence).filter(Evidence.finding_id == f.id).order_by(Evidence.created_at, Evidence.id).all()
    lines += [f"- {e.id} [{e.type}] {e.title}: {e.sha256}" for e in ev]
    return "\n".join(lines) + "\n"
