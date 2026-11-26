"""Workflow runner: recorded inputs/lineage, faults, error handling, replay freezing (TC-RUN-01..04, TC-VER-03)."""

from __future__ import annotations

from typing import Any

from granite_core.checks import CheckDef
from granite_core.llm import Completion, LLMRequest, ProviderUnavailable
from granite_core.runner import (
    FaultRecord,
    StepContext,
    StepDef,
    StepFailed,
    WorkflowDef,
    execute_replay,
    run_workflow,
)
from granite_core.verification import Intervention, plan_replay


class Scripted:
    """Test double for a language model: answers from a function, counts calls, records the seeds it saw."""

    name = "scripted"

    def __init__(self, answer=lambda req: "ok", fail_on: int | None = None) -> None:
        self.answer, self.fail_on, self.calls, self.seeds = answer, fail_on, 0, []

    def complete(self, request: LLMRequest) -> Completion:
        self.calls += 1
        self.seeds.append(request.seed)
        if self.fail_on == self.calls:
            raise ProviderUnavailable("endpoint unreachable")
        return Completion(
            text=self.answer(request), model=request.model, provider="scripted", tokens_in=2, tokens_out=3
        )


def s_double(ctx: StepContext) -> dict[str, Any]:
    return {"n": ctx.inputs["task.n"] * 2}


def s_ask(ctx: StepContext) -> dict[str, Any]:
    c = ctx.ask(LLMRequest(messages=[{"role": "user", "content": f"n={ctx.inputs['s1.n']}"}], model="m"))
    return {"text": c.text, "n": ctx.inputs["s1.n"]}


def s_final(ctx: StepContext) -> dict[str, Any]:
    c = ctx.ask(LLMRequest(messages=[{"role": "user", "content": "say"}], model="m"))
    return {"message": f"{c.text}:{ctx.inputs['s2.n']}"}


def make_defn(fail_step: str | None = None) -> WorkflowDef:
    def boom(ctx: StepContext) -> dict[str, Any]:
        raise StepFailed("model returned unusable output")

    steps = [
        StepDef("s1", "Doubler", "code", "double", ["task.n"], boom if fail_step == "s1" else s_double),
        StepDef("s2", "Asker", "llm", "ask", ["s1.n"], boom if fail_step == "s2" else s_ask),
        StepDef("s3", "Finisher", "llm", "final", ["s2.n", "s2.text"], boom if fail_step == "s3" else s_final),
    ]
    return WorkflowDef(key="toy", title="Toy", steps=steps, checks=[], repairs={}, truth=dict)


class AddOne:
    fault_type = "stale_value"
    target_step = "s1"

    def apply(self, outputs: dict[str, Any], inputs: dict[str, Any]) -> tuple[dict[str, Any], FaultRecord]:
        orig = outputs["n"]
        return {**outputs, "n": orig + 1}, FaultRecord("stale_value", "s1", "n", orig, orig + 1)


def test_run_records_every_step_with_resolved_inputs_and_lineage() -> None:  # TC-RUN-01
    out = run_workflow(make_defn(), {"n": 5}, Scripted())
    t = out.trace
    assert t.run.status == "completed" and [s.step_id for s in t.steps] == ["s1", "s2", "s3"]
    assert t.steps[0].inputs == {"task.n": 5} and t.steps[1].inputs == {"s1.n": 10}
    assert t.steps[2].inputs == {"s2.n": 10, "s2.text": "ok"}
    assert all(s.started_at and s.ended_at and s.error is None for s in t.steps)
    assert t.run.final_output == {"message": "ok:10"}
    assert t.steps[1].model == "m" and t.steps[1].prompt_hash and t.steps[1].params["calls"] == 1


def test_fault_is_injected_after_the_step_and_recorded_as_ground_truth() -> None:  # TC-RUN-02
    out = run_workflow(make_defn(), {"n": 5}, Scripted(), fault=AddOne())
    assert out.trace.steps[0].outputs == {"n": 11}  # downstream steps consumed the bad value
    assert out.trace.steps[1].inputs == {"s1.n": 11}
    assert out.fault == FaultRecord("stale_value", "s1", "n", 10, 11)
    assert run_workflow(make_defn(), {"n": 5}, Scripted()).fault is None


def test_step_failure_ends_the_run_as_errored_and_keeps_the_partial_trace() -> None:
    out = run_workflow(make_defn(fail_step="s2"), {"n": 5}, Scripted())
    t = out.trace
    assert t.run.status == "errored" and [s.step_id for s in t.steps] == ["s1", "s2"]
    assert "unusable output" in (t.steps[1].error or "") and t.run.final_output == {}


def test_provider_outage_is_an_errored_run_not_a_crash() -> None:  # TC-RUN-03
    out = run_workflow(make_defn(), {"n": 5}, Scripted(fail_on=1))
    assert out.trace.run.status == "errored"
    assert "ProviderUnavailable" in (out.trace.steps[1].error or "")


def test_a_step_that_needs_a_model_fails_cleanly_without_one() -> None:
    out = run_workflow(make_defn(), {"n": 5}, None)
    assert out.trace.run.status == "errored" and "needs a language model" in (out.trace.steps[1].error or "")


def test_seed_is_passed_to_every_model_call() -> None:
    p = Scripted()
    run_workflow(make_defn(), {"n": 5}, p, seed=42)
    assert p.seeds == [42, 42]


# ---- replay -----------------------------------------------------------------------------------------------


def test_replay_reuses_frozen_steps_without_calling_the_model_for_them() -> None:  # TC-VER-03
    defn = make_defn()
    first_model = Scripted()
    original = run_workflow(defn, {"n": 5}, first_model, fault=AddOne()).trace  # s1 poisoned: n=11
    assert first_model.calls == 2
    plan = plan_replay(original, Intervention(step_id="s1", patches={"n": 10}, source="truth"))
    assert plan.frozen == ["s1"] and plan.replay == ["s2", "s3"]

    replay_model = Scripted()
    rep = execute_replay(defn, original, plan, replay_model, seed=7, with_intervention=True).trace
    assert replay_model.calls == 2  # only s2 and s3 called a model
    assert rep.steps[0].outputs == {"n": 10}  # patched
    assert rep.steps[1].inputs == {"s1.n": 10} and rep.run.final_output == {"message": "ok:10"}
    assert replay_model.seeds == [7, 7]
    assert original.steps[0].outputs == {"n": 11}  # the stored original is untouched


def test_control_replay_keeps_the_original_value() -> None:
    defn = make_defn()
    original = run_workflow(defn, {"n": 5}, Scripted(), fault=AddOne()).trace
    plan = plan_replay(original, Intervention(step_id="s1", patches={"n": 10}, source="truth"))
    ctrl = execute_replay(defn, original, plan, Scripted(), seed=9, with_intervention=False).trace
    assert ctrl.steps[0].outputs == {"n": 11} and ctrl.run.final_output == {"message": "ok:11"}


def test_replay_that_hits_an_outage_is_errored_and_partial() -> None:
    defn = make_defn()
    original = run_workflow(defn, {"n": 5}, Scripted()).trace
    plan = plan_replay(original, Intervention(step_id="s1", patches={"n": 1}, source="user"))
    rep = execute_replay(defn, original, plan, Scripted(fail_on=2), seed=1, with_intervention=True).trace
    assert rep.run.status == "errored" and [s.step_id for s in rep.steps] == ["s1", "s2", "s3"]
    assert rep.steps[2].error


def test_replaying_a_late_step_re_executes_only_what_follows() -> None:
    defn = make_defn()
    original = run_workflow(defn, {"n": 5}, Scripted()).trace
    plan = plan_replay(original, Intervention(step_id="s2", patches={"text": "patched"}, source="user"))
    model = Scripted()
    rep = execute_replay(defn, original, plan, model, seed=3, with_intervention=True).trace
    assert model.calls == 1 and rep.steps[1].outputs["text"] == "patched"


def test_checkdef_import_is_available_to_workflow_definitions() -> None:
    assert CheckDef(id="X", name="x", scope="step", step="s1", expression="1 == 1").enabled


class SeesUpstream:
    """A fault that needs something its target step never declared as a read (the harness may see everything)."""

    fault_type = "peek"
    target_step = "s2"
    seen: dict[str, Any] = {}

    def apply(self, outputs: dict[str, Any], inputs: dict[str, Any]) -> tuple[dict[str, Any], FaultRecord]:
        SeesUpstream.seen = dict(inputs)
        return outputs, FaultRecord("peek", "s2", "n", outputs["n"], outputs["n"])


def test_fault_sees_the_task_and_all_earlier_outputs_not_only_declared_reads() -> None:
    out = run_workflow(make_defn(), {"n": 5}, Scripted(), fault=SeesUpstream())
    assert out.trace.steps[1].inputs == {"s1.n": 10}  # what the step recorded is unchanged
    assert SeesUpstream.seen == {"task.n": 5, "s1.n": 10}
