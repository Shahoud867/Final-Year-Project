"""Request and response models (they also drive the OpenAPI documentation at /docs)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Out(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RunCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow: str = Field(default="refund_desk", max_length=60)
    task_input: dict[str, Any]
    fault: str | None = Field(default=None, max_length=40, description="Fault to inject, or null for a clean run")
    seed: int = Field(default=1, ge=0, le=2_000_000)
    mode: Literal["live", "recorded", "auto"] | None = None


class ExperimentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    n: int = Field(default=5, ge=1, le=10, description="replays with the fix applied")
    m: int = Field(default=2, ge=0, le=5, description="control replays without the fix")
    mode: Literal["live", "recorded", "auto"] | None = None


class ReviewCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: Literal["accept", "reject", "resolve", "wont_fix", "request_info"]
    comment: str = Field(default="", max_length=2000)
    reviewer: str = Field(default="analyst", min_length=1, max_length=80)


class JobOut(Out):
    id: str
    kind: str
    target_id: str
    status: str
    progress_done: int
    progress_total: int
    message: str
    created_at: datetime
    finished_at: datetime | None


class CheckResultOut(Out):
    check_id: str
    check_version: int
    scope: str
    step: str
    type: str
    severity: str
    status: str
    observed: Any
    expected: Any
    message: str
    computation: dict[str, Any]


class FaultOut(Out):
    fault_type: str
    target_step: str
    field_path: str
    original_value: Any
    injected_value: Any
    note: str


class RunSummary(Out):
    id: str
    workflow_key: str
    status: str
    llm_mode: str
    model: str
    seed: int
    fault_type: str | None
    task_input: dict[str, Any]
    error: str
    created_at: datetime
    finished_at: datetime | None
    finding_count: int = 0
    failed_checks: int = 0


class RunDetail(RunSummary):
    trace: dict[str, Any] | None
    trace_sha256: str | None
    check_results: list[CheckResultOut]
    findings: list[FindingSummary]
    injected_fault: FaultOut | None = Field(
        default=None, description="Ground truth, shown only for evaluation; analysis never reads it"
    )


class FindingSummary(Out):
    id: str
    run_id: str
    kind: str
    severity: str
    title: str
    check_id: str | None
    symptom_step: str
    status: str
    verification_level: str = "V0"
    created_at: datetime


class HypothesisOut(Out):
    id: str
    rank: int
    step_id: str
    agent: str
    method: str
    evidence_kind: str
    score: float
    rationale: str
    evidence: list[dict[str, Any]]
    status: str
    can_verify: bool = True


class ReplayOut(Out):
    kind: str
    idx: int
    seed: int
    completed: bool
    passed: bool | None
    judgement: dict[str, Any] | None
    final_output: dict[str, Any]


class ExperimentOut(Out):
    id: str
    hypothesis_id: str
    finding_id: str
    status: str
    llm_mode: str
    n: int
    m: int
    rule_version: str
    intervention: dict[str, Any] | None
    summary: dict[str, Any] | None
    verdict: str | None
    error: str
    created_at: datetime
    finished_at: datetime | None
    replays: list[ReplayOut] = []


class ReviewOut(Out):
    id: str
    reviewer: str
    decision: str
    comment: str
    from_status: str
    to_status: str
    created_at: datetime


class EvidenceOut(Out):
    id: str
    run_id: str
    finding_id: str | None
    type: str
    title: str
    payload: dict[str, Any]
    sha256: str
    reproduce: str
    created_at: datetime
    hash_valid: bool = True


class FindingDetail(FindingSummary):
    detail: str
    hypotheses: list[HypothesisOut]
    experiments: list[ExperimentOut]
    reviews: list[ReviewOut]
    evidence: list[EvidenceOut]
    allowed_actions: list[str]


class Accepted(BaseModel):
    job_id: str
    run_id: str | None = None
    experiment_id: str | None = None
