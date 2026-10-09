"""Controlled-replay verification, protocol VR-1 (master plan 14.4 and 21.5; FR-VER-01..04).

A hypothesis ("step X is the origin") is tested by re-executing the workflow *after* X:

1. steps up to and including X are frozen (their recorded outputs are reused, no LLM call);
2. X's output is patched with the value its own contract / the source of truth says is correct;
3. everything after X runs again, N times with the intervention and M times *without* it (controls).

The controls matter: without them a lucky re-run proves nothing, because an LLM can answer
differently every time. A hypothesis is only CONFIRMED when the intervention flips the outcome
reliably **and** the unpatched controls do not.

The thresholds below are pre-registered (``VR-1``). A change makes a new version; it never rewrites
the verdicts already stored under the old one.
"""

from __future__ import annotations

import copy
import math
from collections.abc import Callable, Mapping
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field

from .checks import CheckResult, CheckStatus
from .dsl import DSLError, compile_expression
from .trace import TraceV1

RULE_VERSION = "VR-1"
CONFIRM_MIN_RATE = 0.8  # k/N at or above this ...
CONTROL_MAX_RATE = 0.2  # ... with controls at or below this -> CONFIRMED
REFUTE_MAX_RATE = 0.2  # k/N at or below this -> REFUTED
MAX_REPLAYS = 10
MAX_CONTROLS = 5


class Verdict(StrEnum):
    CONFIRMED = "confirmed"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"
    ERROR = "error"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for k successes in n trials (reported with every verdict)."""
    if n <= 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def decide(
    k: int, n: int, c: int, m: int, completed: int | None = None, completed_controls: int | None = None
) -> Verdict:
    """VR-1. ``k`` of ``n`` intervention replays passed; ``c`` of ``m`` control replays passed."""
    if n < 1:
        raise ValueError("n must be at least 1")
    done = n if completed is None else completed
    done_c = m if completed_controls is None else completed_controls
    if done < n or done_c < m:
        return Verdict.ERROR
    p = k / n
    q = c / m if m > 0 else 0.0
    if p >= CONFIRM_MIN_RATE and q <= CONTROL_MAX_RATE:
        return Verdict.CONFIRMED
    if p <= REFUTE_MAX_RATE:
        return Verdict.REFUTED
    return Verdict.INCONCLUSIVE


# ---- interventions ------------------------------------------------------------------------------


class RepairRule(BaseModel):
    """How to compute the correct value of one output field of a step (workflow-defined)."""

    field: str
    expression: str


class Intervention(BaseModel):
    step_id: str
    patches: dict[str, Any] = Field(min_length=1)  # a single atomic field per patch (Spike 8 lesson)
    source: Literal["truth", "contract", "user"]
    description: str = ""


def build_intervention(
    trace: TraceV1,
    step_id: str,
    rules: list[RepairRule],
    truth: Mapping[str, Callable[..., Any]] | None = None,
) -> Intervention | None:
    """Evaluate the workflow's repair rules for ``step_id``. ``None`` if no rule produces a value."""
    patches: dict[str, Any] = {}
    for rule in rules:
        try:
            patches[rule.field] = compile_expression(rule.expression).evaluate(trace.context(), truth).value
        except DSLError:
            continue
    if not patches:
        return None
    step = trace.step(step_id)
    names = ", ".join(patches)
    return Intervention(
        step_id=step_id,
        patches=patches,
        source="truth",
        description=(
            f"Set {step.agent if step else step_id}.{names} to the value its contract or the source of truth requires"
        ),
    )


class ReplayPlan(BaseModel):
    frozen: list[str]  # steps reused verbatim (up to and including the intervention step)
    replay: list[str]  # steps re-executed
    intervention: Intervention


class ReplayUnavailable(Exception):
    """The trace has no runnable workflow, or the intervention names an unknown step."""


def plan_replay(trace: TraceV1, intervention: Intervention) -> ReplayPlan:
    try:
        idx = trace.step_index(intervention.step_id)
    except KeyError:
        raise ReplayUnavailable(f"step '{intervention.step_id}' is not in this run") from None
    step = trace.steps[idx]
    for fld in intervention.patches:
        if fld not in step.outputs:
            raise ReplayUnavailable(f"step '{step.step_id}' has no output field '{fld}' to patch")
    return ReplayPlan(
        frozen=[s.step_id for s in trace.steps[: idx + 1]],
        replay=[s.step_id for s in trace.steps[idx + 1 :]],
        intervention=intervention,
    )


def patched_outputs(original: dict[str, Any], intervention: Intervention) -> dict[str, Any]:
    out = copy.deepcopy(original)
    out.update(copy.deepcopy(intervention.patches))
    return out


# ---- judging --------------------------------------------------------------------------------------


class ReplayJudgement(BaseModel):
    passed: bool
    fixed: list[str] = Field(default_factory=list)
    still_failing: list[str] = Field(default_factory=list)
    regressions: list[str] = Field(default_factory=list)


def judge_replay(
    original: list[CheckResult], replay: list[CheckResult], target_check_ids: list[str]
) -> ReplayJudgement:
    """A replay passes iff every target check now PASSES and no check that passed originally stopped
    passing (regression guard, FR-VER-03)."""
    now = {r.check_id: r.status for r in replay}
    was = {r.check_id: r.status for r in original}
    fixed = [c for c in target_check_ids if now.get(c) is CheckStatus.PASS]
    still = [c for c in target_check_ids if now.get(c) is not CheckStatus.PASS]
    regress = [c for c, s in was.items() if s is CheckStatus.PASS and now.get(c) is not CheckStatus.PASS]
    return ReplayJudgement(passed=not still and not regress, fixed=fixed, still_failing=still, regressions=regress)


class ExperimentSummary(BaseModel):
    rule_version: str = RULE_VERSION
    n_planned: int
    n_completed: int
    k_pass: int
    m_planned: int
    m_completed: int
    c_pass: int
    ci_low: float
    ci_high: float
    verdict: Verdict
    explanation: str


def summarize(intervention_passes: list[bool], control_passes: list[bool], n: int, m: int) -> ExperimentSummary:
    if not 1 <= n <= MAX_REPLAYS or not 0 <= m <= MAX_CONTROLS:
        raise ValueError(f"n must be 1..{MAX_REPLAYS} and m 0..{MAX_CONTROLS}")
    k, c = sum(intervention_passes), sum(control_passes)
    verdict = decide(k, n, c, m, completed=len(intervention_passes), completed_controls=len(control_passes))
    lo, hi = wilson(k, len(intervention_passes)) if intervention_passes else (0.0, 1.0)
    if verdict is Verdict.ERROR:
        why = (
            f"Only {len(intervention_passes)}/{n} replays and {len(control_passes)}/{m} controls finished; no verdict."
        )
    elif verdict is Verdict.CONFIRMED:
        why = (
            f"With the fix applied the outcome was correct in {k}/{n} replays, and in {c}/{m} controls without it: "
            "the fix, not luck, changed the result."
        )
    elif verdict is Verdict.REFUTED:
        why = f"Fixing this step did not change the outcome ({k}/{n} replays passed): it is not the origin."
    else:
        why = (
            f"{k}/{n} replays passed with the fix and {c}/{m} controls without it: not clear enough to decide. "
            "Increase the number of replays or review the evidence."
        )
    return ExperimentSummary(
        n_planned=n,
        n_completed=len(intervention_passes),
        k_pass=k,
        m_planned=m,
        m_completed=len(control_passes),
        c_pass=c,
        ci_low=round(lo, 4),
        ci_high=round(hi, 4),
        verdict=verdict,
        explanation=why,
    )
