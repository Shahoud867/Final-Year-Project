"""Check-derived interventions (ADR-011) and the investigation stop rule."""

from __future__ import annotations

from typing import Any

import pytest

from granite_core.checks import CheckDef, CheckStatus, evaluate_checks
from granite_core.interventions import derive_intervention
from granite_core.investigation import (
    MAX_BUDGET,
    VerifyOutcome,
    check_budget,
    investigate,
)
from granite_core.verification import Verdict

from .conftest import make_trace

ITEM_CHECK = CheckDef(
    id="CT-ITEMS", name="Lookup items match the catalogue", type="truth", scope="step", step="s2",
    expression="s2.items == truth.fix_prices(s2.items)",
)


def _results(trace: Any, checks: list[CheckDef], truth: dict[str, Any]) -> Any:
    return evaluate_checks(trace, checks, truth)


class TestDeriveIntervention:
    def test_equality_check_gives_the_expected_value(self, truth: dict[str, Any]) -> None:
        trace = make_trace(stale=True)
        res = _results(trace, [ITEM_CHECK], truth)
        iv = derive_intervention(trace, "s2", [ITEM_CHECK], res, truth)
        assert iv is not None and iv.source == "check" and iv.derived_from == ["CT-ITEMS"]
        assert iv.patches["items"][0]["price"] == 19.75
        assert "CT-ITEMS" in iv.description

    def test_approx_check_patches_the_field_on_either_side(self, checks: list[CheckDef], truth: dict[str, Any]) -> None:
        trace = make_trace(calc_slip=True)
        res = _results(trace, checks, truth)
        iv = derive_intervention(trace, "s4", checks, res, truth)
        assert iv is not None and iv.patches == {"refund_amount": pytest.approx(43.25)}
        flipped = CheckDef(id="CT-FLIP", name="flipped", scope="step", step="s4",
                           expression="approx(sum(pluck(s3.items_to_refund, 'price')), s4.refund_amount)")
        res2 = _results(trace, [flipped], truth)
        iv2 = derive_intervention(trace, "s4", [flipped], res2, truth)
        assert iv2 is not None and iv2.patches == {"refund_amount": pytest.approx(43.25)}

    def test_passing_check_gives_nothing(self, truth: dict[str, Any]) -> None:
        trace = make_trace()
        res = _results(trace, [ITEM_CHECK], truth)
        assert derive_intervention(trace, "s2", [ITEM_CHECK], res, truth) is None

    def test_total_only_check_cannot_be_inverted(self, checks: list[CheckDef], truth: dict[str, Any]) -> None:
        trace = make_trace(stale=True)
        res = _results(trace, checks, truth)
        assert any(r.check_id == "CT-LOOKUP" and r.status is CheckStatus.FAIL for r in res)
        assert derive_intervention(trace, "s2", checks, res, truth) is None  # sum(...) is not a field

    def test_only_false_conjuncts_are_patched(self, truth: dict[str, Any]) -> None:
        trace = make_trace(stale=True)
        both = CheckDef(id="CT-BOTH", name="both", type="truth", scope="step", step="s2",
                        expression="s2.status == 'delivered' and s2.items == truth.fix_prices(s2.items)")
        res = _results(trace, [both], truth)
        iv = derive_intervention(trace, "s2", [both], res, truth)
        assert iv is not None and list(iv.patches) == ["items"]

    def test_another_steps_field_is_never_patched(self, truth: dict[str, Any]) -> None:
        trace = make_trace(stale=True)
        other = CheckDef(id="CT-OTHER", name="other", type="truth", scope="step", step="s2",
                         expression="s3.items_to_refund == truth.fix_prices(s3.items_to_refund)")
        res = _results(trace, [other], truth)
        assert derive_intervention(trace, "s2", [other], res, truth) is None

    def test_unknown_step_gives_nothing(self, checks: list[CheckDef], truth: dict[str, Any]) -> None:
        trace = make_trace(stale=True)
        assert derive_intervention(trace, "s9", checks, _results(trace, checks, truth), truth) is None


def _verifier(verdicts: dict[str, Verdict | None]):  # type: ignore[no-untyped-def]
    calls: list[str] = []

    def verify(step_id: str) -> VerifyOutcome:
        calls.append(step_id)
        v = verdicts[step_id]
        return VerifyOutcome(verdict=v, replays_used=0 if v is None else 7, reason="" if v else "no patch")

    return verify, calls


class TestInvestigate:
    def test_stops_at_the_first_confirmed_suspect(self) -> None:
        verify, calls = _verifier({"s4": Verdict.REFUTED, "s2": Verdict.CONFIRMED, "s1": Verdict.CONFIRMED})
        out = investigate(["s4", "s2", "s1"], verify, cost=7, budget=21)
        assert out.outcome == "confirmed" and out.confirmed_step == "s2" and calls == ["s4", "s2"]
        assert out.replays_used == 14 and [a.status for a in out.attempts] == ["verified", "verified"]

    def test_unreplayable_suspects_cost_nothing(self) -> None:
        verify, calls = _verifier({"s3": None, "s2": Verdict.CONFIRMED})
        out = investigate(["s3", "s2"], verify, cost=7, budget=7)
        assert out.confirmed_step == "s2" and out.attempts[0].status == "skipped" and out.replays_used == 7

    def test_budget_marks_the_rest_not_reached(self) -> None:
        verify, calls = _verifier({"s4": Verdict.REFUTED, "s2": Verdict.CONFIRMED})
        seen: list[str] = []
        out = investigate(["s4", "s2"], verify, cost=7, budget=10, on_attempt=lambda a: seen.append(a.status))
        assert calls == ["s4"] and out.outcome == "exhausted" and seen == ["verified", "not_reached"]

    def test_nothing_replayable(self) -> None:
        verify, _ = _verifier({"s1": None})
        assert investigate(["s1"], verify, cost=7).outcome == "no_candidate"
        assert investigate([], verify, cost=7).outcome == "no_candidate"

    def test_budget_validation(self) -> None:
        check_budget(5, 2, 21)
        for n, m, b in [(0, 2, 21), (5, 9, 21), (5, 2, 6), (5, 2, MAX_BUDGET + 1)]:
            with pytest.raises(ValueError):
                check_budget(n, m, b)
        verify, _ = _verifier({})
        with pytest.raises(ValueError):
            investigate(["s1"], verify, cost=7, budget=3)
