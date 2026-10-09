"""Fault injection, detection, attribution and verification on the real workflow definition (TC-FLT, TC-VER)."""

from __future__ import annotations

import pytest
from granite_core.attribution import attribute
from granite_core.checks import CheckStatus, derive_findings, evaluate_checks
from granite_core.experiment import run_experiment
from granite_core.runner import run_workflow
from granite_core.verification import ReplayUnavailable, Verdict

from refund_desk import make_fault
from tests.conftest import FakeModel


def statuses(defn, trace):
    return {r.check_id: r.status for r in evaluate_checks(trace, defn.checks, defn.truth())}


def run(defn, task, fault=None, model=None, seed=1):
    return run_workflow(defn, task, model or FakeModel(), fault=make_fault(fault), seed=seed)


class TestCleanRun:
    def test_every_check_passes_and_no_finding(self, defn, task):
        out = run(defn, task)
        assert set(statuses(defn, out.trace).values()) == {CheckStatus.PASS}
        assert derive_findings(out.trace, evaluate_checks(out.trace, defn.checks, defn.truth())) == []

    def test_same_seed_same_trace(self, defn, task):
        a, b = run(defn, task, seed=7), run(defn, task, seed=7)
        assert [s.outputs for s in a.trace.steps] == [s.outputs for s in b.trace.steps]

    def test_refused_order_does_not_raise_false_findings(self, defn, tasks):
        t = next(t for t in tasks if "(pending)" in t["label"])
        out = run(defn, {k: t[k] for k in ("message", "email", "order_id")})
        res = statuses(defn, out.trace)
        assert res["CHK-OUT-2"] is CheckStatus.PASS and CheckStatus.FAIL not in res.values()


class TestStalePriceFault:
    def test_fault_is_silent_and_recorded_as_ground_truth(self, defn, task):
        out = run(defn, task, "stale_price")
        assert out.trace.run.status == "completed" and all(s.error is None for s in out.trace.steps)
        assert out.fault and out.fault.target_step == "s2" and out.fault.field_path.startswith("items[")
        assert out.fault.injected_value < out.fault.original_value

    def test_fault_hits_a_requested_item_not_just_the_first(self, defn, store, tasks):
        """Pick an order whose requested item is not the first line, so a naive 'items[0]' fault would miss it."""
        for oid in sorted(store.orders):
            o = store.orders[oid]
            names = [i["name"] for i in o["items"]]
            if o["status"] == "delivered" and len(set(names)) == len(names) and len(names) >= 3:
                msg = f"Please return the {names[2]} from order {oid}."
                out = run(defn, {"message": msg, "email": store.users[o["user_id"]]["email"], "order_id": oid}, "stale_price")
                assert out.fault.field_path == "items[2].price"
                assert statuses(defn, out.trace)["CHK-OUT-1"] is CheckStatus.FAIL
                return
        pytest.skip("no suitable order in the snapshot")

    def test_outcome_and_lookup_checks_fail_but_downstream_steps_stay_consistent(self, defn, task):
        res = statuses(defn, run(defn, task, "stale_price").trace)
        assert res["CHK-OUT-1"] is CheckStatus.FAIL and res["CT-LOOKUP"] is CheckStatus.FAIL
        assert {res[c] for c in ("CT-INTAKE", "CT-POLICY", "CT-CALC", "CT-WRITER", "CHK-OUT-2")} == {CheckStatus.PASS}

    def test_exactly_one_silent_failure_finding(self, defn, task):
        out = run(defn, task, "stale_price")
        findings = derive_findings(out.trace, evaluate_checks(out.trace, defn.checks, defn.truth()))
        assert [f.kind for f in findings] == ["silent_failure"]

    def test_attribution_ranks_the_injected_step_first_without_seeing_the_fault(self, defn, task):
        out = run(defn, task, "stale_price")
        results = evaluate_checks(out.trace, defn.checks, defn.truth())
        top = attribute(out.trace, results, "s5")[0]
        assert top.step_id == out.fault.target_step == "s2" and top.method == "provenance"

    def test_unknown_fault_name_is_rejected(self):
        with pytest.raises(ValueError, match="unknown fault"):
            make_fault("cosmic_ray")
        assert make_fault(None) is None and make_fault("none") is None


class TestNaturalSlips:
    def test_calculator_slip_is_attributed_to_the_calculator(self, defn, task):
        out = run(defn, task, model=FakeModel(calc_slip=0.5))
        res = statuses(defn, out.trace)
        assert res["CT-CALC"] is CheckStatus.FAIL and res["CT-LOOKUP"] is CheckStatus.PASS
        results = evaluate_checks(out.trace, defn.checks, defn.truth())
        assert attribute(out.trace, results, "s5")[0].step_id == "s4"

    def test_writer_misquoting_the_amount_is_attributed_to_the_writer(self, defn, task):
        out = run(defn, task, model=FakeModel(message_slip=True))
        res = statuses(defn, out.trace)
        assert res["CT-WRITER"] is CheckStatus.FAIL and res["CT-CALC"] is CheckStatus.PASS
        results = evaluate_checks(out.trace, defn.checks, defn.truth())
        assert attribute(out.trace, results, "s5")[0].step_id == "s5"


class TestVerificationExperiment:
    @pytest.fixture
    def faulty(self, defn, task):
        out = run(defn, task, "stale_price")
        return out.trace, evaluate_checks(out.trace, defn.checks, defn.truth())

    def test_true_origin_is_confirmed(self, defn, faulty):
        trace, _ = faulty
        exp = run_experiment(defn, trace, "s2", FakeModel(), n=5, m=2, target_check_ids=["CHK-OUT-1"])
        assert exp.summary.verdict is Verdict.CONFIRMED
        assert (exp.summary.k_pass, exp.summary.c_pass) == (5, 0)
        assert len(exp.replays) == 7 and all(r.completed for r in exp.replays)

    def test_innocent_step_is_refuted(self, defn, faulty):
        trace, _ = faulty
        exp = run_experiment(defn, trace, "s4", FakeModel(), n=5, m=2, target_check_ids=["CHK-OUT-1"])
        assert exp.summary.verdict is Verdict.REFUTED and exp.summary.k_pass == 0

    def test_replays_never_touch_the_original_trace(self, defn, faulty):
        trace, _ = faulty
        before = trace.model_dump_json()
        run_experiment(defn, trace, "s2", FakeModel(), n=2, m=1, target_check_ids=["CHK-OUT-1"])
        assert trace.model_dump_json() == before

    def test_frozen_steps_are_copied_and_cost_no_model_calls(self, defn, faulty):
        trace, _ = faulty
        model = FakeModel()
        run_experiment(defn, trace, "s2", model, n=1, m=0, target_check_ids=["CHK-OUT-1"])
        assert model.calls == 2  # only s4 (calculator) and s5 (writer) are re-executed

    def test_endpoint_failure_gives_no_verdict_instead_of_a_wrong_one(self, defn, faulty):
        trace, _ = faulty
        exp = run_experiment(defn, trace, "s2", FakeModel(fail_after=3), n=5, m=2, target_check_ids=["CHK-OUT-1"])
        assert exp.summary.verdict is Verdict.ERROR
        assert exp.summary.n_completed < 5 and any(not r.completed for r in exp.replays)

    def test_step_without_a_repair_rule_cannot_be_replayed(self, defn, faulty):
        trace, _ = faulty
        with pytest.raises(ReplayUnavailable, match="no repair rule"):
            run_experiment(defn, trace, "s3", FakeModel(), n=1, m=0, target_check_ids=["CHK-OUT-1"])

    def test_on_replay_callback_sees_every_replay(self, defn, faulty):
        trace, _ = faulty
        seen = []
        run_experiment(defn, trace, "s2", FakeModel(), n=2, m=1, target_check_ids=["CHK-OUT-1"], on_replay=seen.append)
        assert [(r.kind, r.index) for r in seen] == [("intervention", 0), ("intervention", 1), ("control", 0)]
