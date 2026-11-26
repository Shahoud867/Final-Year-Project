"""Verification protocol VR-1 (TC-VER-01..06): verdict decision table, CI, regression guard, replay planning."""

from __future__ import annotations

import copy

import pytest

from granite_core.checks import CheckResult, CheckStatus, evaluate_checks
from granite_core.verification import (
    Intervention,
    RepairRule,
    ReplayUnavailable,
    Verdict,
    build_intervention,
    decide,
    judge_replay,
    patched_outputs,
    plan_replay,
    summarize,
    wilson,
)

from .conftest import CHECKS, make_trace

C, R, INC, E = Verdict.CONFIRMED, Verdict.REFUTED, Verdict.INCONCLUSIVE, Verdict.ERROR

# (k, n, c, m, expected). The 20-row decision table from the master plan (TC-VER-01), pre-registered thresholds.
TABLE = [
    (5, 5, 0, 2, C),
    (4, 5, 0, 2, C),
    (4, 5, 1, 5, C),
    (5, 5, 1, 5, C),
    (5, 5, 0, 0, C),
    (4, 5, 1, 2, INC),
    (5, 5, 2, 2, INC),
    (4, 5, 2, 5, INC),  # intervention works but so do the controls: not stable
    (3, 5, 0, 2, INC),
    (2, 5, 0, 2, INC),
    (1, 5, 0, 2, R),
    (0, 5, 0, 2, R),
    (0, 5, 2, 2, R),
    (1, 5, 1, 2, R),
    (1, 3, 0, 2, INC),
    (0, 3, 0, 2, R),
    (3, 3, 0, 2, C),
    (2, 3, 0, 2, INC),
    (10, 10, 0, 2, C),
    (8, 10, 1, 5, C),
]


@pytest.mark.parametrize("k,n,c,m,expected", TABLE)
def test_vr1_decision_table(k: int, n: int, c: int, m: int, expected: Verdict) -> None:
    assert decide(k, n, c, m) is expected


def test_table_has_twenty_rows() -> None:
    assert len(TABLE) == 20


def test_threshold_boundaries() -> None:
    assert decide(4, 5, 1, 5) is C  # 0.8 and controls exactly 0.2: both inclusive
    assert decide(1, 5, 0, 2) is R  # exactly 0.2
    assert decide(2, 5, 0, 2) is INC  # just above the refute line


def test_unfinished_replays_give_error_never_a_verdict() -> None:
    assert decide(5, 5, 0, 2, completed=4) is E
    assert decide(5, 5, 0, 2, completed=5, completed_controls=1) is E
    with pytest.raises(ValueError):
        decide(0, 0, 0, 0)


def test_wilson_interval_properties() -> None:
    lo, hi = wilson(5, 5)
    assert 0.5 < lo < 1.0 and hi == 1.0
    lo, hi = wilson(0, 5)
    assert lo == 0.0 and 0 < hi < 0.5
    assert wilson(0, 0) == (0.0, 1.0)
    lo2, hi2 = wilson(50, 100)
    lo1, hi1 = wilson(5, 10)
    assert (hi2 - lo2) < (hi1 - lo1)  # more replays -> tighter interval


def test_summary_explains_each_verdict() -> None:
    s = summarize([True] * 5, [False, False], 5, 2)
    assert s.verdict is C and s.k_pass == 5 and s.c_pass == 0 and "luck" in s.explanation and s.rule_version == "VR-1"
    assert summarize([False] * 5, [False, False], 5, 2).verdict is R
    assert "Increase" in summarize([True, True, True, False, False], [False, False], 5, 2).explanation
    part = summarize([True, True, True], [False, False], 5, 2)
    assert part.verdict is E and part.n_completed == 3 and "no verdict" in part.explanation


def test_summary_rejects_out_of_range_plans() -> None:
    with pytest.raises(ValueError):
        summarize([], [], 0, 2)
    with pytest.raises(ValueError):
        summarize([True] * 11, [], 11, 0)


# ---- replay judging and the regression guard (TC-VER-02) ---------------------------------------------------


def _res(check_id: str, status: CheckStatus) -> CheckResult:
    return CheckResult(
        check_id=check_id,
        check_version=1,
        scope="outcome",
        step="s5",
        type="assert",
        severity="high",
        status=status,
    )


def test_replay_passes_when_target_fixed_and_nothing_broken() -> None:
    orig = [_res("OUT", CheckStatus.FAIL), _res("CALC", CheckStatus.PASS)]
    new = [_res("OUT", CheckStatus.PASS), _res("CALC", CheckStatus.PASS)]
    j = judge_replay(orig, new, ["OUT"])
    assert j.passed and j.fixed == ["OUT"] and not j.regressions


def test_replay_that_fixes_target_but_breaks_another_check_does_not_pass() -> None:
    orig = [_res("OUT", CheckStatus.FAIL), _res("WRITER", CheckStatus.PASS)]
    new = [_res("OUT", CheckStatus.PASS), _res("WRITER", CheckStatus.FAIL)]
    j = judge_replay(orig, new, ["OUT"])
    assert not j.passed and j.regressions == ["WRITER"]


def test_abstain_or_error_on_target_is_not_a_pass() -> None:
    for st in (CheckStatus.ABSTAIN, CheckStatus.ERROR, CheckStatus.FAIL):
        j = judge_replay([_res("OUT", CheckStatus.FAIL)], [_res("OUT", st)], ["OUT"])
        assert not j.passed and j.still_failing == ["OUT"]


def test_previously_passing_check_that_goes_missing_counts_as_regression() -> None:
    j = judge_replay(
        [_res("OUT", CheckStatus.FAIL), _res("W", CheckStatus.PASS)], [_res("OUT", CheckStatus.PASS)], ["OUT"]
    )
    assert not j.passed and j.regressions == ["W"]


# ---- interventions and replay planning -----------------------------------------------------------------------

RULES = {
    "s2": [RepairRule(field="items", expression="truth.fix_prices(s2.items)")],
    "s4": [RepairRule(field="refund_amount", expression="round(sum(pluck(s3.items_to_refund, 'price')), 2)")],
}


def test_intervention_for_the_faulty_step_restores_catalogue_prices(truth) -> None:
    iv = build_intervention(make_trace(stale=True), "s2", RULES["s2"], truth)
    assert iv is not None and iv.step_id == "s2" and iv.patches["items"][0]["price"] == 19.75


def test_intervention_for_a_consistent_step_is_a_no_op_so_the_hypothesis_will_be_refuted(truth) -> None:
    t = make_trace(stale=True)
    iv = build_intervention(t, "s4", RULES["s4"], truth)
    assert iv is not None and iv.patches["refund_amount"] == t.step("s4").outputs["refund_amount"]


def test_no_rule_or_failing_rule_gives_no_intervention(truth) -> None:
    t = make_trace()
    assert build_intervention(t, "s3", [], truth) is None
    assert build_intervention(t, "s3", [RepairRule(field="x", expression="s9.y")], truth) is None


def test_replay_plan_freezes_everything_up_to_the_intervention_step(truth) -> None:
    t = make_trace(stale=True)
    plan = plan_replay(t, build_intervention(t, "s2", RULES["s2"], truth))  # type: ignore[arg-type]
    assert plan.frozen == ["s1", "s2"] and plan.replay == ["s3", "s4", "s5"]


def test_replay_plan_rejects_unknown_step_or_field() -> None:
    t = make_trace()
    with pytest.raises(ReplayUnavailable):
        plan_replay(t, Intervention(step_id="zz", patches={"a": 1}, source="user"))
    with pytest.raises(ReplayUnavailable, match="no output field"):
        plan_replay(t, Intervention(step_id="s2", patches={"nope": 1}, source="user"))


def test_patched_outputs_does_not_mutate_the_original() -> None:
    t = make_trace(stale=True)
    before = copy.deepcopy(t.step("s2").outputs)
    out = patched_outputs(t.step("s2").outputs, Intervention(step_id="s2", patches={"status": "x"}, source="user"))
    assert out["status"] == "x" and t.step("s2").outputs == before


def test_a_patch_must_name_at_least_one_field() -> None:
    with pytest.raises(ValueError):
        Intervention(step_id="s2", patches={}, source="user")


def test_end_to_end_judging_of_a_patched_trace(truth) -> None:
    """Patch the stale price in the stored trace and confirm the outcome check now passes."""
    t = make_trace(stale=True)
    orig = evaluate_checks(t, CHECKS, truth)
    iv = build_intervention(t, "s2", RULES["s2"], truth)
    fixed = t.model_copy(deep=True)
    fixed.steps[1].outputs = patched_outputs(t.steps[1].outputs, iv)  # type: ignore[arg-type]
    fixed.steps[2].outputs["items_to_refund"][0]["price"] = 19.75  # what a re-run of Policy would produce
    fixed.steps[3].outputs["refund_amount"] = 43.25  # ... and the Calculator
    fixed.steps[4].outputs["message"] = "Your refund of $43.25 is on its way."
    fixed.steps[3].inputs["s3.items_to_refund"] = fixed.steps[2].outputs["items_to_refund"]
    j = judge_replay(orig, evaluate_checks(fixed, CHECKS, truth), ["CHK-OUT-1"])
    assert j.passed and "CT-LOOKUP" not in j.regressions
