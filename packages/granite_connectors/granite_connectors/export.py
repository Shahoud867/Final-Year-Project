"""Turn a Granite trace into neutral spans, so a run can be sent to an observability platform and read back exactly.

Each step becomes one child span of a root span named after the workflow. Granite's own keys (step alias, reads,
agent, kind, task) travel as attributes, so importing the exported trace rebuilds the same lineage with the
``declared`` tier. Ids are derived from the run id, so exporting the same run twice addresses the same spans.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta

from granite_core.trace import TraceV1

from .spans import READS_KEY, STEP_KEY, SpanKind, SpanRecord

_KIND: dict[str, SpanKind] = {"llm": "llm", "tool": "tool", "code": "chain", "handoff": "agent"}


def hex_id(seed: str, length: int) -> str:
    """A stable lowercase hex id of ``length`` characters (32 for an OTel trace id, 16 for a span id)."""
    return hashlib.sha256(seed.encode()).hexdigest()[:length]


def _times(trace: TraceV1) -> list[tuple[datetime, datetime]]:
    """Start and end of each step; a step without times starts when the previous one ended, so platforms that
    order spans by start time show the steps in execution order."""
    out: list[tuple[datetime, datetime]] = []
    cursor = trace.run.started_at or datetime(2026, 1, 1, tzinfo=UTC)
    for step in trace.steps:
        start = step.started_at or cursor
        end = step.ended_at or start + timedelta(microseconds=1)
        out.append((start, end))
        cursor = max(cursor, end)
    return out


def trace_to_spans(trace: TraceV1, run_key: str, run_attrs: dict[str, object] | None = None) -> list[SpanRecord]:
    """The spans of one run: a root span for the workflow, then one span per step in order.

    ``run_attrs`` adds facts about the run to the root span (seed, model, injected fault), prefixed ``granite.``.
    """
    trace_id = hex_id(f"granite-trace:{run_key}", 32)
    root_id = hex_id(f"granite-root:{run_key}", 16)
    timed = _times(trace)
    start = trace.run.started_at or (timed[0][0] if timed else datetime(2026, 1, 1, tzinfo=UTC))
    end = trace.run.ended_at or (timed[-1][1] if timed else start)
    errored = trace.run.status == "errored"
    spans = [SpanRecord(
        span_id=root_id, trace_id=trace_id, name=trace.run.workflow, kind="chain", start=start, end=end,
        input=trace.run.task_input, output=trace.run.final_output, status="error" if errored else "ok",
        attributes={"granite.run_id": run_key, "granite.runtime": trace.run.runtime,
                    **{f"granite.{k}": v for k, v in (run_attrs or {}).items() if v is not None}},
    )]
    for i, step in enumerate(trace.steps):
        s_start, s_end = timed[i]
        attrs: dict[str, object] = {
            STEP_KEY: step.step_id, READS_KEY: json.dumps(step.reads), "granite.agent": step.agent,
            "granite.kind": step.kind, "granite.run_id": run_key, "granite.index": i,
        }
        if step.params is not None:
            attrs["granite.params"] = json.dumps(step.params, default=str)
        if step.started_at is None:
            attrs["granite.untimed"] = True
        if step.prompt_hash:
            attrs["granite.prompt_hash"] = step.prompt_hash
        if step.name:
            attrs["granite.name"] = step.name
        if step.model:
            attrs["llm.model_name"] = step.model
        if i == 0:
            attrs["granite.task"] = json.dumps(trace.run.task_input, default=str)
        spans.append(SpanRecord(
            span_id=hex_id(f"granite-step:{run_key}:{step.step_id}", 16), trace_id=trace_id, parent_id=root_id,
            name=step.agent, kind=_KIND[step.kind], start=s_start, end=s_end, input=step.inputs, output=step.outputs,
            status="error" if step.error else "ok", error=step.error, attributes=attrs,
        ))
    return spans


__all__ = ["hex_id", "trace_to_spans"]
