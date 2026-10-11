"""Database tables (master plan 14.6). Evidence and audit rows are append-only: the API has no update path.

The canonical trace of a run is stored as one JSON document (runs.trace); steps and graph edges are derived
from it on read, so there is a single source for hashing and replay.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def new_id(prefix: str) -> str:
    """A new record id: the prefix and 12 hexadecimal characters."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def now() -> datetime:
    """Current time in UTC."""
    return datetime.now(UTC)


class Project(Base):
    """A workflow under investigation."""
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    workflow_key: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Run(Base):
    """One execution of a workflow, with its trace."""
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    workflow_key: Mapped[str] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)  # queued, running, completed, errored
    llm_mode: Mapped[str] = mapped_column(String(20), default="recorded")  # what actually answered: live or recorded
    model: Mapped[str] = mapped_column(String(80), default="")
    seed: Mapped[int] = mapped_column(Integer, default=1)
    fault_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    task_input: Mapped[dict[str, Any]] = mapped_column(JSON)
    trace: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    trace_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    check_results: Mapped[list[CheckResultRow]] = relationship(back_populates="run", cascade="all, delete-orphan")
    fault: Mapped[FaultInjection | None] = relationship(
        back_populates="run", uselist=False, cascade="all, delete-orphan"
    )
    findings: Mapped[list[Finding]] = relationship(back_populates="run", cascade="all, delete-orphan")


class FaultInjection(Base):
    """Ground truth of an injected fault. Never read by detection or attribution; used only to score them."""

    __tablename__ = "fault_injections"
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), primary_key=True)
    fault_type: Mapped[str] = mapped_column(String(40))
    target_step: Mapped[str] = mapped_column(String(40))
    field_path: Mapped[str] = mapped_column(String(120))
    original_value: Mapped[Any] = mapped_column(JSON)
    injected_value: Mapped[Any] = mapped_column(JSON)
    note: Mapped[str] = mapped_column(Text, default="")
    run: Mapped[Run] = relationship(back_populates="fault")


class CheckResultRow(Base):
    """The result of one check on one run."""
    __tablename__ = "check_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), index=True)
    check_id: Mapped[str] = mapped_column(String(40))
    check_version: Mapped[int] = mapped_column(Integer, default=1)
    scope: Mapped[str] = mapped_column(String(10))
    step: Mapped[str] = mapped_column(String(40))
    type: Mapped[str] = mapped_column(String(20))
    severity: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(10), index=True)
    observed: Mapped[Any] = mapped_column(JSON, nullable=True)
    expected: Mapped[Any] = mapped_column(JSON, nullable=True)
    message: Mapped[str] = mapped_column(Text, default="")
    computation: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    run: Mapped[Run] = relationship(back_populates="check_results")


class Finding(Base):
    """A case opened for a failed outcome check or an errored run."""
    __tablename__ = "findings"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    severity: Mapped[str] = mapped_column(String(10))
    title: Mapped[str] = mapped_column(Text)
    detail: Mapped[str] = mapped_column(Text, default="")
    check_id: Mapped[str | None] = mapped_column(String(40), nullable=True)
    symptom_step: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)

    run: Mapped[Run] = relationship(back_populates="findings")
    hypotheses: Mapped[list[Hypothesis]] = relationship(
        back_populates="finding", cascade="all, delete-orphan", order_by="Hypothesis.rank"
    )
    reviews: Mapped[list[Review]] = relationship(
        back_populates="finding", cascade="all, delete-orphan", order_by="Review.created_at"
    )


class Hypothesis(Base):
    """A ranked suspect step for a finding."""
    __tablename__ = "hypotheses"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    finding_id: Mapped[str] = mapped_column(ForeignKey("findings.id"), index=True)
    rank: Mapped[int] = mapped_column(Integer)
    step_id: Mapped[str] = mapped_column(String(40))
    agent: Mapped[str] = mapped_column(String(80))
    method: Mapped[str] = mapped_column(String(20))
    evidence_kind: Mapped[str] = mapped_column(String(30))
    score: Mapped[float] = mapped_column(Float)
    rationale: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, confirmed, refuted, inconclusive, error
    finding: Mapped[Finding] = relationship(back_populates="hypotheses")
    experiments: Mapped[list[Experiment]] = relationship(
        back_populates="hypothesis", cascade="all, delete-orphan", order_by="Experiment.created_at"
    )


class Experiment(Base):
    """A verification of one hypothesis by replays and controls."""
    __tablename__ = "experiments"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    hypothesis_id: Mapped[str] = mapped_column(ForeignKey("hypotheses.id"), index=True)
    finding_id: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(20), default="queued")  # queued, running, done, error
    llm_mode: Mapped[str] = mapped_column(String(20), default="recorded")
    n: Mapped[int] = mapped_column(Integer)
    m: Mapped[int] = mapped_column(Integer)
    base_seed: Mapped[int] = mapped_column(Integer, default=1000)
    rule_version: Mapped[str] = mapped_column(String(10), default="VR-1")
    intervention: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    summary: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    verdict: Mapped[str | None] = mapped_column(String(20), nullable=True)
    error: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    hypothesis: Mapped[Hypothesis] = relationship(back_populates="experiments")
    replays: Mapped[list[ReplayRow]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan", order_by="ReplayRow.id"
    )


class ReplayRow(Base):
    """One replay or control of an experiment."""
    __tablename__ = "replays"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    experiment_id: Mapped[str] = mapped_column(ForeignKey("experiments.id"), index=True)
    kind: Mapped[str] = mapped_column(String(15))  # intervention or control
    idx: Mapped[int] = mapped_column(Integer)
    seed: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool] = mapped_column(Boolean)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    judgement: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    results: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    final_output: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    experiment: Mapped[Experiment] = relationship(back_populates="replays")


class Evidence(Base):
    """Append-only: content and hash are written once."""

    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(32), index=True)
    finding_id: Mapped[str | None] = mapped_column(String(32), index=True, nullable=True)
    type: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(200))
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    sha256: Mapped[str] = mapped_column(String(64))
    reproduce: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Review(Base):
    """A reviewer's decision on a finding."""
    __tablename__ = "reviews"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    finding_id: Mapped[str] = mapped_column(ForeignKey("findings.id"), index=True)
    reviewer: Mapped[str] = mapped_column(String(80))
    decision: Mapped[str] = mapped_column(String(20))
    comment: Mapped[str] = mapped_column(Text, default="")
    from_status: Mapped[str] = mapped_column(String(20))
    to_status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    finding: Mapped[Finding] = relationship(back_populates="reviews")


class Job(Base):
    """A background job and its progress."""
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))  # run or experiment
    target_id: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(15), default="queued", index=True)  # queued, running, succeeded, failed
    progress_done: Mapped[int] = mapped_column(Integer, default=0)
    progress_total: Mapped[int] = mapped_column(Integer, default=0)
    message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AuditLog(Base):
    """Append-only record of who did what (FR-AUD)."""

    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
    actor: Mapped[str] = mapped_column(String(80))
    action: Mapped[str] = mapped_column(String(40))
    entity_type: Mapped[str] = mapped_column(String(20))
    entity_id: Mapped[str] = mapped_column(String(32))
    detail: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
