"""Verification experiment orchestration on a toy workflow (TC-VER-01..05)."""

from __future__ import annotations

from dataclasses import replace

import pytest

from granite_core.checks import CheckDef
from granite_core.experiment import run_experiment
from granite_core.runner import run_workflow
from granite_core.verification import RepairRule, ReplayUnavailable, Verdict
from tests.test_runner import AddOne, Scripted, make_defn

OUTCOME = CheckDef(id="CHK-1", name="message carries 2n", type="assert", scope="outcome", step="s3",
                   expression="approx(number_in(s3.message), task.n * 2)")


def toy():
    return replace(make_defn(), checks=[OUTCOME], repairs={"s1": [RepairRule(field="n", expression="task.n * 2")]})


def poisoned():
    return run_workflow(toy(), {"n": 5}, Scripted(), fault=AddOne()).trace


def test_fixing_the_poisoned_step_is_confirmed_and_controls_stay_broken() -> None:
    exp = run_experiment(toy(), poisoned(), "s1", Scripted(), n=4, m=2, target_check_ids=["CHK-1"])
    assert exp.summary.verdict is Verdict.CONFIRMED and (exp.summary.k_pass, exp.summary.c_pass) == (4, 0)
    assert [r.kind for r in exp.replays] == ["intervention"] * 4 + ["control"] * 2
    assert len({r.seed for r in exp.replays}) == 6  # every replay and control gets its own seed


def test_fixing_an_innocent_step_is_refuted() -> None:
    defn = replace(toy(), repairs={"s2": [RepairRule(field="n", expression="s1.n")]})
    exp = run_experiment(defn, poisoned(), "s2", Scripted(), n=3, m=1, target_check_ids=["CHK-1"])
    assert exp.summary.verdict is Verdict.REFUTED


def test_endpoint_failure_midway_yields_error_not_a_verdict() -> None:
    exp = run_experiment(toy(), poisoned(), "s1", Scripted(fail_on=3), n=3, m=1, target_check_ids=["CHK-1"])
    assert exp.summary.verdict is Verdict.ERROR
    assert any(not r.completed and r.judgement is None for r in exp.replays)


def test_no_repair_rule_means_replay_unavailable() -> None:
    with pytest.raises(ReplayUnavailable, match="no repair rule"):
        run_experiment(replace(toy(), repairs={}), poisoned(), "s1", Scripted(), n=1, m=0, target_check_ids=["CHK-1"])


def test_callback_receives_each_replay_in_order_and_original_is_untouched() -> None:
    trace, seen = poisoned(), []
    before = trace.model_dump_json()
    run_experiment(toy(), trace, "s1", Scripted(), n=2, m=1, target_check_ids=["CHK-1"], on_replay=seen.append)
    assert [(r.kind, r.index) for r in seen] == [("intervention", 0), ("intervention", 1), ("control", 0)]
    assert trace.model_dump_json() == before


def test_an_explicit_intervention_overrides_the_repair_rules() -> None:
    from granite_core.verification import Intervention

    custom = Intervention(step_id="s1", patches={"n": 10}, source="user", description="analyst override")
    exp = run_experiment(replace(toy(), repairs={}), poisoned(), "s1", Scripted(), n=2, m=0,
                         target_check_ids=["CHK-1"], intervention=custom)
    assert exp.intervention.source == "user" and exp.summary.verdict is Verdict.CONFIRMED
