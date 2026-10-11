"""Evidence records: typed, hashed, append-only (master plan 14.5).

The hash covers a canonical JSON form, so the same payload always gives the same SHA-256 and anyone
holding the payload can confirm a report's hash.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class EvidenceType(StrEnum):
    """The nine kinds of evidence a finding can carry."""
    STEP_SNAPSHOT = "step_snapshot"
    CHECK_COMPUTATION = "check_computation"
    SOURCE_OF_TRUTH_QUERY = "source_of_truth_query"
    PROVENANCE_PATH = "provenance_path"
    REPLAY_OUTPUT = "replay_output"
    DIFF = "diff"
    VERDICT_COMPUTATION = "verdict_computation"
    LLM_OPINION = "llm_opinion"
    REVIEWER_NOTE = "reviewer_note"


def canonical_json(obj: Any) -> str:
    """Serialize with sorted keys and no extra whitespace, so equal payloads give equal text."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def sha256_of(obj: Any) -> str:
    """SHA-256 of the canonical JSON of an object."""
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


class EvidenceRecord(BaseModel):
    """A typed evidence payload with the hash that proves it has not changed."""
    type: EvidenceType
    payload: dict[str, Any]
    sha256: str
    reproduce: str = ""


def make_evidence(type_: EvidenceType, payload: dict[str, Any], reproduce: str = "") -> EvidenceRecord:
    """Build an evidence record and compute its hash."""
    return EvidenceRecord(type=type_, payload=payload, sha256=sha256_of(payload), reproduce=reproduce)


def verify_evidence(rec: EvidenceRecord) -> bool:
    """True if the record's payload still matches its stored hash."""
    return sha256_of(rec.payload) == rec.sha256
