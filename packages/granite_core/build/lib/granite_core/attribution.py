"""Deterministic value-provenance attribution (master plan 21.4; FR-ATT-01/02).

Question answered: *where did the wrong value originate*, as opposed to *where did it surface*?

Walk the data flow backwards from the step where the failed outcome check surfaced. Each step on the
way is classified from evidence that already exists in the run:

=================  ======  ====================================================================
evidence           weight  meaning
=================  ======  ====================================================================
truth_mismatch     1.0     the step's output contradicts a registered source of truth
contract_fail      0.8     the step violates its own contract (e.g. refund != sum of its inputs)
handoff_drift      0.7     what the step received differs from what its upstream step produced
unknown            0.2     no contract defined for the step: cannot be cleared or blamed
consistent         0.1     its contract passes: it faithfully propagated what it was given
=================  ======  ====================================================================

Nothing here calls an LLM, reads the fault-injection ground truth, or asks a model how confident it
is: the same trace and check results always give byte-identical hypotheses (NFR-05).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel

from .checks import CheckResult, CheckStatus
from .lineage import ancestors_with_distance, betweenness_fraction, edges
from .trace import TASK, Step, TraceV1, split_read

WEIGHTS: dict[str, float] = {
    "truth_mismatch": 1.0,
    "contract_fail": 0.8,
    "handoff_drift": 0.7,
    "unknown": 0.2,
    "consistent": 0.1,
}
ORIGIN_THRESHOLD = 0.7
DECAY = 0.9
MAX_HYPOTHESES = 5


class HypothesisSpec(BaseModel):
    rank: int
    step_id: str
    agent: str
    method: Literal["provenance", "structural"]
    evidence_kind: str
    score: float
    rationale: str
    evidence: list[dict[str, Any]]


def _same(a: Any, b: Any) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) < 1e-9
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b, strict=True))
    return bool(a == b)


def _drift(trace: TraceV1, step: Step) -> list[dict[str, Any]]:
    """Reads whose recorded input differs from the upstream step's recorded output."""
    found = []
    for ref in step.reads:
        if ref not in step.inputs:
            continue
        src, fld = split_read(ref)
        if src == TASK:
            upstream = trace.run.task_input.get(fld)
        else:
            up = trace.step(src)
            upstream = up.outputs.get(fld) if up else None
        if not _same(step.inputs[ref], upstream):
            found.append({"read": ref, "received": step.inputs[ref], "produced_upstream": upstream})
    return found


def _classify(trace: TraceV1, step: Step, step_results: list[CheckResult]) -> tuple[str, list[dict[str, Any]], str]:
    truth_fail = [r for r in step_results if r.status is CheckStatus.FAIL and r.type == "truth"]
    if truth_fail:
        r = truth_fail[0]
        why = (
            f"{step.agent}'s output contradicts the source of truth ({r.check_id}): "
            f"observed {r.observed!r}, expected {r.expected!r}."
        )
        return "truth_mismatch", [_ev(r)], why
    contract_fail = [r for r in step_results if r.status is CheckStatus.FAIL]
    if contract_fail:
        r = contract_fail[0]
        return (
            "contract_fail",
            [_ev(r)],
            (f"{step.agent} broke its own contract ({r.check_id}): observed {r.observed!r}, expected {r.expected!r}."),
        )
    drift = _drift(trace, step)
    if drift:
        return (
            "handoff_drift",
            [{"type": "handoff_drift", **d} for d in drift],
            (f"{step.agent} received a value different from what its upstream step produced ({drift[0]['read']})."),
        )
    if any(r.status is CheckStatus.PASS for r in step_results):
        ids = ", ".join(r.check_id for r in step_results if r.status is CheckStatus.PASS)
        return (
            "consistent",
            [_ev(r) for r in step_results if r.status is CheckStatus.PASS],
            (f"{step.agent} is consistent with its inputs ({ids} passed): it passed on what it was given."),
        )
    return "unknown", [], f"{step.agent} has no check, so it can neither be cleared nor blamed."


def _ev(r: CheckResult) -> dict[str, Any]:
    return {
        "type": "check",
        "check_id": r.check_id,
        "status": r.status.value,
        "observed": r.observed,
        "expected": r.expected,
        "computation": r.computation,
    }


def attribute(trace: TraceV1, results: list[CheckResult], symptom_step: str) -> list[HypothesisSpec]:
    """Rank origin hypotheses for a failure that surfaced at ``symptom_step``."""
    if trace.step(symptom_step) is None:
        return []
    dist, parent = ancestors_with_distance(trace, symptom_step)
    order = {s.step_id: i for i, s in enumerate(trace.steps)}
    rows = []
    for sid, d in dist.items():
        step = trace.step(sid)
        assert step is not None
        step_results = [r for r in results if r.scope == "step" and r.step == sid]
        kind, ev, why = _classify(trace, step, step_results)
        rows.append((sid, step, d, kind, ev, why))

    has_origin_evidence = any(WEIGHTS[k] >= ORIGIN_THRESHOLD for _, _, _, k, _, _ in rows)
    between = {} if has_origin_evidence else betweenness_fraction(trace, symptom_step)

    def structural(sid: str, kind: str) -> float:
        # position only, but a step whose own contract PASSED is cleared: it must never outrank an unchecked one
        return between.get(sid, 0.0) * min(1.0, WEIGHTS[kind] / WEIGHTS["unknown"])

    rows.sort(key=lambda r: (-WEIGHTS[r[3]] if has_origin_evidence else -structural(r[0], r[3]), order[r[0]]))

    out: list[HypothesisSpec] = []
    edge_fields = {(e.src, e.dst): e.field for e in edges(trace)}
    for rank, (sid, step, d, kind, ev, why) in enumerate(rows[:MAX_HYPOTHESES], start=1):
        if has_origin_evidence:
            score, method = round(min(1.0, WEIGHTS[kind] * DECAY**d), 3), "provenance"
        else:
            score, method = round(0.5 * structural(sid, kind), 3), "structural"
            why += " No step has direct evidence, so this suspect is ranked by position only: verify before trusting."
        path, cur = [], sid
        while True:
            path.append({"step_id": cur, "agent": trace.step(cur).agent if trace.step(cur) else cur})  # type: ignore[union-attr]
            if cur == symptom_step or cur not in parent:
                break
            nxt = parent[cur]
            path[-1]["carries"] = edge_fields.get((cur, nxt))
            cur = nxt
        out.append(
            HypothesisSpec(
                rank=rank,
                step_id=sid,
                agent=step.agent,
                method=method,
                evidence_kind=kind,
                score=score,
                rationale=why,
                evidence=[{"type": "provenance_path", "from": sid, "to": symptom_step, "path": path}, *ev],
            )
        )
    return out
