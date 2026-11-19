"""Investigate: verify a finding's ranked suspects in order until one is confirmed or the budget is spent.

The stop rule lives in :mod:`granite_core.investigation`. This service supplies the ``verify`` step, which creates and
runs an ordinary experiment for each suspect, so every attempt is stored, hashed and shown exactly like a verification
started by hand.
"""

from __future__ import annotations

from collections.abc import Callable

from granite_core.experiment import plan_intervention
from granite_core.investigation import Attempt, VerifyOutcome, check_budget, investigate
from granite_core.lifecycle import Event, FindingStatus, allowed_events
from granite_core.trace import TraceV1
from granite_core.verification import Verdict
from sqlalchemy.orm import Session, sessionmaker

from ..config import Settings
from ..db import session_scope
from ..errors import ProblemError
from ..jobs import JobHandle
from ..llm_factory import resolve_mode
from ..models import Experiment, Finding, Investigation, Run, new_id, now
from .common import audit
from .experiments import create_experiment, experiment_job
from .runs import entry_for


def create_investigation(
    session: Session, settings: Settings, finding_id: str, n: int, m: int, budget: int, mode: str | None, actor: str
) -> Investigation:
    """Validate and queue an investigation; refuses a finding that cannot be verified now."""
    finding = session.get(Finding, finding_id)
    if finding is None:
        raise ProblemError(404, "Finding not found", f"There is no finding {finding_id}.")
    try:
        check_budget(n, m, budget)
    except ValueError as exc:
        raise ProblemError(422, "Invalid budget", str(exc)) from None
    if Event.VERIFY_STARTED not in allowed_events(FindingStatus(finding.status)):
        raise ProblemError(409, "Cannot investigate now",
                           f"A finding that is '{finding.status}' cannot be verified again.")
    if not finding.hypotheses:
        raise ProblemError(422, "Nothing to investigate", "This finding has no ranked suspects.")
    busy = session.query(Investigation).filter(
        Investigation.finding_id == finding_id, Investigation.status.in_(["queued", "running"])).first()
    if busy is not None:
        raise ProblemError(409, "Already investigating", f"Investigation {busy.id} is still running.")
    inv = Investigation(id=new_id("inv"), finding_id=finding_id, status="queued", llm_mode=resolve_mode(settings, mode),
                        n=n, m=m, budget=budget)
    session.add(inv)
    session.flush()
    audit(session, actor, "investigation_created", "investigation", inv.id, finding=finding_id, n=n, m=m,
          budget=budget, mode=inv.llm_mode)
    return inv


class _Relay:
    """Forwards an experiment's progress to the investigation's job, with the suspect's name in front."""

    def __init__(self, handle: JobHandle, label: str) -> None:
        self.handle, self.label = handle, label

    def progress(self, done: int, total: int, message: str = "") -> None:
        self.handle.progress(done, total, f"{self.label}: {message}" if message else self.label)


def investigation_job(factory: sessionmaker[Session], settings: Settings, inv_id: str) -> Callable[[JobHandle], None]:
    """Return the job that verifies the ranked suspects in order."""

    def job(handle: JobHandle) -> None:
        with session_scope(factory) as s:
            inv = s.get(Investigation, inv_id)
            assert inv is not None
            inv.status = "running"
            finding = s.get(Finding, inv.finding_id)
            assert finding is not None
            run = s.get(Run, finding.run_id)
            assert run is not None and run.trace is not None
            ranked = [(h.id, h.step_id, h.agent) for h in sorted(finding.hypotheses, key=lambda h: h.rank)]
            n, m, budget, mode = inv.n, inv.m, inv.budget, inv.llm_mode
            defn = entry_for(run.workflow_key).build(run.model)
            trace = TraceV1.model_validate(run.trace)
        by_step = {step: (hid, agent) for hid, step, agent in ranked}
        attempts: list[dict[str, object]] = []

        def verify(step_id: str) -> VerifyOutcome:
            hyp_id, agent = by_step[step_id]
            if plan_intervention(defn, trace, step_id) is None:
                return VerifyOutcome(verdict=None, reason=f"no failed check of {agent} says what its output should be")
            with session_scope(factory) as s:
                try:
                    exp = create_experiment(s, settings, hyp_id, n, m, mode, "investigation")
                except ProblemError as exc:
                    return VerifyOutcome(verdict=None, reason=exc.detail)
                exp_id = exp.id
            experiment_job(factory, settings, exp_id)(_Relay(handle, agent))  # type: ignore[arg-type]
            with session_scope(factory) as s:
                done = s.get(Experiment, exp_id)
                assert done is not None
                verdict = Verdict(done.verdict) if done.verdict else Verdict.ERROR
                reason = (done.summary or {}).get("explanation", "") or done.error
            return VerifyOutcome(verdict=verdict, replays_used=n + m, reason=reason, experiment_id=exp_id)

        def on_attempt(att: Attempt) -> None:
            hyp_id, agent = by_step[att.step_id]
            attempts.append({**att.model_dump(mode="json"), "hypothesis_id": hyp_id, "agent": agent})
            with session_scope(factory) as s:
                row = s.get(Investigation, inv_id)
                assert row is not None
                row.attempts = list(attempts)
                row.replays_used = sum(int(a.get("replays_used") or 0) for a in attempts)  # type: ignore[call-overload]

        try:
            result = investigate([step for _, step, _ in ranked], verify, n + m, budget, on_attempt)
        except Exception as exc:
            with session_scope(factory) as s:
                row = s.get(Investigation, inv_id)
                assert row is not None
                row.status, row.error, row.finished_at = "error", f"{type(exc).__name__}: {exc}"[:500], now()
            raise
        with session_scope(factory) as s:
            row = s.get(Investigation, inv_id)
            assert row is not None
            row.status, row.finished_at = "done", now()
            row.outcome, row.confirmed_step = result.outcome, result.confirmed_step
            row.replays_used = result.replays_used
            audit(s, "system", "investigation_finished", "investigation", inv_id, outcome=result.outcome,
                  confirmed_step=result.confirmed_step, replays=result.replays_used)
        handle.progress(result.replays_used, budget, f"finished: {result.outcome}")

    return job


__all__ = ["create_investigation", "investigation_job"]
