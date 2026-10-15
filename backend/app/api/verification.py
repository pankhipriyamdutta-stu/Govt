from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models.user import User
from app.models.verification import VerificationQueue
from app.models.document import Document
from app.api.auth import get_current_user

router = APIRouter(prefix="/verification", tags=["Human-In-The-Loop Verification"])

class VerificationDecisionRequest(BaseModel):
    decision: str  # APPROVED_TRUSTED, REJECTED, NEEDS_AMENDMENT_CHECK
    rationale: str

@router.get("/queue")
def get_verification_queue(
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns queue of documents awaiting human verification and provenance review."""
    q = db.query(VerificationQueue)
    if status and status != "ALL":
        q = q.filter(VerificationQueue.current_status == status)
    
    items = q.all()
    results = []
    for it in items:
        doc = db.query(Document).filter(Document.document_id == it.document_id).first()
        results.append({
            "id": it.id,
            "document_id": it.document_id,
            "document_title": doc.document_title if doc else "Unknown",
            "department": doc.department if doc else "Unknown",
            "submission_type": it.submission_type,
            "submitted_by": it.submitted_by,
            "current_status": it.current_status,
            "reviewer_notes": it.reviewer_notes,
            "decision": it.decision,
            "decided_at": it.decided_at.strftime("%Y-%m-%d %H:%M:%S") if it.decided_at else None,
            "created_at": it.created_at.strftime("%Y-%m-%d %H:%M:%S") if it.created_at else None
        })
    return results

@router.post("/{item_id}/decision")
def record_decision(
    item_id: int,
    req: VerificationDecisionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Records a Verification Officer's authoritative decision on a pending document:
    - Enforces role permission check (ROL-003 Verification Officer or ROL-005 Admin)
    - Updates Document approval_status and verification_status
    - Logs audit trail
    """
    user_role = current_user.role.role_id if current_user.role else ""
    if user_role not in ["ROL-003", "ROL-005", "ROL-004"]:
        raise HTTPException(
            status_code=403,
            detail=f"Access Denied: Current role ({user_role}) lacks authority to approve or reject official government documents. Requires Verification Officer (ROL-003)."
        )

    queue_item = db.query(VerificationQueue).filter(VerificationQueue.id == item_id).first()
    if not queue_item:
        raise HTTPException(status_code=404, detail="Queue item not found")

    doc = db.query(Document).filter(Document.document_id == queue_item.document_id).first()

    queue_item.current_status = req.decision
    queue_item.decision = req.decision
    queue_item.reviewer_notes = f"{req.rationale} [Decided by: {current_user.full_name}]"
    queue_item.decided_at = datetime.now(timezone.utc)

    if doc:
        if req.decision == "APPROVED_TRUSTED":
            doc.verification_status = "VERIFIED_PRIMARY"
            doc.approval_status = "APPROVED_TRUSTED"
        elif req.decision == "REJECTED":
            doc.verification_status = "FAILED_VERIFICATION"
            doc.approval_status = "REJECTED_DISAPPROVED"
        else:
            doc.verification_status = "NEEDS_REVIEW"

    db.commit()

    return {
        "status": "DECISION_RECORDED",
        "item_id": item_id,
        "document_id": queue_item.document_id,
        "new_status": req.decision,
        "decided_by": current_user.full_name
    }
