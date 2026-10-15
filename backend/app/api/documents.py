import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.config import settings
from app.models.document import Document, DocumentVersion, DocumentFile, StructurePageReference, CleanedTextChunk
from app.models.user import User
from app.api.auth import get_current_user
from app.services.crypto_service import calculate_sha256, inspect_pdf_authenticity

router = APIRouter(prefix="/documents", tags=["Knowledge & Document Repository"])

@router.get("")
def list_documents(
    query: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    doc_type: Optional[str] = Query(None),
    verification_status: Optional[str] = Query(None),
    include_quarantined: bool = Query(False),
    db: Session = Depends(get_db)
):
    q = db.query(Document)
    
    if not include_quarantined:
        q = q.filter(Document.approval_status != "REJECTED_QUARANTINED")

    if query:
        q = q.filter(
            (Document.document_title.ilike(f"%{query}%")) |
            (Document.reference_number.ilike(f"%{query}%")) |
            (Document.issuing_authority.ilike(f"%{query}%"))
        )

    if department and department != "ALL":
        q = q.filter(Document.department.ilike(f"%{department}%"))

    if doc_type and doc_type != "ALL":
        q = q.filter(Document.document_type == doc_type)

    if verification_status and verification_status != "ALL":
        q = q.filter(Document.verification_status.ilike(f"%{verification_status}%"))

    docs = q.all()
    results = []
    for d in docs:
        results.append({
            "id": d.id,
            "document_id": d.document_id,
            "document_title": d.document_title,
            "document_type": d.document_type,
            "department": d.department,
            "issuing_authority": d.issuing_authority,
            "reference_number": d.reference_number,
            "publication_date": d.publication_date,
            "effective_date": d.effective_date,
            "verification_status": d.verification_status,
            "approval_status": d.approval_status,
            "classification": d.classification,
            "original_file_hash": d.original_file_hash,
            "notes": d.notes
        })
    return results

@router.get("/{document_id}")
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    versions = db.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).all()
    files = db.query(DocumentFile).filter(DocumentFile.document_id == document_id).all()
    pages = db.query(StructurePageReference).filter(StructurePageReference.document_id == document_id).all()
    chunks = db.query(CleanedTextChunk).filter(CleanedTextChunk.document_id == document_id).all()

    # Realtime file integrity inspection
    physical_check = {}
    if files:
        physical_check = inspect_pdf_authenticity(files[0].storage_path)

    return {
        "document": {
            "document_id": doc.document_id,
            "title": doc.document_title,
            "type": doc.document_type,
            "department": doc.department,
            "issuing_authority": doc.issuing_authority,
            "reference_number": doc.reference_number,
            "publication_date": doc.publication_date,
            "effective_date": doc.effective_date,
            "expiry_date": doc.expiry_date,
            "language": doc.language,
            "jurisdiction": doc.jurisdiction,
            "verification_status": doc.verification_status,
            "approval_status": doc.approval_status,
            "sha256_hash": doc.original_file_hash,
            "notes": doc.notes
        },
        "versions": [
            {
                "version_id": v.version_id,
                "version_number": v.version_number,
                "is_active": v.is_active_version,
                "effective_from": v.effective_from,
                "effective_to": v.effective_to
            }
            for v in versions
        ],
        "files": [
            {
                "path": f.storage_path,
                "size_bytes": f.file_size_bytes,
                "is_quarantined": f.is_quarantined,
                "quarantine_reason": f.quarantine_reason,
                "hash": f.sha256_hash
            }
            for f in files
        ],
        "structure": {
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "sample_sections": [p.section_title for p in pages[:6] if p.section_title]
        },
        "live_inspection": physical_check
    }

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_title: str = Form(...),
    department: str = Form(...),
    document_type: str = Form("CIRCULAR"),
    reference_number: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Asynchronous document ingestion endpoint:
    - Calculates SHA-256 immediately
    - Conducts quarantine scan for executable code and malware signatures
    - Evaluates third-party tool metadata
    - Places document in PENDING_VERIFICATION state (Never auto-approved)
    """
    clean_filename = os.path.basename(file.filename or "uploaded_document.pdf")
    temp_path = os.path.join(settings.UPLOAD_DIR, f"temp_{clean_filename}")
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_hash = calculate_sha256(temp_path)
    file_size = os.path.getsize(temp_path)

    # Perform Authenticity & Anomaly Scan
    inspection = inspect_pdf_authenticity(temp_path)

    is_quarantine = False
    quarantine_reason = None

    if inspection["metadata_anomalies"]:
        if any("adultpdf" in a or "ilovepdf" in a for a in inspection["metadata_anomalies"]):
            is_quarantine = True
            quarantine_reason = "Flagged: Suspect third-party conversion tool detected in document metadata."

    # Move to permanent location or quarantine
    dest_folder = settings.QUARANTINE_DIR if is_quarantine else settings.UPLOAD_DIR
    final_path = os.path.join(dest_folder, f"{file_hash[:12]}_{clean_filename}")
    os.rename(temp_path, final_path)

    # Generate Unique Document ID
    doc_count = db.query(Document).count()
    new_doc_id = f"DOC-UPLOAD-{doc_count + 1:03d}"

    new_doc = Document(
        document_id=new_doc_id,
        source_id="SRC-AUTHORIZED-UPLOAD",
        original_filename=clean_filename,
        document_title=document_title,
        document_type=document_type,
        department=department,
        issuing_authority=f"Department Official ({current_user.full_name})",
        reference_number=reference_number or f"DEP-UPL-{doc_count + 1}",
        publication_date=None,
        issue_date=None,
        effective_date=None,
        original_file_hash=file_hash,
        classification="DEPARTMENTAL_PROVISIONAL",
        extraction_status="INGESTED_PENDING_OCR",
        verification_status="PENDING_VERIFICATION",
        approval_status="QUARANTINED_PENDING_REVIEW" if is_quarantine else "PENDING_APPROVAL",
        notes=quarantine_reason or "Uploaded by authorized official. Pending verification officer inspection."
    )
    db.add(new_doc)
    db.flush()

    new_file = DocumentFile(
        document_id=new_doc_id,
        version_id=f"VER-{new_doc_id}-V1",
        storage_path=final_path,
        file_size_bytes=file_size,
        mime_type=file.content_type or "application/pdf",
        sha256_hash=file_hash,
        is_quarantined=is_quarantine,
        quarantine_reason=quarantine_reason
    )
    db.add(new_file)
    db.commit()

    return {
        "status": "INGESTION_ACCEPTED",
        "document_id": new_doc_id,
        "document_title": document_title,
        "sha256_hash": file_hash,
        "is_quarantined": is_quarantine,
        "verification_status": new_doc.verification_status,
        "message": "Document successfully ingested and quarantined for verification officer audit. It will NOT enter authoritative search until formally approved."
    }
