"""Granite Trace v1: the input contract for runs, imports and the SDK (master plan 22.4).

A trace is an ordered list of steps. Each step declares what it *read* from earlier steps
(`reads`, entries like ``"s2.items"``), which gives the lineage that attribution walks backwards.
Validation is strict on purpose: a malformed trace is rejected with a precise error path rather
than analysed wrongly.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION: Final = "granite.trace/v1"
MAX_STEPS = 500
TASK = "task"  # pseudo step id for reads of the run's input

StepKind = Literal["llm", "tool", "code", "handoff"]
RunStatus = Literal["completed", "errored"]


class Step(BaseModel):
    """One recorded agent action: what it read, received and produced."""
    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    agent: str = Field(min_length=1, max_length=120)
    kind: StepKind
    name: str = ""
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    reads: list[str] = Field(default_factory=list)
    model: str | None = None
    params: dict[str, Any] | None = None
    prompt_hash: str | None = None
    error: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None


class RunInfo(BaseModel):
    """Facts about the whole run: workflow, status, task input and final output."""
    model_config = ConfigDict(extra="forbid")

    external_id: str | None = None
    workflow: str = Field(min_length=1, max_length=120)
    runtime: str = "granite"
    status: RunStatus = "completed"
    task_input: dict[str, Any] = Field(default_factory=dict)
    final_output: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime | None = None
    ended_at: datetime | None = None


def split_read(ref: str) -> tuple[str, str]:
    """``"s2.items"`` -> ``("s2", "items")``. Raises ValueError for anything else."""
    src, sep, field = ref.partition(".")
    if not sep or not src or not field or "." in field:
        raise ValueError(f"read '{ref}' must look like '<step_id>.<field>'")
    return src, field


class TraceV1(BaseModel):
    """Granite Trace v1: a run and its ordered steps, validated on construction."""
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["granite.trace/v1"] = SCHEMA_VERSION
    run: RunInfo
    steps: list[Step] = Field(default_factory=list, max_length=MAX_STEPS)

    @model_validator(mode="after")
    def _check_lineage(self) -> TraceV1:
        seen: set[str] = set()
        for step in self.steps:
            if step.step_id in seen:
                raise ValueError(f"duplicate step_id '{step.step_id}'")
            for ref in step.reads:
                src, _field = split_read(ref)
                if src != TASK and src not in seen:
                    raise ValueError(f"step '{step.step_id}' reads '{ref}', but '{src}' is not an earlier step")
            seen.add(step.step_id)
        return self

    # ---- convenience views -------------------------------------------------------------
    def step(self, step_id: str) -> Step | None:
        """Return the step with this id, or None."""
        return next((s for s in self.steps if s.step_id == step_id), None)

    def step_index(self, step_id: str) -> int:
        """Position of a step in the trace; raises KeyError if it is unknown."""
        for i, s in enumerate(self.steps):
            if s.step_id == step_id:
                return i
        raise KeyError(step_id)

    def context(self) -> dict[str, Any]:
        """Name space for check expressions: ``task`` plus one entry per step holding its outputs."""
        ctx: dict[str, Any] = {TASK: self.run.task_input}
        for s in self.steps:
            ctx[s.step_id] = s.outputs
        return ctx
