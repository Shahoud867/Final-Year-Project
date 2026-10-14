"""Baseline attributors to measure Granite's trace-back against (FR-EVA-01).

A number is only meaningful next to the naive thing it should beat. The first baseline is
``last_agent``: blame the step where the failure surfaced. It is what a developer does without
a tool, it is what the symptom step already tells you, and on a pipeline where the fault is
injected upstream it is wrong by construction — which is exactly the gap Granite claims to close.

The baselines deliberately share ``HypothesisSpec`` with :mod:`granite_core.attribution`, so the
evaluation harness scores every method through one code path and cannot accidentally favour ours.
"""

from __future__ import annotations

from .attribution import HypothesisSpec
from .lineage import ancestors_with_distance
from .trace import TraceV1

__all__ = ["last_agent", "upstream_first"]


def last_agent(trace: TraceV1, symptom_step: str) -> list[HypothesisSpec]:
    """Blame the step where the failure surfaced. One hypothesis, no evidence, no search.

    This is the "last agent" baseline named in the evaluation plan. It is free and it is right
    whenever the failure originates where it shows, which is the case this project exists to
    distinguish from the case where it does not.
    """
    step = trace.step(symptom_step)
    if step is None:
        return []
    return [
        HypothesisSpec(
            rank=1,
            step_id=symptom_step,
            agent=step.agent,
            method="last_agent",
            evidence_kind="none",
            score=1.0,
            rationale="Baseline: the step where the wrong outcome was observed, with no search for its origin.",
            evidence=[],
        )
    ]


def upstream_first(trace: TraceV1, symptom_step: str, limit: int = 5) -> list[HypothesisSpec]:
    """Blame the earliest ancestor of the symptom, then work forward. Structure only, no evidence.

    A second naive strategy, and the opposite error to ``last_agent``: it is right whenever the
    fault sits at the start of the pipeline. Reporting both bounds the range a position-only
    method can reach, so a reader can see how much of Granite's accuracy comes from evidence
    rather than from the shape of the workflow.
    """
    dist, _ = ancestors_with_distance(trace, symptom_step)
    if not dist:
        return []
    order = {s.step_id: i for i, s in enumerate(trace.steps)}
    candidates = sorted(dist, key=lambda sid: order.get(sid, len(order)))
    out: list[HypothesisSpec] = []
    for rank, sid in enumerate(candidates[:limit], start=1):
        step = trace.step(sid)
        if step is None:
            continue
        out.append(
            HypothesisSpec(
                rank=rank,
                step_id=sid,
                agent=step.agent,
                method="upstream_first",
                evidence_kind="none",
                score=round(1.0 / rank, 3),
                rationale="Baseline: ranked by position in the pipeline, earliest first, with no evidence.",
                evidence=[],
            )
        )
    return out
