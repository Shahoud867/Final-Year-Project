"""Trace contract (TC-IMP) and checks engine (TC-CHK-01..06)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from granite_core.checks import (
    CheckDef,
    CheckStatus,
    derive_findings,
    evaluate_check,
    evaluate_checks,
    validate_expression,
)
from granite_core.dsl import DSLSyntaxError
from granite_core.trace import RunInfo, Step, TraceV1, split_read

from .conftest import CHECKS, make_trace

# ---- trace schema --------------------------------------------------------------------------------------


def _t(steps: list[Step]) -> TraceV1:
    return TraceV1(run=RunInfo(workflow="w"), steps=steps)


def test_valid_trace_roundtrips_through_json() -> None:
    t = make_trace()
    assert TraceV1.model_validate_json(t.model_dump_json()) == t


def test_duplicate_step_ids_rejected() -> None:
    s = Step(step_id="a", agent="A", kind="code")
    with pytest.raises(ValidationError, match="duplicate step_id"):
        _t([s, s])


def test_read_of_a_later_or_unknown_step_rejected() -> None:
    with pytest.raises(ValidationError, match="not an earlier step"):
        _t(
            [
                Step(step_id="a", agent="A", kind="code", reads=["b.x"]),
                Step(step_id="b", agent="B", kind="code"),
            ]
        )
    with pytest.raises(ValidationError, match="not an earlier step"):
        _t([Step(step_id="a", agent="A", kind="code", reads=["ghost.x"])])


@pytest.mark.parametrize("bad", ["nofield", "a.b.c", ".x", "x."])
def test_malformed_read_reference_rejected(bad: str) -> None:
    with pytest.raises(ValueError):
        split_read(bad)
    with pytest.raises(ValidationError):
        _t([Step(step_id="a", agent="A", kind="code", reads=[bad])])


def test_task_reads_are_allowed() -> None:
    _t([Step(step_id="a", agent="A", kind="code", reads=["task.message"])])


def test_unknown_fields_and_bad_ids_rejected() -> None:
    with pytest.raises(ValidationError):
        Step(step_id="a b", agent="A", kind="code")
    with pytest.raises(ValidationError):
        Step(step_id="a", agent="A", kind="code", surprise=1)  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        Step(step_id="a", agent="A", kind="wizard")  # type: ignore[arg-type]


def test_step_limit_enforced() -> None:
    steps = [Step(step_id=f"s{i}", agent="A", kind="code") for i in range(501)]
    with pytest.raises(ValidationError):
        _t(steps)
    assert len(_t(steps[:500]).steps) == 500


# ---- checks engine ---------------------------------------------------------------------------------------


def test_outcome_check_fails_on_stale_price_and_reports_observed_vs_expected(truth) -> None:
    r = evaluate_check(CHECKS[0], make_trace(stale=True), truth)
    assert r.status is CheckStatus.FAIL
    assert r.observed == 43.0 and r.expected == 43.25  # TC-CHK-01
    assert "observed 43.0" in r.message


def test_outcome_check_passes_on_clean_run(truth) -> None:
    assert evaluate_check(CHECKS[0], make_trace(), truth).status is CheckStatus.PASS  # TC-CHK-02


def test_step_contracts_localise_the_fault(truth) -> None:
    res = {r.check_id: r.status for r in evaluate_checks(make_trace(stale=True), CHECKS, truth)}
    assert res == {
        "CHK-OUT-1": CheckStatus.FAIL,
        "CT-LOOKUP": CheckStatus.FAIL,
        "CT-CALC": CheckStatus.PASS,
        "CT-WRITER": CheckStatus.PASS,
    }


def test_calculator_slip_fails_its_own_contract_not_the_lookup(truth) -> None:
    res = {r.check_id: r.status for r in evaluate_checks(make_trace(calc_slip=True), CHECKS, truth)}
    assert res["CT-LOOKUP"] is CheckStatus.PASS and res["CT-CALC"] is CheckStatus.FAIL


def test_missing_field_abstains_never_passes(truth) -> None:  # TC-CHK-03
    bad = CheckDef(id="X", name="x", scope="step", step="s2", expression="s2.no_such_field == 1")
    r = evaluate_check(bad, make_trace(), truth)
    assert r.status is CheckStatus.ABSTAIN and "no_such_field" in r.message


def test_unknown_step_abstains(truth) -> None:
    bad = CheckDef(id="X", name="x", scope="step", step="s99", expression="1 == 1")
    assert evaluate_check(bad, make_trace(), truth).status is CheckStatus.ABSTAIN


def test_type_problems_and_non_boolean_results_are_errors(truth) -> None:
    assert (
        evaluate_check(
            CheckDef(id="X", name="x", scope="step", step="s2", expression="'a' + 1"), make_trace(), truth
        ).status
        is CheckStatus.ERROR
    )
    r = evaluate_check(CheckDef(id="X", name="x", scope="step", step="s2", expression="1 + 1"), make_trace(), truth)
    assert r.status is CheckStatus.ERROR and "true or false" in r.message


def test_invalid_expression_is_an_error_result_not_a_crash(truth) -> None:
    r = evaluate_check(
        CheckDef(id="X", name="x", scope="step", step="s2", expression="__import__('os')"),
        make_trace(),
        truth,
    )
    assert r.status is CheckStatus.ERROR and "invalid check" in r.message


def test_broken_truth_source_yields_error(truth) -> None:
    def down(_: list[str]) -> float:
        raise ConnectionError("db down")

    r = evaluate_check(CHECKS[0], make_trace(), {**truth, "catalog_total": down})
    assert r.status is CheckStatus.ERROR


def test_disabled_checks_are_not_evaluated(truth) -> None:
    off = CHECKS[0].model_copy(update={"enabled": False})
    assert evaluate_checks(make_trace(stale=True), [off], truth) == []


def test_results_carry_a_reproducible_computation(truth) -> None:  # TC-CHK-06
    t = make_trace(stale=True)
    first = evaluate_check(CHECKS[0], t, truth)
    again = evaluate_check(CHECKS[0], t, truth)
    assert first.model_dump() == again.model_dump()
    comp = first.computation
    assert comp["truth_calls"][0]["function"] == "catalog_total" and "s5.message" in comp["resolved"]


def test_validate_expression_gate() -> None:
    validate_expression("approx(1, 1)")
    with pytest.raises(DSLSyntaxError):
        validate_expression("open('x')")


# ---- findings ---------------------------------------------------------------------------------------------


def test_failed_outcome_check_on_completed_run_is_a_silent_failure(truth) -> None:  # TC-CHK-05
    t = make_trace(stale=True)
    specs = derive_findings(t, evaluate_checks(t, CHECKS, truth))
    assert len(specs) == 1 and specs[0].kind == "silent_failure"
    assert specs[0].check_id == "CHK-OUT-1" and specs[0].symptom_step == "s5" and specs[0].severity == "high"


def test_clean_run_opens_no_finding(truth) -> None:  # TC-UI-02 (clean run)
    t = make_trace()
    assert derive_findings(t, evaluate_checks(t, CHECKS, truth)) == []


def test_step_contract_failure_alone_does_not_open_a_finding(truth) -> None:
    t = make_trace(message_slip=True)  # only CT-WRITER and CHK-OUT-1 fail; CT-* alone never open one
    results = [r for r in evaluate_checks(t, CHECKS, truth) if r.scope == "step"]
    assert derive_findings(t, results) == []


def test_errored_run_opens_an_explicit_error_finding() -> None:
    t = make_trace()
    t.run.status = "errored"
    t.steps[2].error = "ProviderUnavailable: timeout"
    specs = derive_findings(t, [])
    assert specs[0].kind == "explicit_error" and specs[0].symptom_step == "s3"
