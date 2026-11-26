"""The neutral span record every source produces, and the profile that names a team's steps.

Langfuse observations, Phoenix spans and (later) OTLP spans are all turned into :class:`SpanRecord` first, so the
mapping to Granite Trace v1 is written once (docs/plan/integrations-strategy.md, section 4.1).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SpanKind = Literal["llm", "tool", "retriever", "agent", "chain", "other"]

#: Metadata or attribute key an application can set to declare what a step read (``["lookup.items"]``).
READS_KEY = "granite.reads"
#: Key carrying the step alias Granite used when it exported its own run (exact round trip).
STEP_KEY = "granite.step_id"


class SpanRecord(BaseModel):
    """One step of a trace as a third-party platform stored it, normalised."""

    model_config = ConfigDict(extra="forbid")

    span_id: str
    trace_id: str
    parent_id: str | None = None
    name: str
    kind: SpanKind = "other"
    start: datetime | None = None
    end: datetime | None = None
    input: Any = None
    output: Any = None
    status: Literal["ok", "error"] = "ok"
    error: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class Profile(BaseModel):
    """How one connection's traces become Granite traces: which spans are steps, and what they are called.

    ``steps`` maps a span name to the step alias that checks use (``"order-lookup tool": "lookup"``). When it is
    empty, every leaf span becomes a step, named after the span. ``workflow`` names a Granite workflow when the traces
    come from a workflow Granite itself can execute, which makes replay possible.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    steps: dict[str, str] = Field(default_factory=dict)
    workflow: str | None = None
    trace_name: str | None = Field(default=None, description="import only traces with this name")


__all__ = ["READS_KEY", "STEP_KEY", "Profile", "SpanKind", "SpanRecord"]
