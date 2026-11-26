"""Lifecycle state machine (TC-REV-01), evidence hashing, redaction (TC-SEC-03), LLM cassettes."""

from __future__ import annotations

import pytest

from granite_core.evidence import EvidenceType, canonical_json, make_evidence, sha256_of, verify_evidence
from granite_core.lifecycle import (
    TERMINAL,
    TRANSITIONS,
    Event,
    FindingStatus,
    IllegalTransition,
    allowed_events,
    transition,
    verification_level,
)
from granite_core.llm import (
    Cassette,
    Completion,
    LLMRequest,
    ProviderUnavailable,
    RecordedMiss,
    RecordedProvider,
    RecordingProvider,
)
from granite_core.redaction import redact

S, E = FindingStatus, Event

# ---- lifecycle ------------------------------------------------------------------------------------------


@pytest.mark.parametrize("state,event,expected", [(s, e, t) for (s, e), t in TRANSITIONS.items()])
def test_every_legal_transition(state: FindingStatus, event: Event, expected: FindingStatus) -> None:
    assert transition(state, event) is expected


def test_happy_path_from_detection_to_resolution() -> None:
    st = S.OPEN
    for ev in (E.HYPOTHESES_READY, E.VERIFY_STARTED, E.VERDICT_CONFIRMED, E.REVIEW_ACCEPT, E.RESOLVE):
        st = transition(st, ev)
    assert st is S.RESOLVED


@pytest.mark.parametrize(
    "state,event",
    [
        (S.OPEN, E.REVIEW_ACCEPT),  # cannot accept before any analysis
        (S.HYPOTHESIZED, E.REVIEW_ACCEPT),  # cannot accept an unverified hypothesis
        (S.CONFIRMED, E.RESOLVE),  # must be reviewed first
        (S.REFUTED, E.REVIEW_ACCEPT),
        (S.RESOLVED, E.VERIFY_STARTED),  # terminal
        (S.REJECTED, E.REVIEW_ACCEPT),  # terminal
    ],
)
def test_illegal_transitions_raise(state: FindingStatus, event: Event) -> None:
    with pytest.raises(IllegalTransition, match="not allowed"):
        transition(state, event)


def test_terminal_states_have_no_exit() -> None:
    for st in TERMINAL:
        assert allowed_events(st) == []


def test_refuted_and_inconclusive_can_be_verified_again() -> None:
    assert transition(S.REFUTED, E.VERIFY_STARTED) is S.VERIFYING
    assert transition(S.INCONCLUSIVE, E.VERIFY_STARTED) is S.VERIFYING


def test_provider_failure_mid_verification_returns_to_hypothesized() -> None:
    assert transition(S.VERIFYING, E.VERIFY_ERROR) is S.HYPOTHESIZED


def test_verification_levels() -> None:
    assert verification_level(S.OPEN) == "V0"
    assert verification_level(S.HYPOTHESIZED) == "V1"
    assert verification_level(S.EVIDENCE_SUPPORTED) == "V1"
    assert verification_level(S.CONFIRMED) == "V2"
    assert verification_level(S.ACCEPTED) == "V3" and verification_level(S.RESOLVED) == "V3"


# ---- evidence -------------------------------------------------------------------------------------------


def test_hash_is_independent_of_key_order_and_whitespace() -> None:
    assert sha256_of({"a": 1, "b": [1, 2]}) == sha256_of({"b": [1, 2], "a": 1})
    assert canonical_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'


def test_evidence_hash_detects_tampering() -> None:
    rec = make_evidence(EvidenceType.CHECK_COMPUTATION, {"value": 43.0, "expected": 43.25}, "GET /check-results/1")
    assert verify_evidence(rec)
    rec.payload["value"] = 43.25
    assert not verify_evidence(rec)


def test_non_json_values_hash_deterministically() -> None:
    import datetime as dt

    p = {"when": dt.datetime(2026, 10, 6, tzinfo=dt.UTC)}
    assert sha256_of(p) == sha256_of({"when": dt.datetime(2026, 10, 6, tzinfo=dt.UTC)})


# ---- redaction ------------------------------------------------------------------------------------------


def test_redacts_email_cnic_card_and_phone() -> None:
    out = redact({"msg": "mail a.b+c@example.com, CNIC 35202-1234567-1, card 4111 1111 1111 1111, call 0300-123-4567"})
    m = out["msg"]
    assert "@" not in m and "35202" not in m and "4111" not in m and "0300" not in m
    assert "<EMAIL_1>" in m and "<CNIC_1>" in m and "<CARD_1>" in m and "<PHONE_1>" in m


def test_redaction_is_idempotent_and_keeps_equality() -> None:
    once = redact(["x@example.com", {"k": "x@example.com"}, 12, None])
    assert once == redact(once)
    assert once[0] == once[1]["k"] == "<EMAIL_1>" and once[2:] == [12, None]


def test_redaction_does_not_mutate_input_and_leaves_ordinary_numbers_alone() -> None:
    src = {"order": "#W2611340", "price": 47.84, "item": "6469567736", "n": ["a"]}
    assert redact(src) == src and src["order"] == "#W2611340"


# ---- LLM cassettes --------------------------------------------------------------------------------------


class _Live:
    name = "fake-live"

    def __init__(self) -> None:
        self.calls = 0

    def complete(self, request: LLMRequest) -> Completion:
        self.calls += 1
        return Completion(
            text=f"answer {self.calls}",
            model=request.model,
            provider=self.name,
            tokens_in=3,
            tokens_out=5,
            latency_ms=10,
        )


def _req(**kw) -> LLMRequest:
    base = dict(messages=[{"role": "user", "content": "hi"}], model="m", seed=1)
    return LLMRequest(**{**base, **kw})


def test_request_key_covers_everything_that_changes_the_answer() -> None:
    k = _req().key()
    assert k == _req().key()
    for change in (
        {"seed": 2},
        {"model": "other"},
        {"temperature": 0.9},
        {"max_tokens": 9},
        {"json_mode": True},
        {"messages": [{"role": "user", "content": "hello"}]},
    ):
        assert _req(**change).key() != k


def test_recording_then_recorded_mode_returns_the_same_real_answer(tmp_path) -> None:
    cas = Cassette(tmp_path / "c.json")
    live = _Live()
    first = RecordingProvider(live, cas).complete(_req())
    assert first.text == "answer 1" and not first.recorded and len(cas) == 1
    again = RecordedProvider(Cassette(tmp_path / "c.json")).complete(_req())  # reloaded from disk
    assert again.text == "answer 1" and again.recorded and again.provider == "recorded"
    assert live.calls == 1


def test_recorded_mode_never_invents_an_answer(tmp_path) -> None:
    with pytest.raises(RecordedMiss, match="never recorded"):
        RecordedProvider(Cassette(tmp_path / "empty.json")).complete(_req())


def test_live_recording_is_really_live_unless_reuse_is_requested(tmp_path) -> None:
    cas, live = Cassette(tmp_path / "c.json"), _Live()
    p = RecordingProvider(live, cas)
    p.complete(_req())
    p.complete(_req())
    assert live.calls == 2
    q = RecordingProvider(live, cas, reuse=True)
    q.complete(_req())
    assert live.calls == 2


def test_provider_errors_are_distinct_exception_types() -> None:
    assert issubclass(ProviderUnavailable, Exception) and not issubclass(RecordedMiss, ProviderUnavailable)
