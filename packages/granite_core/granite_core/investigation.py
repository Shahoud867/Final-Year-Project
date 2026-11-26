"""Verified attribution: verify ranked suspects in order until one is confirmed or the replay budget runs out.

Attribution ranks suspects from recorded evidence; verification tests one suspect by controlled replay (VR-1). An
investigation chains the two: it walks the ranking from the top, skips a suspect that cannot be replayed (nothing
says what its correct output is), verifies the next one, and stops at the first CONFIRMED verdict. A replay budget
bounds the cost, because every replay may call a model.

This module only decides the order and when to stop. The caller supplies ``verify``, so the same rule drives the
API (which stores every experiment) and the evaluation harness (which does not).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from pydantic import BaseModel, Field

from .verification import MAX_CONTROLS, MAX_REPLAYS, Verdict

DEFAULT_BUDGET = 21  # three suspects at N=5, M=2
MAX_BUDGET = 60


class Attempt(BaseModel):
    """What happened to one suspect during an investigation."""

    step_id: str
    status: Literal["verified", "skipped", "not_reached"]
    verdict: Verdict | None = None
    replays_used: int = 0
    reason: str = ""
    experiment_id: str | None = None  # set by the API when the attempt was stored


class InvestigationResult(BaseModel):
    """The attempts in order, the confirmed origin if one was found, and the replays spent."""

    attempts: list[Attempt]
    outcome: Literal["confirmed", "exhausted", "no_candidate"]
    confirmed_step: str | None = None
    replays_used: int = 0
    budget: int = Field(ge=1)


class VerifyOutcome(BaseModel):
    """What ``verify`` reports for one suspect: a verdict, or None with the reason it could not run."""

    verdict: Verdict | None
    replays_used: int = 0
    reason: str = ""
    experiment_id: str | None = None


def check_budget(n: int, m: int, budget: int) -> None:
    """Raise ValueError unless one experiment fits the budget and the numbers are within the rule's limits."""
    if not 1 <= n <= MAX_REPLAYS or not 0 <= m <= MAX_CONTROLS:
        raise ValueError(f"n must be 1..{MAX_REPLAYS} and m 0..{MAX_CONTROLS}")
    if not n + m <= budget <= MAX_BUDGET:
        raise ValueError(f"the budget must cover at least one experiment ({n + m} replays) and be at most {MAX_BUDGET}")


def investigate(
    candidates: list[str],
    verify: Callable[[str], VerifyOutcome],
    cost: int,
    budget: int = DEFAULT_BUDGET,
    on_attempt: Callable[[Attempt], None] | None = None,
) -> InvestigationResult:
    """Verify ``candidates`` (ranked step ids, best first) in order; stop at the first CONFIRMED verdict.

    ``cost`` is the number of replays one experiment uses (N + M). A suspect is verified only if a whole experiment
    still fits the budget; the remaining suspects are then reported as not reached. A suspect that cannot be replayed
    costs nothing and is skipped.
    """
    if cost < 1 or budget < cost:
        raise ValueError("the budget must cover at least one experiment")
    attempts: list[Attempt] = []
    spent = 0
    confirmed: str | None = None
    for i, step_id in enumerate(candidates):
        if spent + cost > budget:
            for rest in candidates[i:]:
                att = Attempt(step_id=rest, status="not_reached", reason="the replay budget was spent")
                attempts.append(att)
                if on_attempt:
                    on_attempt(att)
            break
        result = verify(step_id)
        spent += result.replays_used
        if result.verdict is None:
            att = Attempt(step_id=step_id, status="skipped", reason=result.reason, experiment_id=result.experiment_id)
        else:
            att = Attempt(
                step_id=step_id, status="verified", verdict=result.verdict, replays_used=result.replays_used,
                reason=result.reason, experiment_id=result.experiment_id,
            )
        attempts.append(att)
        if on_attempt:
            on_attempt(att)
        if result.verdict is Verdict.CONFIRMED:
            confirmed = step_id
            break
    if confirmed:
        outcome: Literal["confirmed", "exhausted", "no_candidate"] = "confirmed"
    elif any(a.status == "verified" for a in attempts):
        outcome = "exhausted"
    else:
        outcome = "no_candidate"
    return InvestigationResult(
        attempts=attempts, outcome=outcome, confirmed_step=confirmed, replays_used=spent, budget=budget
    )


__all__ = [
    "DEFAULT_BUDGET", "MAX_BUDGET", "Attempt", "InvestigationResult", "VerifyOutcome", "check_budget", "investigate",
]
