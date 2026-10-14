"""Provenance attribution: golden traces, clean runs, metamorphic invariances, determinism (TC-ATT-01..05)."""

from __future__ import annotations

import copy

from granite_core.attribution import attribute
from granite_core.checks import evaluate_checks
from granite_core.trace import TraceV1

from .conftest import CHECKS, make_trace


def _attr(t: TraceV1, truth, symptom: str = "s5"):
    return attribute(t, evaluate_checks(t, CHECKS, truth), symptom)


def test_stale_price_is_traced_to_the_lookup_not_the_step_where_it_surfaced(truth) -> None:  # TC-ATT-01
    hyps = _attr(make_trace(stale=True), truth)
    assert hyps[0].step_id == "s2" and hyps[0].evidence_kind == "truth_mismatch" and hyps[0].method == "provenance"
    assert hyps[0].rank == 1 and hyps[0].score == round(0.9**3, 3)
    assert "contradicts the source of truth" in hyps[0].rationale
    by = {h.step_id: h for h in hyps}
    assert by["s4"].evidence_kind == "consistent" and by["s4"].score < 0.1  # the naive "blame the calculator" suspect
    path = hyps[0].evidence[0]
    assert path["type"] == "provenance_path" and [p["step_id"] for p in path["path"]] == [
        "s2",
        "s3",
        "s4",
        "s5",
    ]


def test_natural_calculator_slip_is_traced_to_the_calculator(truth) -> None:  # TC-ATT-02
    hyps = _attr(make_trace(calc_slip=True), truth)
    assert hyps[0].step_id == "s4" and hyps[0].evidence_kind == "contract_fail"
    assert {h.step_id: h.evidence_kind for h in hyps}["s2"] == "consistent"


def test_writer_slip_is_traced_to_the_writer(truth) -> None:
    hyps = _attr(make_trace(message_slip=True), truth)
    assert hyps[0].step_id == "s5" and hyps[0].evidence_kind == "contract_fail"


def test_clean_run_has_no_origin_evidence(truth) -> None:  # TC-ATT-03
    hyps = _attr(make_trace(), truth)
    assert all(h.evidence_kind in ("consistent", "unknown") for h in hyps)
    assert {h.method for h in hyps} == {"structural"} and max(h.score for h in hyps) <= 0.5
    cleared = [h.score for h in hyps if h.evidence_kind == "consistent"]
    unchecked = [h.score for h in hyps if h.evidence_kind == "unknown"]
    assert max(cleared) <= min(unchecked)  # a step that passed its contract never outranks an unchecked one


def test_handoff_drift_is_detected_when_a_step_received_something_other_than_was_produced(truth) -> None:
    t = make_trace()
    t.steps[3].inputs["s3.items_to_refund"][0]["price"] = 1.0  # what the Calculator "received"
    results = [r for r in evaluate_checks(t, CHECKS, truth) if r.check_id != "CT-CALC"]  # no contract on s4
    hyps = attribute(t, results, "s5")
    s4 = next(h for h in hyps if h.step_id == "s4")
    assert s4.evidence_kind == "handoff_drift" and s4.score >= 0.4


def test_without_any_evidence_suspects_are_structural_and_scores_are_modest(truth) -> None:
    t = make_trace()
    hyps = attribute(t, [], "s5")  # no check results at all
    assert {h.method for h in hyps} == {"structural"} and all(h.score <= 0.5 for h in hyps)
    assert all("verify before trusting" in h.rationale for h in hyps)


def test_unknown_symptom_step_gives_no_hypotheses(truth) -> None:
    assert attribute(make_trace(), [], "nope") == []


# ---- metamorphic: relabelling and padding must not move the verdict ---------------------------------------


def test_renaming_agents_does_not_change_the_origin_step(truth) -> None:  # TC-ATT-04
    a = _attr(make_trace(stale=True), truth)[0].step_id
    b = _attr(make_trace(stale=True, agent_prefix="Zeta-"), truth)[0].step_id
    assert a == b == "s2"


def test_inserting_an_unrelated_step_does_not_change_the_origin(truth) -> None:
    t = make_trace(stale=True, extra_step=True)
    hyps = _attr(t, truth)
    assert hyps[0].step_id == "s2" and "x1" not in {h.step_id for h in hyps}


def test_scaling_all_prices_does_not_change_the_origin(truth) -> None:
    # a stale price is a stale price at any scale (the truth table is scaled by patching the check tolerance)
    t = make_trace(stale=True, scale=1.0)
    assert _attr(t, truth)[0].step_id == "s2"


# ---- determinism (NFR-05) ---------------------------------------------------------------------------------


def test_same_input_gives_byte_identical_output(truth) -> None:
    t = make_trace(stale=True)
    one = [h.model_dump_json() for h in _attr(t, truth)]
    two = [h.model_dump_json() for h in _attr(copy.deepcopy(t), truth)]
    assert one == two


def test_attribution_never_sees_fault_ground_truth() -> None:
    """The API takes only a trace, check results and a symptom step: there is no parameter that could carry
    the injected-fault record, so ground truth cannot leak into the hypotheses (FR-RUN-02)."""
    import inspect

    params = set(inspect.signature(attribute).parameters)
    assert params == {"trace", "results", "symptom_step"}


def test_rank_and_score_agree_so_the_table_reads_in_one_order(truth) -> None:  # TC-ATT-06 (D-25)
    """A reader compares the scores in the table; the ranking must not contradict them.

    Before this was fixed the rank key used the evidence weight alone while the score also
    decayed with distance from the symptom, so a far step could be ranked above a nearer one
    that showed a higher number (Intake 0.066 above Writer 0.100).
    """
    hyps = _attr(make_trace(stale=True), truth)
    scores = [h.score for h in hyps]
    assert scores == sorted(scores, reverse=True), f"rank disagrees with the displayed score: {scores}"
    assert [h.rank for h in hyps] == list(range(1, len(hyps) + 1))
