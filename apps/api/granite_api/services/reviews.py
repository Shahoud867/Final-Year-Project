"""Human review: the analyst accepts or rejects a finding and closes it. Every decision is recorded."""

from __future__ import annotations

from granite_core.evidence import EvidenceType
from granite_core.lifecycle import Event
from sqlalchemy.orm import Session

from ..errors import ProblemError
from ..models import Finding, Review, new_id
from .common import add_evidence, audit, move

DECISIONS: dict[str, Event] = {
    "accept": Event.REVIEW_ACCEPT,
    "reject": Event.REVIEW_REJECT,
    "resolve": Event.RESOLVE,
    "wont_fix": Event.WONT_FIX,
}
COMMENT_REQUIRED = {"reject", "wont_fix", "request_info"}
MIN_COMMENT = 5
# A reviewer may ask for more information (no status change) while a finding awaits a decision.
AWAITING_REVIEW = {"confirmed", "inconclusive", "evidence_supported"}


def apply_review(session: Session, finding_id: str, decision: str, comment: str, reviewer: str) -> Review:
    finding = session.get(Finding, finding_id)
    if finding is None:
        raise ProblemError(404, "Finding not found", f"There is no finding '{finding_id}'.")
    comment = comment.strip()
    # FR-REV-01: accepting a finding that was not clearly confirmed needs a stated reason
    needs_comment = decision in COMMENT_REQUIRED or (decision == "accept" and finding.status == "inconclusive")
    if needs_comment and len(comment) < MIN_COMMENT:
        raise ProblemError(
            422, "A comment is required", f"Say why you chose '{decision}' (at least {MIN_COMMENT} characters)."
        )
    before = finding.status
    if decision == "request_info":
        if before not in AWAITING_REVIEW:
            raise ProblemError(
                409, "Action not allowed in this state", f"Information can only be requested while a finding is "
                f"{', '.join(sorted(AWAITING_REVIEW))}; this one is {before}.",
                allowed_actions=[],
            )
    else:
        move(session, finding, DECISIONS[decision], reviewer)  # raises IllegalTransition (409)
    review = Review(
        id=new_id("rev"), finding_id=finding.id, reviewer=reviewer, decision=decision, comment=comment,
        from_status=before, to_status=finding.status,
    )
    session.add(review)
    if comment:
        add_evidence(
            session, finding.run_id, finding.id, EvidenceType.REVIEWER_NOTE, f"Reviewer note ({decision})",
            {"reviewer": reviewer, "decision": decision, "comment": comment},
        )
    audit(session, reviewer, "review", "finding", finding.id, decision=decision, to_status=finding.status)
    session.flush()
    return review
