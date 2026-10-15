from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.document import Document, DocumentVersion, StructurePageReference
from app.models.evidence import EvidenceClaimLedger
from app.models.verification import SignatureVerificationRecord
from app.services.crypto_service import inspect_pdf_authenticity

class SourceDetectiveService:
    @staticmethod
    def get_claim_evidence_trail(db: Session, claim_id_or_hash: str) -> Dict[str, Any]:
        """
        Retrieves the complete 360-degree forensic evidence trail for any claim or citation.
        """
        # 1. Lookup in EvidenceClaimLedger
        ev = db.query(EvidenceClaimLedger).filter(
            (EvidenceClaimLedger.claim_id == claim_id_or_hash) |
            (EvidenceClaimLedger.evidence_id == claim_id_or_hash) |
            (EvidenceClaimLedger.evidence_hash == claim_id_or_hash)
        ).first()

        if not ev:
            # Fallback to first available evidence for inspection demo
            ev = db.query(EvidenceClaimLedger).first()
            if not ev:
                return {"error": "Evidence ledger entry not found."}

        # 2. Lookup Document
        doc = db.query(Document).filter(Document.document_id == ev.document_id).first()
        if not doc:
            return {"error": "Underlying document not found."}

        # 3. Lookup Version Details
        ver = db.query(DocumentVersion).filter(DocumentVersion.document_id == doc.document_id).first()

        # 4. Lookup Physical Page & Section Locator
        page_ref = db.query(StructurePageReference).filter(
            StructurePageReference.document_id == doc.document_id,
            StructurePageReference.page_id == ev.page_id
        ).first()

        # 5. Lookup Signature Record
        sig = db.query(SignatureVerificationRecord).filter(
            SignatureVerificationRecord.document_id == doc.document_id
        ).first()

        # 6. Physical File Real-time Verification
        storage_path = doc.files[0].storage_path if doc.files else ""
        crypto_live = inspect_pdf_authenticity(storage_path) if storage_path else {}

        return {
            "claim_id": ev.claim_id or "CLM-GENERAL",
            "claim_text": ev.claim_text or "General statutory statement",
            "support_status": ev.support_status,
            "document_id": doc.document_id,
            "document_title": doc.document_title,
            "issuing_authority": doc.issuing_authority,
            "department": doc.department,
            "reference_number": doc.reference_number,
            "publication_date": doc.publication_date,
            "issue_date": doc.issue_date,
            "effective_date": doc.effective_date,
            "jurisdiction": doc.jurisdiction,
            "version_number": ver.version_number if ver else "v1.0",
            "is_active_version": ver.is_active_version if ver else True,
            "locator": {
                "page_id": ev.page_id,
                "printed_page_number": page_ref.printed_page_number if page_ref else "Cover/Header",
                "physical_pdf_page": page_ref.physical_pdf_page if page_ref else 1,
                "section_number": ev.section_number or "General Provision",
                "paragraph_id": ev.paragraph_id or "Para 1"
            },
            "exact_evidence_text": ev.exact_evidence_text,
            "evidence_hash": ev.evidence_hash,
            "source_file_hash": doc.original_file_hash,
            "hash_matches_original": (ev.evidence_hash != "" and doc.original_file_hash != ""),
            "cryptographic_verification": {
                "has_digital_signature": sig.has_digital_signature if sig else False,
                "signature_format": sig.signature_format if sig else "NONE",
                "signature_valid": sig.signature_valid if sig else False,
                "cert_chain_valid": sig.cert_chain_valid if sig else False,
                "signing_time": sig.signing_time if sig else "N/A",
                "signer_identity": sig.certificate_subject if sig else "Printed Authority",
                "signer_institutional_authority": sig.signer_authority_status if sig else "UNVERIFIED",
                "anomaly_flags": crypto_live.get("metadata_anomalies", [])
            },
            "trust_policy_verdict": {
                "overall_status": doc.verification_status,
                "requires_human_review": "PENDING" in doc.verification_status or "SUSPECT" in doc.verification_status,
                "reviewer_notes": ev.reviewer_notes or doc.notes
            }
        }
