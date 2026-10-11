"""Verification experiments: replay from a hypothesised step with and without the fix, decide with VR-1."""

from __future__ import annotations

from collections.abc import Callable

from granite_core.evidence import EvidenceType
from granite_core.experiment import ReplayRecord, run_experiment
from granite_core.lifecycle import Event
from granite_core.trace import TraceV1
from granite_core.verification import RULE_VERSION, ReplayUnavailable, Verdict, build_intervention
from sqlalchemy.orm import Session, sessionmaker

from ..config import Settings
from ..db import session_scope
from ..errors import ProblemError
from ..jobs import JobHandle
from ..llm_factory import build_provider, resolve_mode
from ..models import Experiment, Finding, Hypothesis, ReplayRow, Run, new_id, now
from .common import add_evidence, audit, move
from .runs import entry_for

BASE_SEED = 1000
VERDICT_EVENT = {
    Verdict.CONFIRMED: Event.VERDICT_CONFIRMED,
    Verdict.REFUTED: Event.VERDICT_REFUTED,
    Verdict.INCONCLUSIVE: Event.VERDICT_INCONCLUSIVE,
    Verdict.ERROR: Event.VERIFY_ERROR,
}


def create_experiment(
    session: Session, settings: Settings, hypothesis_id: str, n: int, m: int, mode: str | None, actor: str
) -> Experiment:
    """Validate and queue a verification; refuses a step with no repair rule or an illegal state."""
    hyp = session.get(Hypothesis, hypothesis_id)
    if hyp is None:
        raise ProblemError(404, "Hypothesis not found", f"There is no hypothesis '{hypothesis_id}'.")
    finding = session.get(Finding, hyp.finding_id)
    run = session.get(Run, finding.run_id) if finding else None
    assert finding is not None and run is not None and run.trace is not None
    entry = entry_for(run.workflow_key)
    defn = entry.build(run.model)
    trace = TraceV1.model_validate(run.trace)
    if build_intervention(trace, hyp.step_id, defn.repairs.get(hyp.step_id, []), defn.truth()) is None:
        raise ProblemError(
            422, "Cannot be verified automatically",
            f"This workflow defines no repair for step '{hyp.step_id}', so a replay would have nothing to test. "
            "Review the evidence instead.",
        )
    move(session, finding, Event.VERIFY_STARTED, actor)  # raises IllegalTransition (409) if not allowed now
    exp = Experiment(
        id=new_id("exp"), hypothesis_id=hyp.id, finding_id=finding.id, status="queued",
        llm_mode=resolve_mode(settings, mode), n=n, m=m, base_seed=BASE_SEED, rule_version=RULE_VERSION,
    )
    session.add(exp)
    session.flush()
    audit(session, actor, "experiment_created", "experiment", exp.id, hypothesis=hyp.id, n=n, m=m, mode=exp.llm_mode)
    return exp


def _store_replay(factory: sessionmaker[Session], exp_id: str, rec: ReplayRecord) -> None:
    with session_scope(factory) as s:
        s.add(ReplayRow(
            experiment_id=exp_id, kind=rec.kind, idx=rec.index, seed=rec.seed, completed=rec.completed,
            passed=None if rec.judgement is None else rec.judgement.passed,
            judgement=None if rec.judgement is None else rec.judgement.model_dump(mode="json"),
            results=[r.model_dump(mode="json") for r in rec.results],
            final_output=rec.trace.run.final_output,
        ))


def experiment_job(factory: sessionmaker[Session], settings: Settings, exp_id: str) -> Callable[[JobHandle], None]:
    """Return the job that runs the experiment and stores each replay as it finishes."""
    def job(handle: JobHandle) -> None:
        with session_scope(factory) as s:
            exp = s.get(Experiment, exp_id)
            assert exp is not None
            exp.status = "running"
            hyp = s.get(Hypothesis, exp.hypothesis_id)
            assert hyp is not None
            finding = s.get(Finding, exp.finding_id)
            assert finding is not None
            run = s.get(Run, finding.run_id)
            assert run is not None and run.trace is not None
            trace = TraceV1.model_validate(run.trace)
            step_id, n, m, mode, model, workflow = hyp.step_id, exp.n, exp.m, exp.llm_mode, run.model, run.workflow_key
            targets = [c.check_id for c in run.check_results if c.scope == "outcome" and c.status == "fail"]
        defn = entry_for(workflow).build(model)
        done = 0

        def on_replay(rec: ReplayRecord) -> None:
            nonlocal done
            done += 1
            _store_replay(factory, exp_id, rec)
            handle.progress(done, n + m, f"{rec.kind} {rec.index + 1} finished")

        handle.progress(0, n + m, "starting replays")
        try:
            result = run_experiment(
                defn, trace, step_id, build_provider(settings, mode), n, m, targets, BASE_SEED, on_replay
            )
        except ReplayUnavailable as exc:
            _fail(factory, exp_id, str(exc))
            return
        _finish(factory, exp_id, result, trace)

    return job


def _fail(factory: sessionmaker[Session], exp_id: str, message: str) -> None:
    with session_scope(factory) as s:
        exp = s.get(Experiment, exp_id)
        assert exp is not None
        exp.status, exp.error, exp.finished_at = "error", message, now()
        finding = s.get(Finding, exp.finding_id)
        assert finding is not None
        move(s, finding, Event.VERIFY_ERROR)


def _why_unfinished(result) -> str:  # type: ignore[no-untyped-def]
    """Explain replays that could not run because recorded mode holds no saved answer for them."""
    missed = [r for r in result.replays
              if not r.completed and any("never recorded" in (step.error or "") for step in r.trace.steps)]
    if not missed:
        return ""
    return (f" {len(missed)} replay(s) needed model answers that are not in the recording, so they could not run. "
            "Recorded mode only replays saved answers; verify this step with a live model.")


def _finish(factory, exp_id, result, trace) -> None:  # type: ignore[no-untyped-def]
    summary = result.summary
    summary = summary.model_copy(update={"explanation": summary.explanation + _why_unfinished(result)})
    with session_scope(factory) as s:
        exp = s.get(Experiment, exp_id)
        assert exp is not None
        hyp = s.get(Hypothesis, exp.hypothesis_id)
        finding = s.get(Finding, exp.finding_id)
        assert hyp is not None and finding is not None
        exp.status, exp.finished_at = "done", now()
        exp.verdict, exp.summary = summary.verdict.value, summary.model_dump(mode="json")
        exp.intervention = result.intervention.model_dump(mode="json")
        hyp.status = summary.verdict.value
        move(s, finding, VERDICT_EVENT[summary.verdict])
        seeds = {f"{r.kind}-{r.index + 1}": r.seed for r in result.replays}
        add_evidence(
            s, finding.run_id, finding.id, EvidenceType.VERDICT_COMPUTATION,
            f"Verdict for {hyp.agent}: {summary.verdict.value}",
            {"rule": RULE_VERSION, "summary": exp.summary, "intervention": exp.intervention, "seeds": seeds},
            reproduce=f"Re-run experiment {exp.id} with the same seeds; replays are deterministic given the recording",
        )
        add_evidence(
            s, finding.run_id, finding.id, EvidenceType.REPLAY_OUTPUT, f"Replay outputs for {hyp.agent}",
            {"replays": [
                {"kind": r.kind, "index": r.index, "seed": r.seed, "completed": r.completed,
                 "passed": None if r.judgement is None else r.judgement.passed,
                 "final_output": r.trace.run.final_output}
                for r in result.replays
            ]},
        )
        fixed = next((r for r in result.replays if r.kind == "intervention" and r.completed), None)
        if fixed is not None:
            add_evidence(
                s, finding.run_id, finding.id, EvidenceType.DIFF, f"Original vs fixed output ({hyp.agent})",
                {"original": trace.run.final_output, "with_fix": fixed.trace.run.final_output,
                 "patched": result.intervention.patches},
            )
        audit(s, "system", "experiment_finished", "experiment", exp.id, verdict=summary.verdict.value)
