"""Finding lifecycle as a state machine (master plan 13.3; FR-REV-02). Illegal transitions raise."""

from __future__ import annotations

from enum import StrEnum


class FindingStatus(StrEnum):
    OPEN = "open"
    HYPOTHESIZED = "hypothesized"
    VERIFYING = "verifying"
    CONFIRMED = "confirmed"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"
    EVIDENCE_SUPPORTED = "evidence_supported"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    RESOLVED = "resolved"
    WONT_FIX = "wont_fix"


class Event(StrEnum):
    HYPOTHESES_READY = "hypotheses_ready"
    VERIFY_STARTED = "verify_started"
    VERDICT_CONFIRMED = "verdict_confirmed"
    VERDICT_REFUTED = "verdict_refuted"
    VERDICT_INCONCLUSIVE = "verdict_inconclusive"
    VERIFY_ERROR = "verify_error"
    EVIDENCE_SUPPORTED = "evidence_supported"
    REVIEW_ACCEPT = "review_accept"
    REVIEW_REJECT = "review_reject"
    RESOLVE = "resolve"
    WONT_FIX = "wont_fix"


S, E = FindingStatus, Event

TRANSITIONS: dict[tuple[FindingStatus, Event], FindingStatus] = {
    (S.OPEN, E.HYPOTHESES_READY): S.HYPOTHESIZED,
    (S.HYPOTHESIZED, E.VERIFY_STARTED): S.VERIFYING,
    (S.HYPOTHESIZED, E.EVIDENCE_SUPPORTED): S.EVIDENCE_SUPPORTED,
    (S.VERIFYING, E.VERDICT_CONFIRMED): S.CONFIRMED,
    (S.VERIFYING, E.VERDICT_REFUTED): S.REFUTED,
    (S.VERIFYING, E.VERDICT_INCONCLUSIVE): S.INCONCLUSIVE,
    (S.VERIFYING, E.VERIFY_ERROR): S.HYPOTHESIZED,
    (S.REFUTED, E.VERIFY_STARTED): S.VERIFYING,  # verify the next hypothesis
    (S.INCONCLUSIVE, E.VERIFY_STARTED): S.VERIFYING,  # increase N (added to the plan's diagram, 2026-10)
    (S.CONFIRMED, E.REVIEW_ACCEPT): S.ACCEPTED,
    (S.CONFIRMED, E.REVIEW_REJECT): S.REJECTED,
    (S.INCONCLUSIVE, E.REVIEW_ACCEPT): S.ACCEPTED,
    (S.INCONCLUSIVE, E.REVIEW_REJECT): S.REJECTED,
    (S.EVIDENCE_SUPPORTED, E.REVIEW_ACCEPT): S.ACCEPTED,
    (S.EVIDENCE_SUPPORTED, E.REVIEW_REJECT): S.REJECTED,
    (S.ACCEPTED, E.RESOLVE): S.RESOLVED,
    (S.ACCEPTED, E.WONT_FIX): S.WONT_FIX,
}
TERMINAL = {S.REJECTED, S.RESOLVED, S.WONT_FIX}


class IllegalTransition(Exception):
    def __init__(self, status: FindingStatus, event: Event) -> None:
        super().__init__(f"event '{event.value}' is not allowed while a finding is '{status.value}'")
        self.status, self.event = status, event


def transition(status: FindingStatus, event: Event) -> FindingStatus:
    try:
        return TRANSITIONS[(status, event)]
    except KeyError:
        raise IllegalTransition(status, event) from None


def allowed_events(status: FindingStatus) -> list[Event]:
    return [ev for (st, ev) in TRANSITIONS if st is status]


def verification_level(status: FindingStatus, has_v1_evidence: bool = True) -> str:
    """V0 detected, V1 evidence-reproduced, V2 replay-verified, V3 human-confirmed (master plan 14.3)."""
    if status in (S.ACCEPTED, S.RESOLVED, S.WONT_FIX):
        return "V3"
    if status is S.CONFIRMED:
        return "V2"
    if status is S.EVIDENCE_SUPPORTED:
        return "V1"
    return "V1" if has_v1_evidence and status is not S.OPEN else "V0"
