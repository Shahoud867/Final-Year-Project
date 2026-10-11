"""Workflow runner: executes a workflow definition and records a Granite trace; re-executes for replay.

A workflow is an ordered list of :class:`StepDef`. Every step declares what it ``reads`` (``"s2.items"``);
the runner resolves those reads into the step's recorded ``inputs``, so the lineage that attribution
walks is exactly the data the step really received (FR-RUN-01).

Faults are injected *after* a step produces its output and are recorded as ground truth in a
separate :class:`FaultRecord`, which attribution never sees (FR-RUN-02).
"""

from __future__ import annotations

import copy
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from .checks import CheckDef
from .evidence import sha256_of
from .llm import Completion, LLMProvider, LLMRequest
from .trace import TASK, RunInfo, Step, StepKind, TraceV1, split_read
from .verification import Intervention, RepairRule, ReplayPlan, patched_outputs


def _now() -> datetime:
    return datetime.now(UTC)


class StepFailed(Exception):
    """A step could not produce a valid output (bad model output, tool failure...). Ends the run as errored."""


@dataclass
class LLMCallInfo:
    """Facts about one model call made by a step, kept in the trace."""
    model: str
    params: dict[str, Any]
    prompt_hash: str
    provider: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    recorded: bool


@dataclass
class StepContext:
    """What a step function receives: the task, earlier outputs, its resolved inputs and a model handle."""
    task: dict[str, Any]
    outputs: dict[str, dict[str, Any]]
    inputs: dict[str, Any]
    llm: LLMProvider | None
    seed: int | None = None
    calls: list[LLMCallInfo] = field(default_factory=list)

    def ask(self, request: LLMRequest) -> Completion:
        """Call the model with the run's seed and record the call."""
        if self.llm is None:
            raise StepFailed("this step needs a language model but none is configured")
        if request.seed is None and self.seed is not None:
            request.seed = self.seed
        out = self.llm.complete(request)
        self.calls.append(
            LLMCallInfo(
                model=out.model,
                params=request.params(),
                provider=out.provider,
                tokens_in=out.tokens_in,
                tokens_out=out.tokens_out,
                latency_ms=out.latency_ms,
                recorded=out.recorded,
                prompt_hash=sha256_of({"model": request.model, "messages": request.messages})[:16],
            )
        )
        return out


@dataclass
class StepDef:
    """A workflow step: its identity, the values it reads and the function that executes it."""
    step_id: str
    agent: str
    kind: StepKind
    name: str
    reads: list[str]
    fn: Callable[[StepContext], dict[str, Any]]


@dataclass
class FaultRecord:
    """Ground truth of an injected fault; stored for scoring, never given to the analysis."""
    fault_type: str
    target_step: str
    field_path: str
    original_value: Any
    injected_value: Any
    note: str = ""


class Fault(Protocol):
    """A deterministic fault operator applied to one step's outputs."""
    fault_type: str
    target_step: str

    def apply(self, outputs: dict[str, Any], inputs: dict[str, Any]) -> tuple[dict[str, Any], FaultRecord]:
        """Corrupt ``outputs``. ``inputs`` is the harness view: the task (``task.<f>``) and every earlier step's
        outputs (``<step>.<f>``), not just what the target step declared it reads."""
        ...


@dataclass
class WorkflowDef:
    """A runnable workflow: steps, checks, repair rules and its source-of-truth functions."""
    key: str
    title: str
    steps: list[StepDef]
    checks: list[CheckDef]
    repairs: dict[str, list[RepairRule]]
    truth: Callable[[], Mapping[str, Callable[..., Any]]]
    description: str = ""
    data_snapshot: str = ""  # id of the pinned data the truth functions read (FR-CHK-06)

    def step_ids(self) -> list[str]:
        """Step ids in execution order."""
        return [s.step_id for s in self.steps]


@dataclass
class RunOutcome:
    """Result of executing a workflow: the trace, the fault record if any, and the model calls."""
    trace: TraceV1
    fault: FaultRecord | None
    calls: list[LLMCallInfo]


def _resolve_reads(reads: list[str], task: dict[str, Any], outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    resolved: dict[str, Any] = {}
    for ref in reads:
        src, fld = split_read(ref)
        pool = task if src == TASK else outputs.get(src, {})
        if fld in pool:
            resolved[ref] = copy.deepcopy(pool[fld])
    return resolved


def _harness_view(task: dict[str, Any], outputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    view: dict[str, Any] = {f"{TASK}.{k}": copy.deepcopy(v) for k, v in task.items()}
    for sid, out in outputs.items():
        view.update({f"{sid}.{k}": copy.deepcopy(v) for k, v in out.items()})
    return view


def _execute_steps(
    defn: WorkflowDef,
    steps: list[StepDef],
    task: dict[str, Any],
    outputs: dict[str, dict[str, Any]],
    llm: LLMProvider | None,
    seed: int | None,
    fault: Fault | None,
) -> tuple[list[Step], FaultRecord | None, list[LLMCallInfo], str | None]:
    records: list[Step] = []
    fault_rec: FaultRecord | None = None
    all_calls: list[LLMCallInfo] = []
    for sd in steps:
        ctx = StepContext(
            task=task, outputs=outputs, inputs=_resolve_reads(sd.reads, task, outputs), llm=llm, seed=seed
        )
        started, error, out = _now(), None, {}
        try:
            out = sd.fn(ctx)
            if fault is not None and fault.target_step == sd.step_id:
                out, fault_rec = fault.apply(out, _harness_view(task, outputs))
        except StepFailed as e:
            error = str(e)
        except Exception as e:  # any provider/tool failure ends the run cleanly as errored
            error = f"{type(e).__name__}: {e}"
        last = ctx.calls[-1] if ctx.calls else None
        records.append(
            Step(
                step_id=sd.step_id,
                agent=sd.agent,
                kind=sd.kind,
                name=sd.name,
                inputs=ctx.inputs,
                outputs=out,
                reads=list(sd.reads),
                model=last.model if last else None,
                params={
                    **last.params,
                    "provider": last.provider,
                    "recorded": last.recorded,
                    "calls": len(ctx.calls),
                    "tokens_in": sum(c.tokens_in for c in ctx.calls),
                    "tokens_out": sum(c.tokens_out for c in ctx.calls),
                }
                if last
                else None,
                prompt_hash=last.prompt_hash if last else None,
                error=error,
                started_at=started,
                ended_at=_now(),
            )
        )
        all_calls.extend(ctx.calls)
        if error is not None:
            return records, fault_rec, all_calls, f"{sd.agent}: {error}"
        outputs[sd.step_id] = out
    return records, fault_rec, all_calls, None


def run_workflow(
    defn: WorkflowDef,
    task_input: dict[str, Any],
    llm: LLMProvider | None,
    fault: Fault | None = None,
    seed: int | None = None,
    external_id: str | None = None,
) -> RunOutcome:
    """Execute a workflow on a task and return its trace; a failing step ends the run as errored."""
    started = _now()
    outputs: dict[str, dict[str, Any]] = {}
    records, fault_rec, calls, err = _execute_steps(defn, defn.steps, task_input, outputs, llm, seed, fault)
    last_out = records[-1].outputs if records else {}
    trace = TraceV1(
        run=RunInfo(
            external_id=external_id,
            workflow=defn.key,
            runtime="granite",
            status="errored" if err else "completed",
            task_input=copy.deepcopy(task_input),
            final_output=last_out if not err else {},
            started_at=started,
            ended_at=_now(),
        ),
        steps=records,
    )
    return RunOutcome(trace=trace, fault=fault_rec, calls=calls)


def execute_replay(
    defn: WorkflowDef,
    original: TraceV1,
    plan: ReplayPlan,
    llm: LLMProvider | None,
    seed: int | None,
    with_intervention: bool,
    fault: Fault | None = None,
) -> RunOutcome:
    """Re-execute the steps after the intervention step. Frozen steps are copied verbatim (no model call)."""
    started = _now()
    by_id = {s.step_id: s for s in defn.steps}
    outputs: dict[str, dict[str, Any]] = {}
    records: list[Step] = []
    for sid in plan.frozen:
        orig = original.step(sid)
        assert orig is not None
        rec = orig.model_copy(deep=True)
        if with_intervention and sid == plan.intervention.step_id:
            rec.outputs = patched_outputs(orig.outputs, plan.intervention)
        outputs[sid] = rec.outputs
        records.append(rec)
    todo = [by_id[sid] for sid in plan.replay]
    new, fault_rec, calls, err = _execute_steps(
        defn, todo, copy.deepcopy(original.run.task_input), outputs, llm, seed, fault
    )
    records.extend(new)
    trace = TraceV1(
        run=RunInfo(
            workflow=defn.key,
            runtime="granite",
            status="errored" if err else "completed",
            task_input=copy.deepcopy(original.run.task_input),
            final_output=(records[-1].outputs if records and not err else {}),
            started_at=started,
            ended_at=_now(),
        ),
        steps=records,
    )
    return RunOutcome(trace=trace, fault=fault_rec, calls=calls)


__all__ = [
    "Fault",
    "FaultRecord",
    "Intervention",
    "LLMCallInfo",
    "RunOutcome",
    "StepContext",
    "StepDef",
    "StepFailed",
    "WorkflowDef",
    "execute_replay",
    "run_workflow",
]
