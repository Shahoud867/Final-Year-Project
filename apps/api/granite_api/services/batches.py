"""Fault Lab: generate many runs (chosen faults and clean runs on chosen example tasks) in one action (F12)."""

from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.orm import Session, sessionmaker

from ..config import Settings
from ..db import session_scope
from ..errors import ProblemError
from ..jobs import JobHandle
from ..llm_factory import resolve_mode
from ..models import Batch, BatchRun, Run, new_id, now
from .common import audit
from .runs import create_run, entry_for, run_job

MAX_BATCH_RUNS = 120


class _Quiet:
    """Swallows a single run's own progress; the batch reports progress per run instead."""

    def progress(self, done: int, total: int, message: str = "") -> None:
        return None


def create_batch(
    session: Session, settings: Settings, workflow: str, faults: list[str], task_ids: list[str] | None, seed: int,
    mode: str | None, actor: str = "analyst",
) -> Batch:
    """Validate the request and queue one run per (task, fault) pair, clean runs written as fault 'none'."""
    entry = entry_for(workflow)
    allowed = {"none", *entry.fault_types}
    unknown = sorted(set(faults) - allowed)
    if unknown:
        raise ProblemError(422, "Unknown fault", f"Not available: {', '.join(unknown)}. "
                                                 f"Choose from: {', '.join(sorted(allowed))}.")
    ordered = list(dict.fromkeys(faults))  # keep the user's order, drop repeats
    examples = entry.examples()
    if task_ids is not None:
        wanted = list(dict.fromkeys(task_ids))
        known = {t["order_id"] for t in examples}
        missing = [t for t in wanted if t not in known]
        if missing:
            raise ProblemError(422, "Unknown task", f"Not an example task: {', '.join(missing)}.")
        examples = [t for t in examples if t["order_id"] in wanted]
    if not examples:
        raise ProblemError(422, "No tasks", "Choose at least one task.")
    total = len(examples) * len(ordered)
    if total > MAX_BATCH_RUNS:
        raise ProblemError(422, "Batch too large", f"{total} runs requested; the limit is {MAX_BATCH_RUNS}.")
    batch = Batch(id=new_id("bat"), workflow_key=entry.key, status="queued",
                  llm_mode=resolve_mode(settings, mode), faults=ordered, task_count=len(examples), seed=seed)
    session.add(batch)
    session.flush()
    position = 0
    for task in examples:
        clean = {k: task[k] for k in ("message", "email", "order_id")}
        for fault in ordered:
            run = create_run(session, settings, entry.key, clean, None if fault == "none" else fault, seed,
                             batch.llm_mode, actor)
            session.add(BatchRun(batch_id=batch.id, run_id=run.id, position=position))
            position += 1
    session.flush()
    audit(session, actor, "batch_created", "batch", batch.id, workflow=entry.key, faults=ordered,
          tasks=len(examples), runs=total, mode=batch.llm_mode)
    return batch


def batch_job(factory: sessionmaker[Session], settings: Settings, batch_id: str) -> Callable[[JobHandle], None]:
    """Return the job that executes the batch's runs one after another."""

    def job(handle: JobHandle) -> None:
        with session_scope(factory) as s:
            batch = s.get(Batch, batch_id)
            assert batch is not None
            batch.status = "running"
            run_ids = [r.run_id for r in s.query(BatchRun).filter(BatchRun.batch_id == batch_id)
                       .order_by(BatchRun.position)]
        total = len(run_ids)
        handle.progress(0, total, "starting")
        for i, run_id in enumerate(run_ids, start=1):
            try:
                run_job(factory, settings, run_id)(_Quiet())  # type: ignore[arg-type]
            except Exception:  # one broken run must not stop the batch; the run row keeps its own error
                with session_scope(factory) as s:
                    run = s.get(Run, run_id)
                    if run is not None and run.status in ("queued", "running"):
                        run.status, run.error, run.finished_at = "errored", "the run failed unexpectedly", now()
            handle.progress(i, total, f"run {i} of {total} finished")
        with session_scope(factory) as s:
            batch = s.get(Batch, batch_id)
            assert batch is not None
            batch.status, batch.finished_at = "done", now()
            audit(s, "system", "batch_finished", "batch", batch_id, runs=total)

    return job


__all__ = ["MAX_BATCH_RUNS", "batch_job", "create_batch"]
