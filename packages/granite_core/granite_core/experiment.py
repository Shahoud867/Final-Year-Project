"""Verification experiment: N replays with the intervention, M controls without it (FR-VER-01..05, VR-1).

Pure orchestration over :mod:`runner` and :mod:`verification`; persistence and progress reporting belong to the
caller (the API passes ``on_replay`` to store each replay as it finishes).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from .checks import CheckResult, evaluate_checks
from .llm import LLMProvider
from .runner import RunOutcome, WorkflowDef, execute_replay
from .trace import TraceV1
from .verification import (
    ExperimentSummary,
    Intervention,
    ReplayJudgement,
    ReplayUnavailable,
    build_intervention,
    judge_replay,
    plan_replay,
    summarize,
)


class ReplayRecord(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    kind: Literal["intervention", "control"]
    index: int
    seed: int
    completed: bool
    trace: TraceV1
    results: list[CheckResult]
    judgement: ReplayJudgement | None  # None when the replay did not finish


class ExperimentRun(BaseModel):
    intervention: Intervention
    summary: ExperimentSummary
    replays: list[ReplayRecord]


def run_experiment(
    defn: WorkflowDef,
    trace: TraceV1,
    step_id: str,
    llm: LLMProvider | None,
    n: int,
    m: int,
    target_check_ids: list[str],
    base_seed: int = 1000,
    on_replay: Callable[[ReplayRecord], None] | None = None,
    intervention: Intervention | None = None,
) -> ExperimentRun:
    """Replay the run from ``step_id`` on, with and without the repair, and decide with VR-1.

    Raises :class:`ReplayUnavailable` when the workflow has no repair for that step (the caller then reports the
    hypothesis as 'cannot be verified automatically' rather than guessing).
    """
    truth: Mapping[str, Callable[..., Any]] = defn.truth()
    original = evaluate_checks(trace, defn.checks, truth)
    chosen = intervention or build_intervention(trace, step_id, defn.repairs.get(step_id, []), truth)
    if chosen is None:
        raise ReplayUnavailable(f"no repair rule is defined for step '{step_id}', so it cannot be replayed")
    plan = plan_replay(trace, chosen)

    records: list[ReplayRecord] = []
    passes: dict[str, list[bool]] = {"intervention": [], "control": []}
    schedule = [("intervention", i) for i in range(n)] + [("control", j) for j in range(m)]
    for kind, idx in schedule:
        seed = base_seed + (0 if kind == "intervention" else 500) + idx
        out: RunOutcome = execute_replay(defn, trace, plan, llm, seed, with_intervention=(kind == "intervention"))
        done = out.trace.run.status == "completed"
        results = evaluate_checks(out.trace, defn.checks, truth)
        judgement = judge_replay(original, results, target_check_ids) if done else None
        if done and judgement is not None:
            passes[kind].append(judgement.passed)
        rec = ReplayRecord(
            kind="intervention" if kind == "intervention" else "control", index=idx, seed=seed, completed=done,
            trace=out.trace, results=results, judgement=judgement,
        )
        records.append(rec)
        if on_replay:
            on_replay(rec)
    summary = summarize(passes["intervention"], passes["control"], n, m)
    return ExperimentRun(intervention=chosen, summary=summary, replays=records)
