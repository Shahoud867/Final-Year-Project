"""Verification experiment: N replays with the intervention, M controls without it (FR-VER-01..05, VR-1).

Pure orchestration over :mod:`runner` and :mod:`verification`; persistence and progress reporting belong to the
caller (the API passes ``on_replay`` to store each replay as it finishes).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from .checks import CheckResult, evaluate_checks
from .interventions import derive_intervention
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
    """One replay of an experiment: its trace, check results and whether it passed."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    kind: Literal["intervention", "control"]
    index: int
    seed: int
    completed: bool
    trace: TraceV1
    results: list[CheckResult]
    judgement: ReplayJudgement | None  # None when the replay did not finish


class ExperimentRun(BaseModel):
    """A finished experiment: the intervention used, every replay and the VR-1 summary."""
    intervention: Intervention
    summary: ExperimentSummary
    replays: list[ReplayRecord]


def plan_intervention(
    defn: WorkflowDef, trace: TraceV1, step_id: str, results: list[CheckResult] | None = None
) -> Intervention | None:
    """The patch a replay of ``step_id`` would test: derived from the step's failed checks (ADR-011), else from the
    workflow's repair rules; ``None`` when neither says what the correct value is."""
    truth: Mapping[str, Callable[..., Any]] = defn.truth()
    found = results if results is not None else evaluate_checks(trace, defn.checks, truth)
    derived = derive_intervention(trace, step_id, defn.checks, found, truth)
    return derived or build_intervention(trace, step_id, defn.repairs.get(step_id, []), truth)


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

    Raises :class:`ReplayUnavailable` when nothing says what the step's correct output is: no failed check of that
    step names the value and the workflow has no repair rule for it (the caller then reports the hypothesis as
    'cannot be verified automatically' rather than guessing).
    """
    truth: Mapping[str, Callable[..., Any]] = defn.truth()
    original = evaluate_checks(trace, defn.checks, truth)
    chosen = intervention or plan_intervention(defn, trace, step_id, original)
    if chosen is None:
        raise ReplayUnavailable(
            f"no failed check of step '{step_id}' says what its output should be, and the workflow defines no repair "
            "rule for it, so it cannot be replayed"
        )
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
