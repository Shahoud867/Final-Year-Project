"""Lineage graph over a trace: who read what from whom (derived from each step's ``reads``)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .trace import TASK, TraceV1, split_read


@dataclass(frozen=True)
class Edge:
    """A data-flow edge: ``dst`` read ``field`` from ``src``."""
    src: str  # the step that produced the value
    dst: str  # the step that read it
    field: str  # which output field travelled


def edges(trace: TraceV1) -> list[Edge]:
    """Data-flow edges between steps. Reads of the run input (``task.*``) are not step-to-step edges."""
    out: list[Edge] = []
    for step in trace.steps:
        for ref in step.reads:
            src, fld = split_read(ref)
            if src != TASK:
                out.append(Edge(src, step.step_id, fld))
    return out


def incoming(trace: TraceV1) -> dict[str, list[Edge]]:
    """Index the edges of a trace by the step that reads them."""
    inc: dict[str, list[Edge]] = defaultdict(list)
    for e in edges(trace):
        inc[e.dst].append(e)
    return inc


def ancestors_with_distance(
    trace: TraceV1, symptom: str, max_revisit: int = 3
) -> tuple[dict[str, int], dict[str, str]]:
    """Breadth-first walk backwards from ``symptom``.

    Returns (distance from the symptom, the downstream neighbour each step was reached from).
    The ``max_revisit`` bound keeps the walk finite even if an imported trace were cyclic (FR-ATT-03).
    """
    inc = incoming(trace)
    dist: dict[str, int] = {symptom: 0}
    parent: dict[str, str] = {}
    visits: dict[str, int] = defaultdict(int)
    queue = [symptom]
    while queue:
        cur = queue.pop(0)
        visits[cur] += 1
        if visits[cur] > max_revisit:
            continue
        for e in inc.get(cur, []):
            if e.src not in dist:
                dist[e.src] = dist[cur] + 1
                parent[e.src] = cur
                queue.append(e.src)
    return dist, parent


def betweenness_fraction(trace: TraceV1, symptom: str) -> dict[str, float]:
    """Share of all source-to-symptom paths that pass through each ancestor (DAG; used only when no
    step carries direct evidence, to rank purely structural suspects)."""
    dist, _ = ancestors_with_distance(trace, symptom)
    order = [s.step_id for s in trace.steps if s.step_id in dist]
    inc = incoming(trace)
    paths_in: dict[str, int] = {}
    for sid in order:  # trace order is a topological order for a recorded run
        preds = [e.src for e in inc.get(sid, []) if e.src in dist]
        # An imported trace may declare a read that points downstream (FR-ATT-03). A predecessor
        # not yet counted contributes nothing rather than raising: the walk stays finite and the
        # share is computed from the acyclic part.
        paths_in[sid] = sum(paths_in.get(p, 0) for p in preds) if preds else 1
    paths_out: dict[str, int] = {symptom: 1}
    for sid in reversed(order):
        if sid == symptom:
            continue
        succs = [e.dst for e in edges(trace) if e.src == sid and e.dst in dist]
        paths_out[sid] = sum(paths_out.get(d, 0) for d in succs)
    total = paths_in.get(symptom, 1) or 1
    return {sid: min(1.0, paths_in[sid] * paths_out.get(sid, 0) / total) for sid in order}
