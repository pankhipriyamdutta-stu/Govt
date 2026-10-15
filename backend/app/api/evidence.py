from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models.evidence import EvidenceClaimLedger
from app.services.detective_service import SourceDetectiveService

router = APIRouter(prefix="/evidence", tags=["Source Intelligence & Detective"])

class CitationValidationRequest(BaseModel):
    document_id: str
    section_number: str
    claim_text: str
    evidence_hash: str

@router.get("/detective/{claim_or_hash}")
def inspect_evidence_trail(claim_or_hash: str, db: Session = Depends(get_db)):
    """
    Source Detective API:
    Returns the complete 360-degree forensic evidence trail for any claim, citation, or evidence ID.
    Includes issuing authority, signer institutional authorization, exact locator, verbatim text,
    cryptographic hash, third-party metadata anomalies, and human review verdict.
    """
    trail = SourceDetectiveService.get_claim_evidence_trail(db, claim_or_hash)
    if "error" in trail:
        raise HTTPException(status_code=404, detail=trail["error"])
    return trail

@router.get("/ledger")
def get_evidence_ledger(
    document_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    q = db.query(EvidenceClaimLedger)
    if document_id:
        q = q.filter(EvidenceClaimLedger.document_id == document_id)
    if status and status != "ALL":
        q = q.filter(EvidenceClaimLedger.support_status.ilike(f"%{status}%"))
    
    entries = q.limit(limit).all()
    return [
        {
            "evidence_id": e.evidence_id,
            "document_id": e.document_id,
            "section_number": e.section_number,
            "claim_id": e.claim_id,
            "claim_text": e.claim_text,
            "exact_evidence_text": e.exact_evidence_text,
            "evidence_hash": e.evidence_hash,
            "support_status": e.support_status,
            "citation_status": e.citation_status,
            "reviewer_notes": e.reviewer_notes
        }
        for e in entries
    ]

@router.post("/validate-citation")
def validate_citation(req: CitationValidationRequest, db: Session = Depends(get_db)):
    """Validates whether a proposed citation matches official ledger evidence and hash."""
    ev = db.query(EvidenceClaimLedger).filter(
        EvidenceClaimLedger.document_id == req.document_id,
        EvidenceClaimLedger.evidence_hash == req.evidence_hash
    ).first()

    if not ev:
        return {
            "is_valid": False,
            "validation_verdict": "HASH_MISMATCH_OR_UNINDEXED",
            "message": "The citation hash does not correspond to an authenticated excerpt in the repository."
        }

    return {
        "is_valid": True,
        "validation_verdict": "AUTHENTICATED_AND_MATCHED",
        "document_id": ev.document_id,
        "section_number": ev.section_number,
        "support_status": ev.support_status,
        "evidence_hash": ev.evidence_hash
    }
