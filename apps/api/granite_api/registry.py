"""Workflows the API can run. Adding a workflow means adding one entry here (the core stays unchanged)."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from granite_core.runner import Fault, WorkflowDef
from pydantic import BaseModel, ConfigDict, Field, field_validator
from refund_desk import FAULT_TYPES, WORKFLOW_KEY, build_workflow, default_store, make_fault

EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,120}\.[^@\s]{2,24}$")
ORDER_ID = re.compile(r"^#W\d{3,12}$")


class RefundTask(BaseModel):
    """A refund request as the Refund Desk accepts it."""
    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=3, max_length=2000)
    email: str = Field(max_length=190)
    order_id: str

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        if not EMAIL.match(v):
            raise ValueError("must look like name@example.com")
        return v

    @field_validator("order_id")
    @classmethod
    def _order(cls, v: str) -> str:
        if not ORDER_ID.match(v):
            raise ValueError("must look like #W1234567")
        return v


@dataclass(frozen=True)
class WorkflowEntry:
    """What the API needs to offer a workflow: builder, examples, faults and input validation."""
    key: str
    title: str
    description: str
    build: Callable[[str], WorkflowDef]
    examples: Callable[[], list[dict[str, Any]]]
    fault_types: tuple[str, ...]
    make_fault: Callable[[str | None], Fault | None]
    validate_task: Callable[[dict[str, Any]], dict[str, Any]]


def _validate_refund(raw: dict[str, Any]) -> dict[str, Any]:
    return RefundTask.model_validate(raw).model_dump()


WORKFLOWS: dict[str, WorkflowEntry] = {
    WORKFLOW_KEY: WorkflowEntry(
        key=WORKFLOW_KEY,
        title="Refund Desk",
        description="Five-step customer-support refund workflow on synthetic tau-bench retail data.",
        build=lambda model: build_workflow(default_store(), model),
        examples=lambda: default_store().example_tasks(12),
        fault_types=tuple(sorted(FAULT_TYPES)),
        make_fault=make_fault,
        validate_task=_validate_refund,
    )
}
