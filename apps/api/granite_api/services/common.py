"""Shared persistence helpers: evidence, audit log, finding transitions."""

from __future__ import annotations

from typing import Any

from granite_core.evidence import EvidenceType, make_evidence
from granite_core.lifecycle import Event, FindingStatus, transition
from sqlalchemy.orm import Session

from ..models import AuditLog, Evidence, Finding, new_id


def add_evidence(
    session: Session,
    run_id: str,
    finding_id: str | None,
    type_: EvidenceType,
    title: str,
    payload: dict[str, Any],
    reproduce: str = "",
) -> Evidence:
    rec = make_evidence(type_, payload, reproduce)
    row = Evidence(
        id=new_id("ev"),
        run_id=run_id,
        finding_id=finding_id,
        type=rec.type.value,
        title=title[:200],
        payload=rec.payload,
        sha256=rec.sha256,
        reproduce=rec.reproduce,
    )
    session.add(row)
    return row


def audit(session: Session, actor: str, action: str, entity_type: str, entity_id: str, **detail: Any) -> None:
    session.add(AuditLog(actor=actor, action=action, entity_type=entity_type, entity_id=entity_id, detail=detail))


def move(session: Session, finding: Finding, event: Event, actor: str = "system") -> FindingStatus:
    """Apply a lifecycle event (raises IllegalTransition) and write the audit row."""
    before = FindingStatus(finding.status)
    after = transition(before, event)
    finding.status = after.value
    audit(
        session, actor, "finding_transition", "finding", finding.id,
        event=event.value, from_status=before.value, to_status=after.value,
    )
    return after
