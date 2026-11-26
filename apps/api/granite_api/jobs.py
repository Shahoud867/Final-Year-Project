"""Background jobs: a small thread pool with a persisted job row for progress and crash recovery."""

from __future__ import annotations

import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy.orm import Session, sessionmaker

from .db import session_scope
from .models import Experiment, Finding, Job, Run, new_id, now

log = logging.getLogger("granite.jobs")


class JobHandle:
    """Lets a running job report its progress."""
    def __init__(self, factory: sessionmaker[Session], job_id: str) -> None:
        self._factory, self.job_id = factory, job_id

    def progress(self, done: int, total: int, message: str = "") -> None:
        """Store how many units are done and an optional message."""
        with session_scope(self._factory) as s:
            job = s.get(Job, self.job_id)
            if job:
                job.progress_done, job.progress_total = done, total
                if message:
                    job.message = message


class JobRunner:
    """Runs jobs on a small thread pool (or inline) and keeps a database row per job."""
    def __init__(self, factory: sessionmaker[Session], inline: bool = False, max_workers: int = 2) -> None:
        self.factory, self.inline = factory, inline
        self._pool = None if inline else ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="granite-job")

    def submit(self, kind: str, target_id: str, fn: Callable[[JobHandle], None]) -> str:
        """Queue a job and return its id."""
        job_id = new_id("job")
        with session_scope(self.factory) as s:
            s.add(Job(id=job_id, kind=kind, target_id=target_id))
        if self._pool is None:
            self._execute(job_id, fn)
        else:
            self._pool.submit(self._execute, job_id, fn)
        return job_id

    def _execute(self, job_id: str, fn: Callable[[JobHandle], None]) -> None:
        with session_scope(self.factory) as s:
            job = s.get(Job, job_id)
            assert job is not None
            job.status, job.started_at = "running", now()
        try:
            fn(JobHandle(self.factory, job_id))
            status, message = "succeeded", ""
        except Exception as exc:  # the job function reports entity-level errors itself; this is the last resort
            log.exception("job %s failed", job_id)
            status, message = "failed", f"{type(exc).__name__}: {exc}"[:300]
        with session_scope(self.factory) as s:
            job = s.get(Job, job_id)
            assert job is not None
            job.status, job.finished_at = status, now()
            if message:
                job.message = message

    def shutdown(self) -> None:
        """Stop the pool without waiting for queued jobs."""
        if self._pool is not None:
            self._pool.shutdown(wait=False, cancel_futures=True)


def recover_interrupted(factory: sessionmaker[Session]) -> int:
    """After a restart nothing is really running: close dangling jobs so no screen waits forever."""
    note = "interrupted by a server restart; start it again"
    count = 0
    with session_scope(factory) as s:
        for job in s.query(Job).filter(Job.status.in_(["queued", "running"])):
            job.status, job.message, job.finished_at = "failed", note, now()
            count += 1
        for run in s.query(Run).filter(Run.status.in_(["queued", "running"])):
            run.status, run.error, run.finished_at = "errored", note, now()
        for exp in s.query(Experiment).filter(Experiment.status.in_(["queued", "running"])):
            exp.status, exp.error, exp.finished_at = "error", note, now()
            finding = s.get(Finding, exp.finding_id)
            if finding and finding.status == "verifying":
                finding.status = "hypothesized"
    return count
