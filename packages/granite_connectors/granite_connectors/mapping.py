"""Map the spans of one third-party trace to Granite Trace v1, inferring who read what when nobody declared it.

Lineage comes from three sources, tried in order and recorded on every edge (integrations strategy, section 4.3):

* ``declared``: the span carries ``granite.reads`` (Granite's own exports, or an application that adds one line);
* ``value``: a later step's input contains a distinctive value an earlier step produced;
* ``order``: otherwise a step is taken to read its predecessor (the weakest evidence; attribution then ranks by
  position).
"""

from __future__ import annotations

import json
import re
from typing import Any, Literal

from granite_core.trace import TASK, RunInfo, Step, StepKind, TraceV1, split_read
from pydantic import BaseModel, Field

from .spans import READS_KEY, STEP_KEY, Profile, SpanRecord

MAPPER_VERSION = "granite.mapper/1"
MIN_TEXT = 12  # a string shorter than this is too common to prove a hand-off
Tier = Literal["declared", "value", "order"]


class Edge(BaseModel):
    """A read of one step's output by a later step, and how Granite knows it."""

    read: str
    step_id: str
    tier: Tier


class MappedTrace(BaseModel):
    """The Granite trace, the provenance of each edge, and what the mapping left out."""

    trace: TraceV1
    lineage: list[Edge] = Field(default_factory=list)
    spans_total: int
    spans_dropped: int
    root_span_id: str | None = None
    span_ids: dict[str, str] = Field(default_factory=dict, description="step_id -> span id on the platform")
    run_attrs: dict[str, Any] = Field(default_factory=dict, description="granite.* attributes of the root span")
    mapper_version: str = MAPPER_VERSION


def as_dict(value: Any) -> dict[str, Any]:
    """Inputs and outputs as a dict: JSON text is parsed; anything that is not a dict goes under ``value``."""
    if value is None:
        return {}
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return {"value": value}
    return value if isinstance(value, dict) else {"value": value}


def _slug(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", name.strip()).strip("_")
    return (s or "step")[:48]


def _kind(span: SpanRecord) -> StepKind:
    forced = span.attributes.get("granite.kind")
    if forced in ("llm", "tool", "code", "handoff"):
        return forced  # type: ignore[no-any-return]
    return {"llm": "llm", "tool": "tool", "retriever": "tool"}.get(span.kind, "code")  # type: ignore[return-value]


def _order(spans: list[SpanRecord]) -> list[SpanRecord]:
    """Granite's own exports carry their position (``granite.index``); other spans are ordered by start time."""
    def key(p: tuple[int, SpanRecord]) -> tuple[int, Any, int]:
        index = p[1].attributes.get("granite.index")
        if isinstance(index, int):
            return (0, index, p[0])
        return (1 if p[1].start else 2, p[1].start.timestamp() if p[1].start else 0, p[0])
    return [s for _, s in sorted(enumerate(spans), key=key)]


def select_steps(spans: list[SpanRecord], profile: Profile) -> list[SpanRecord]:
    """The spans that become steps: those the profile names (or Granite exported), else the leaf spans."""
    named = [s for s in spans if s.name in profile.steps or STEP_KEY in s.attributes]
    if named:
        return _order(named)
    parents = {s.parent_id for s in spans if s.parent_id}
    return _order([s for s in spans if s.span_id not in parents])


def _leaves(value: Any) -> list[Any]:
    if isinstance(value, dict):
        return [x for v in value.values() for x in _leaves(v)]
    if isinstance(value, list):
        return [x for v in value for x in _leaves(v)]
    return [value]


def _distinctive(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return abs(value) >= 10 or (isinstance(value, float) and value != round(value))
    if isinstance(value, str):
        return len(value) >= MIN_TEXT
    return len(json.dumps(value, default=str)) >= MIN_TEXT


def _appears_in(value: Any, haystack: Any) -> bool:
    """True if ``value`` is in ``haystack``: equal to a nested value, or (for text) contained in a string."""
    if isinstance(value, (dict, list)):
        if value == haystack:
            return True
        if isinstance(haystack, dict):
            return any(_appears_in(value, v) for v in haystack.values())
        if isinstance(haystack, list):
            return any(_appears_in(value, v) for v in haystack)
        return False
    for leaf in _leaves(haystack):
        if leaf == value or (isinstance(value, str) and isinstance(leaf, str) and value in leaf):
            return True
        if isinstance(value, (int, float)) and isinstance(leaf, str) and _number_in_text(value, leaf):
            return True
    return False


def _number_in_text(value: float, text: str) -> bool:
    shown = {f"{value:.2f}", f"{value:g}", str(value)}
    return any(re.search(rf"(?<![\d.]){re.escape(s)}(?![\d])", text) for s in shown)


def _declared(span: SpanRecord, known: set[str]) -> list[str]:
    raw = span.attributes.get(READS_KEY)
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            raw = [raw]
    out = []
    for ref in raw if isinstance(raw, list) else []:
        try:
            src, _ = split_read(str(ref))
        except ValueError:
            continue
        if src == TASK or src in known:
            out.append(str(ref))
    return out


def _text(raw: Any) -> str | None:
    return None if raw is None else str(raw)


def _params(raw: Any) -> dict[str, Any] | None:
    if raw is None:
        return None
    parsed = as_dict(raw)
    return None if set(parsed) == {"value"} else parsed


def _value_reads(inputs: dict[str, Any], earlier: list[Step]) -> list[str]:
    reads = []
    for prev in earlier:
        for field, value in prev.outputs.items():
            if _distinctive(value) and _appears_in(value, inputs):
                reads.append(f"{prev.step_id}.{field}")
    return reads


def map_trace(spans: list[SpanRecord], profile: Profile, runtime: str) -> MappedTrace:
    """Build a Granite trace from the spans of one third-party trace (all spans must share one trace id)."""
    if not spans:
        raise ValueError("a trace needs at least one span")
    if len({s.trace_id for s in spans}) != 1:
        raise ValueError("spans of more than one trace were given")
    chosen = select_steps(spans, profile)
    roots = [s for s in spans if not s.parent_id]
    task_source = roots[0] if roots and roots[0] not in chosen else chosen[0]
    steps: list[Step] = []
    lineage: list[Edge] = []
    used: set[str] = set()
    span_ids: dict[str, str] = {}
    for span in chosen:
        base = str(span.attributes.get(STEP_KEY) or profile.steps.get(span.name) or _slug(span.name))
        step_id, n = base, 2
        while step_id in used:
            step_id, n = f"{base}_{n}", n + 1
        inputs, outputs = as_dict(span.input), as_dict(span.output)
        untimed = span.attributes.get("granite.untimed") is True  # Granite exported a step that had no times
        reads = _declared(span, used)
        tier: Tier = "declared"
        declared = READS_KEY in span.attributes  # an explicit empty list means "reads nothing earlier"
        if not reads and not declared:
            reads, tier = _value_reads(inputs, steps), "value"
        if not reads and not declared and steps and steps[-1].outputs:
            reads, tier = [f"{steps[-1].step_id}.{next(iter(steps[-1].outputs))}"], "order"
        lineage += [Edge(read=r, step_id=step_id, tier=tier) for r in reads]
        steps.append(Step(
            step_id=step_id, agent=str(span.attributes.get("granite.agent") or span.name)[:120], kind=_kind(span),
            name=str(span.attributes.get("granite.name") or ""), inputs=inputs, outputs=outputs, reads=reads,
            model=span.attributes.get("llm.model_name") or span.attributes.get("model"),
            params=_params(span.attributes.get("granite.params")),
            prompt_hash=_text(span.attributes.get("granite.prompt_hash")),
            error=span.error if span.status == "error" else None,
            started_at=None if untimed else span.start, ended_at=None if untimed else span.end,
        ))
        used.add(step_id)
        span_ids[step_id] = span.span_id
    errored = any(s.status == "error" for s in spans)
    task_input = as_dict(task_source.input)
    if "granite.task" in chosen[0].attributes:
        task_input = as_dict(chosen[0].attributes["granite.task"])
    trace = TraceV1(run=RunInfo(
        external_id=spans[0].trace_id, workflow=profile.workflow or profile.name, runtime=runtime,
        status="errored" if errored else "completed", task_input=task_input,
        final_output={} if errored else steps[-1].outputs,
        started_at=min((s.start for s in spans if s.start), default=None),
        ended_at=max((s.end for s in spans if s.end), default=None),
    ), steps=steps)
    root = roots[0] if roots else None
    run_attrs = {k.removeprefix("granite."): v for k, v in (root.attributes if root else {}).items()
                 if k.startswith("granite.")}
    return MappedTrace(trace=trace, lineage=lineage, spans_total=len(spans), spans_dropped=len(spans) - len(steps),
                       root_span_id=root.span_id if root else None, span_ids=span_ids, run_attrs=run_attrs)


__all__ = ["MAPPER_VERSION", "Edge", "MappedTrace", "as_dict", "map_trace", "select_steps"]
