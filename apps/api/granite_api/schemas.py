"""Request and response models (they also drive the OpenAPI documentation at /docs)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Out(BaseModel):
    """Base for response models read from database rows."""
    model_config = ConfigDict(from_attributes=True)


class RunCreate(BaseModel):
    """Request to start a run."""
    model_config = ConfigDict(extra="forbid")

    workflow: str = Field(default="refund_desk", max_length=60)
    task_input: dict[str, Any]
    fault: str | None = Field(default=None, max_length=40, description="Fault to inject, or null for a clean run")
    seed: int = Field(default=1, ge=0, le=2_000_000)
    mode: Literal["live", "recorded", "auto"] | None = None


class ExperimentCreate(BaseModel):
    """Request to verify a hypothesis."""
    model_config = ConfigDict(extra="forbid")

    n: int = Field(default=5, ge=1, le=10, description="replays with the fix applied")
    m: int = Field(default=2, ge=0, le=5, description="control replays without the fix")
    mode: Literal["live", "recorded", "auto"] | None = None


class ReviewCreate(BaseModel):
    """A reviewer's decision."""
    model_config = ConfigDict(extra="forbid")

    decision: Literal["accept", "reject", "resolve", "wont_fix", "request_info"]
    comment: str = Field(default="", max_length=2000)
    reviewer: str = Field(default="analyst", min_length=1, max_length=80)


class JobOut(Out):
    """A background job's status and progress."""
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
    """The result of one check."""
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
    """Ground truth of an injected fault."""
    fault_type: str
    target_step: str
    field_path: str
    original_value: Any
    injected_value: Any
    note: str


class RunSummary(Out):
    """A run as shown in lists."""
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
    """A run with its trace, check results and findings."""
    trace: dict[str, Any] | None
    trace_sha256: str | None
    check_results: list[CheckResultOut]
    findings: list[FindingSummary]
    injected_fault: FaultOut | None = Field(
        default=None, description="Ground truth, shown only for evaluation; analysis never reads it"
    )


class LeadOut(Out):
    """The suspect a finding leads with: the step a replay confirmed, otherwise the first-ranked one."""
    step_id: str
    agent: str
    status: str
    fix_pass: int | None = None
    fix_n: int | None = None
    control_pass: int | None = None
    control_n: int | None = None


class FindingSummary(Out):
    """A finding as shown in lists."""
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
    lead: LeadOut | None = None


class HypothesisOut(Out):
    """A ranked origin hypothesis."""
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
    """One replay or control."""
    kind: str
    idx: int
    seed: int
    completed: bool
    passed: bool | None
    judgement: dict[str, Any] | None
    final_output: dict[str, Any]


class ExperimentOut(Out):
    """A verification experiment and its result."""
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
    """A recorded review decision."""
    id: str
    reviewer: str
    decision: str
    comment: str
    from_status: str
    to_status: str
    created_at: datetime


class EvidenceOut(Out):
    """An evidence record with the result of its hash check."""
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


class InvestigationCreate(BaseModel):
    """Request to verify a finding's ranked suspects in order until one is confirmed."""
    model_config = ConfigDict(extra="forbid")

    n: int = Field(default=5, ge=1, le=10, description="replays with the fix, per suspect")
    m: int = Field(default=2, ge=0, le=5, description="control replays without the fix, per suspect")
    budget: int = Field(default=21, ge=1, le=60, description="most replays the whole investigation may use")
    mode: Literal["live", "recorded", "auto"] | None = None


class InvestigationOut(Out):
    """An investigation: the suspects tried, in order, and how it ended."""
    id: str
    finding_id: str
    status: str
    llm_mode: str
    n: int
    m: int
    budget: int
    replays_used: int
    outcome: str | None
    confirmed_step: str | None
    attempts: list[dict[str, Any]]
    error: str
    created_at: datetime
    finished_at: datetime | None


class FindingDetail(FindingSummary):
    """A finding with everything needed to investigate it."""
    detail: str
    hypotheses: list[HypothesisOut]
    experiments: list[ExperimentOut]
    reviews: list[ReviewOut]
    evidence: list[EvidenceOut]
    allowed_actions: list[str]
    investigations: list[InvestigationOut] = []
    can_export_regression: bool = False


class BatchCreate(BaseModel):
    """Request to generate a Fault Lab batch: every chosen fault (and clean runs) on every chosen task."""
    model_config = ConfigDict(extra="forbid")

    workflow: str = Field(default="refund_desk", max_length=60)
    faults: list[str] = Field(min_length=1, max_length=10, description="fault names; 'none' adds clean runs")
    task_ids: list[str] | None = Field(default=None, max_length=50,
                                       description="order ids of example tasks; null means every example task")
    seed: int = Field(default=1, ge=0, le=2_000_000)
    mode: Literal["live", "recorded", "auto"] | None = None


class BatchOut(Out):
    """A batch, its per-condition counts and its runs."""
    id: str
    workflow_key: str
    status: str
    llm_mode: str
    faults: list[str]
    task_count: int
    seed: int
    created_at: datetime
    finished_at: datetime | None
    groups: dict[str, dict[str, int]] = {}
    runs: list[RunSummary] = []


class Accepted(BaseModel):
    """Returned when work was queued: the job to poll and the record it will fill."""
    job_id: str
    run_id: str | None = None
    experiment_id: str | None = None
    investigation_id: str | None = None
    batch_id: str | None = None


class ConnectionCreate(BaseModel):
    """A Phoenix or Langfuse project to import traces from and write verdicts to. Keys come from the environment."""
    model_config = ConfigDict(extra="forbid")

    kind: Literal["phoenix", "langfuse"]
    name: str = Field(min_length=1, max_length=120)
    base_url: str = Field(min_length=8, max_length=300, description="http://localhost:6006 or https://cloud.langfuse.com")
    project: str = Field(default="", max_length=120,
                         description="Phoenix project name; for Langfuse, an optional trace name to filter on")
    workflow: str = Field(default="refund_desk", max_length=60, description="Granite workflow whose checks apply")
    steps: dict[str, str] = Field(default_factory=dict, description="span name -> step id, when names differ")

    @field_validator("steps")
    @classmethod
    def _aliases(cls, v: dict[str, str]) -> dict[str, str]:
        bad = [a for a in v.values() if not a or len(a) > 64 or not all(c.isalnum() or c in "_-" for c in a)]
        if bad or len(v) > 50:
            raise ValueError("step ids use letters, digits, '_' and '-' only (at most 50 mappings)")
        return v


class TraceLinkOut(Out):
    """Where a run lives on a connected platform."""
    connection_id: str
    run_id: str
    direction: str
    external_trace_id: str
    root_span_id: str
    span_ids: dict[str, str]
    lineage: list[dict[str, Any]]
    created_at: datetime


class ConnectionOut(Out):
    """A connection and how many runs it has brought in or received."""
    id: str
    kind: str
    name: str
    base_url: str
    project: str
    workflow_key: str
    profile: dict[str, Any]
    created_at: datetime
    last_sync_at: datetime | None
    last_error: str
    keys_configured: bool = False
    imported_runs: int = 0
    exported_runs: int = 0


class ImportRequest(BaseModel):
    """How many of the newest traces to look at."""
    model_config = ConfigDict(extra="forbid")

    limit: int = Field(default=20, ge=1, le=50)


class ExportRequest(BaseModel):
    """The connection to send a run to."""
    model_config = ConfigDict(extra="forbid")

    connection_id: str = Field(min_length=1, max_length=32)
