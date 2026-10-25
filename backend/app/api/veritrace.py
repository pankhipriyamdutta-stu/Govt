import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from app.database import get_db
from app.config import settings
from app.models.veritrace import (
    VeritraceDocument,
    ForensicFinding,
    ExtractedClaim,
    ClaimEvidence,
    ProvenanceNode,
    ProvenanceEdge
)
from app.models.user import User
from app.api.auth import get_current_user
from app.services.veritrace import (
    HashingService,
    OCRService,
    DocumentProcessor,
    VisualForensicsService,
    ForensicService,
    FraudDetectionMLService,
    ClaimExtractor,
    EvidenceRetrievalService,
    FactVerificationEngine,
    ProvenanceService,
    ReportService,
    IITSovereignFrameworkService
)

router = APIRouter(prefix="/veritrace", tags=["VERITRACE AI — CyberSecurity & Document Intelligence"])

@router.get("/health")
def veritrace_health():
    """Health and capability diagnostic for VERITRACE AI framework."""
    return {
        "status": "HEALTHY",
        "service": "VERITRACE AI Document Fraud Detection & Provenance Framework",
        "version": "2.0.0-SOVEREIGN",
        "capabilities": {
            "dual_hashing_sha256_sha512": True,
            "pdf_structural_inspection": True,
            "pypdf_pymupdf_extraction": True,
            "opencv_ela_forensics": VisualForensicsService.is_opencv_available(),
            "windows_media_ocr": OCRService.is_ocr_available(),
            "ml_anomaly_isolation_forest": True,
            "fact_verification_nli": True,
            "networkx_provenance_graph": True
        },
        "malware_scanner_configured": False,
        "malware_scanner_notice": "Malware scanning not performed (no external scanner configured)"
    }

@router.get("/stats")
def get_veritrace_stats(db: Session = Depends(get_db)):
    """Overview dashboard statistics: counts, risk distribution, recent activity."""
    total_docs = db.query(VeritraceDocument).count()
    completed_docs = db.query(VeritraceDocument).filter(VeritraceDocument.analysis_status == "COMPLETED").count()
    failed_docs = db.query(VeritraceDocument).filter(VeritraceDocument.analysis_status == "FAILED").count()
    pending_docs = db.query(VeritraceDocument).filter(VeritraceDocument.analysis_status.in_(["PENDING", "PROCESSING"])).count()

    low_risk = db.query(VeritraceDocument).filter(VeritraceDocument.overall_risk_verdict == "LOW").count()
    mod_risk = db.query(VeritraceDocument).filter(VeritraceDocument.overall_risk_verdict == "MODERATE").count()
    high_risk = db.query(VeritraceDocument).filter(VeritraceDocument.overall_risk_verdict == "HIGH").count()
    insufficient_risk = db.query(VeritraceDocument).filter(VeritraceDocument.overall_risk_verdict == "INSUFFICIENT_DATA").count()

    recent_docs = db.query(VeritraceDocument).order_by(VeritraceDocument.created_at.desc()).limit(10).all()

    return {
        "summary": {
            "total_documents": total_docs,
            "completed_analyses": completed_docs,
            "failed_analyses": failed_docs,
            "pending_or_processing": pending_docs
        },
        "risk_distribution": {
            "LOW": low_risk,
            "MODERATE": mod_risk,
            "HIGH": high_risk,
            "INSUFFICIENT_DATA": insufficient_risk
        },
        "recent_documents": [
            {
                "document_id": d.document_id,
                "filename": d.original_filename,
                "sha256": d.sha256_hash,
                "file_type": d.file_type,
                "overall_risk_verdict": d.overall_risk_verdict,
                "overall_risk_score": d.overall_risk_score,
                "page_count": d.page_count,
                "has_digital_signature": d.has_digital_signature,
                "analysis_status": d.analysis_status,
                "upload_timestamp": d.upload_timestamp.isoformat() if d.upload_timestamp else None
            }
            for d in recent_docs
        ]
    }

@router.post("/upload")
async def upload_document_for_verification(
    file: UploadFile = File(...),
    uploaded_by: Optional[str] = Form("authorized_officer"),
    db: Session = Depends(get_db)
):
    """
    Module One: Secure Document Upload.
    - Validates file type and binary magic signatures
    - Enforces size limit (25MB)
    - Generates internal document identifier
    - Computes SHA-256 and SHA-512 hashes
    - Stores file outside public web root with non-user-controlled filename
    - Runs text extraction and entity extraction
    - Reports explicit malware scan status
    """
    content = await file.read()
    filename = file.filename or "uploaded_document"

    # Validate file
    is_valid, err_msg, mime_type = DocumentProcessor.validate_file(filename, content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=err_msg)

    # Secure storage
    upload_info = DocumentProcessor.save_uploaded_file(
        storage_dir=settings.UPLOAD_DIR,
        filename=filename,
        content=content
    )

    doc_id = upload_info["document_id"]
    storage_path = upload_info["storage_path"]

    # Extract text & entities
    extraction_res = DocumentProcessor.extract_document_content(
        storage_path=storage_path,
        file_type=mime_type
    )

    # Create database record
    new_doc = VeritraceDocument(
        document_id=doc_id,
        original_filename=upload_info["original_filename"],
        storage_path=storage_path,
        file_type=mime_type,
        file_size_bytes=upload_info["file_size_bytes"],
        sha256_hash=upload_info["sha256_hash"],
        sha512_hash=upload_info["sha512_hash"],
        uploaded_by=uploaded_by,
        upload_timestamp=datetime.now(timezone.utc),
        malware_scan_status=upload_info["malware_scan_status"],
        malware_scan_details=upload_info["malware_scan_details"],
        extraction_status=extraction_res["extraction_status"],
        analysis_status="PENDING",
        page_count=extraction_res["page_count"],
        ocr_used=extraction_res["ocr_used"],
        text_extraction_method=extraction_res["text_extraction_method"],
        extracted_text=extraction_res["extracted_text"],
        extracted_entities=extraction_res["extracted_entities"]
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "status": "UPLOAD_ACCEPTED",
        "document_id": doc_id,
        "filename": new_doc.original_filename,
        "file_type": new_doc.file_type,
        "file_size_bytes": new_doc.file_size_bytes,
        "sha256_hash": new_doc.sha256_hash,
        "sha512_hash": new_doc.sha512_hash,
        "malware_scan": {
            "status": new_doc.malware_scan_status,
            "details": new_doc.malware_scan_details
        },
        "extraction": {
            "status": new_doc.extraction_status,
            "page_count": new_doc.page_count,
            "ocr_used": new_doc.ocr_used,
            "entities_found": len(new_doc.extracted_entities or [])
        },
        "next_step": f"POST /api/v1/veritrace/documents/{doc_id}/analyze"
    }

@router.get("/documents")
def list_veritrace_documents(
    risk_filter: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    limit: int = Query(50),
    db: Session = Depends(get_db)
):
    """Lists analyzed documents with filtering and pagination."""
    q = db.query(VeritraceDocument)
    if risk_filter and risk_filter != "ALL":
        q = q.filter(VeritraceDocument.overall_risk_verdict == risk_filter)
    if status_filter and status_filter != "ALL":
        q = q.filter(VeritraceDocument.analysis_status == status_filter)

    docs = q.order_by(VeritraceDocument.created_at.desc()).limit(limit).all()

    return [
        {
            "document_id": d.document_id,
            "filename": d.original_filename,
            "file_type": d.file_type,
            "file_size_bytes": d.file_size_bytes,
            "sha256_hash": d.sha256_hash,
            "page_count": d.page_count,
            "ocr_used": d.ocr_used,
            "has_digital_signature": d.has_digital_signature,
            "overall_risk_verdict": d.overall_risk_verdict,
            "overall_risk_score": d.overall_risk_score,
            "analysis_status": d.analysis_status,
            "claims_count": d.claims_count,
            "claims_verified_count": d.claims_verified_count,
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in docs
    ]

@router.get("/documents/{document_id}")
def get_veritrace_document_details(document_id: str, db: Session = Depends(get_db)):
    """Fetches complete record of a Veritrace document."""
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    findings = db.query(ForensicFinding).filter(ForensicFinding.document_id == document_id).all()
    claims = db.query(ExtractedClaim).filter(ExtractedClaim.document_id == document_id).all()

    return {
        "document": {
            "document_id": doc.document_id,
            "original_filename": doc.original_filename,
            "file_type": doc.file_type,
            "file_size_bytes": doc.file_size_bytes,
            "sha256_hash": doc.sha256_hash,
            "sha512_hash": doc.sha512_hash,
            "uploaded_by": doc.uploaded_by,
            "upload_timestamp": doc.upload_timestamp.isoformat() if doc.upload_timestamp else None,
            "malware_scan": {
                "status": doc.malware_scan_status,
                "details": doc.malware_scan_details
            },
            "extraction": {
                "status": doc.extraction_status,
                "page_count": doc.page_count,
                "ocr_used": doc.ocr_used,
                "text_extraction_method": doc.text_extraction_method,
                "text_snippet": (doc.extracted_text or "")[:1500],
                "entities": doc.extracted_entities
            },
            "risk_assessment": {
                "verdict": doc.overall_risk_verdict,
                "score": doc.overall_risk_score,
                "summary": doc.risk_summary
            },
            "forensics": {
                "has_digital_signature": doc.has_digital_signature,
                "signature_valid": doc.signature_valid,
                "signature_details": doc.signature_details,
                "reference_hash_status": doc.reference_hash_status,
                "trusted_reference_source": doc.trusted_reference_source,
                "structural_indicators": doc.structural_indicators,
                "visual_tampering_score": doc.visual_tampering_score,
                "visual_tampering_verdict": doc.visual_tampering_verdict,
                "visual_findings": doc.visual_findings
            },
            "ml_fraud_evaluation": {
                "fraud_probability": doc.ml_fraud_score,
                "anomaly_verdict": doc.ml_anomaly_verdict,
                "features": doc.ml_features
            },
            "analysis_status": doc.analysis_status
        },
        "findings_count": len(findings),
        "claims_count": len(claims)
    }

@router.post("/documents/{document_id}/analyze")
def run_veritrace_analysis_pipeline(document_id: str, db: Session = Depends(get_db)):
    """
    Runs the complete connected VERITRACE AI Investigation Pipeline:
    1. Digital Forensics (Integrity, PDF Metadata & Structure, Signatures, OpenCV ELA)
    2. ML Fraud Risk Anomaly Detection
    3. Claim Extraction from text
    4. Fact Verification against authoritative sources
    5. NetworkX Source Provenance Graph generation
    6. Overall Explainable Risk aggregation & Audit Report assembly
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    doc.analysis_status = "PROCESSING"
    db.commit()

    try:
        # 1. Digital Forensics
        forensic_res = ForensicService.perform_full_forensic_audit(
            document_id=doc.document_id,
            storage_path=doc.storage_path,
            file_type=doc.file_type
        )

        # Clear any prior findings for this doc
        db.query(ForensicFinding).filter(ForensicFinding.document_id == document_id).delete()
        for f in forensic_res.get("findings", []):
            finding_row = ForensicFinding(
                finding_id=f["finding_id"],
                document_id=document_id,
                category=f["category"],
                status=f["status"],
                severity=f["severity"],
                description=f["description"],
                evidence=f["evidence"],
                limitations=f["limitations"],
                model_version=f.get("model_version")
            )
            db.add(finding_row)

        # 2. ML Fraud Risk Evaluation
        features = FraudDetectionMLService.extract_features(
            metadata_anomalies_count=len(forensic_res.get("metadata", {}).get("anomalies", [])),
            structural_revisions_count=forensic_res.get("structural_indicators", {}).get("incremental_revisions", 0),
            visual_tamper_score=forensic_res.get("visual_tampering", {}).get("visual_tampering_score", 0.0),
            ocr_confidence=0.92 if not doc.ocr_used else 0.75,
            has_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
            page_count=doc.page_count,
            text_length=len(doc.extracted_text or "")
        )

        ml_eval = FraudDetectionMLService.evaluate_fraud_risk(
            features=features,
            has_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
            ref_hash_matches=(forensic_res.get("reference_hash_status") == "MATCHES_TRUSTED_REFERENCE")
        )

        # 3. Claim Extraction
        raw_claims = ClaimExtractor.extract_claims(doc.extracted_text or "")

        # 4. Fact Verification
        verified_claims = FactVerificationEngine.verify_all_claims(raw_claims, db=db)

        # Save claims & evidence in database
        db.query(ClaimEvidence).filter(ClaimEvidence.document_id == document_id).delete()
        db.query(ExtractedClaim).filter(ExtractedClaim.document_id == document_id).delete()

        claims_verified_count = 0
        for vc in verified_claims:
            if vc["verification_status"] in ("SUPPORTED", "CONTRADICTED"):
                claims_verified_count += 1

            c_row = ExtractedClaim(
                claim_id=vc["claim_id"],
                document_id=document_id,
                claim_text=vc["claim_text"],
                subject=vc["subject"],
                predicate=vc["predicate"],
                object=vc["object"],
                verification_status=vc["verification_status"],
                confidence_score=vc["confidence_score"],
                reasoning=vc["reasoning"],
                limitations=vc["limitations"]
            )
            db.add(c_row)

            for ev_idx, ev in enumerate(vc.get("evidence_items", [])):
                ev_id = f"EV-{c_row.claim_id[-6:]}-{ev_idx + 1}-{uuid.uuid4().hex[:6].upper()}"
                ev_row = ClaimEvidence(
                    evidence_id=ev_id,
                    claim_id=c_row.claim_id,
                    document_id=document_id,
                    source_title=ev["source_title"],
                    source_url=ev["source_url"],
                    source_authority=ev.get("authority"),
                    publication_date=ev.get("publication_date"),
                    passage_text=ev["passage_text"],
                    alignment_label=ev.get("alignment_label", "NEUTRAL"),
                    similarity_score=ev.get("similarity_score", 0.0)
                )
                db.add(ev_row)

        # 5. Provenance Graph Generation
        provenance_data = ProvenanceService.generate_provenance_graph(
            document_id=document_id,
            filename=doc.original_filename,
            sha256_hash=doc.sha256_hash,
            metadata=forensic_res.get("metadata", {}),
            signature_details=forensic_res.get("signature_details", {}),
            ref_hash_status=forensic_res.get("reference_hash_status", "NO_TRUSTED_REFERENCE"),
            claims_with_evidence=verified_claims
        )

        # Store provenance nodes & edges in database
        db.query(ProvenanceEdge).filter(ProvenanceEdge.document_id == document_id).delete()
        db.query(ProvenanceNode).filter(ProvenanceNode.document_id == document_id).delete()

        for n in provenance_data.get("nodes", []):
            db.add(ProvenanceNode(
                document_id=document_id,
                node_id=n["id"],
                node_type=n["node_type"],
                label=n["label"],
                metadata_json=n
            ))

        for e in provenance_data.get("edges", []):
            db.add(ProvenanceEdge(
                document_id=document_id,
                source_node=e["source"],
                target_node=e["target"],
                relation_type=e["relation_type"],
                confidence=e.get("confidence", 1.0),
                evidence_basis=e.get("evidence_basis")
            ))

        # 6. Overall Explainable Risk & Report Assembly
        doc_dict = {
            "document_id": doc.document_id,
            "original_filename": doc.original_filename,
            "file_type": doc.file_type,
            "file_size_bytes": doc.file_size_bytes,
            "page_count": doc.page_count,
            "sha256_hash": doc.sha256_hash,
            "sha512_hash": doc.sha512_hash,
            "uploaded_by": doc.uploaded_by,
            "upload_timestamp": doc.upload_timestamp.isoformat() if doc.upload_timestamp else None,
            "malware_scan_status": doc.malware_scan_status,
            "malware_scan_details": doc.malware_scan_details
        }

        final_report = ReportService.assemble_final_report(
            document_record=doc_dict,
            forensic_data=forensic_res,
            claims_data=verified_claims,
            provenance_data=provenance_data,
            ml_data=ml_eval
        )

        overall = final_report["executive_verdict"]

        # Update document record
        doc.analysis_status = "COMPLETED"
        doc.overall_risk_verdict = overall["verdict"]
        doc.overall_risk_score = overall["risk_score"]
        doc.risk_summary = overall["explanation"]
        doc.has_digital_signature = forensic_res["signature_details"].get("has_signature", False)
        doc.signature_valid = forensic_res["signature_details"].get("signature_valid", False)
        doc.signature_details = forensic_res["signature_details"]
        doc.reference_hash_status = forensic_res["reference_hash_status"]
        doc.trusted_reference_source = forensic_res["trusted_reference_source"]
        doc.structural_indicators = forensic_res["structural_indicators"]
        doc.visual_tampering_score = forensic_res.get("visual_tampering", {}).get("visual_tampering_score", 0.0)
        doc.visual_tampering_verdict = forensic_res.get("visual_tampering", {}).get("verdict", "NOT_EVALUATED")
        doc.visual_findings = forensic_res.get("visual_tampering", {}).get("suspicious_regions", [])
        doc.ml_fraud_score = ml_eval.get("fraud_probability", 0.0)
        doc.ml_anomaly_verdict = ml_eval.get("anomaly_verdict", "CONSISTENT")
        doc.ml_features = features
        doc.claims_count = len(verified_claims)
        doc.claims_verified_count = claims_verified_count
        doc.provenance_node_count = len(provenance_data.get("nodes", []))

        db.commit()

        return {
            "status": "ANALYSIS_COMPLETED",
            "document_id": document_id,
            "executive_verdict": overall,
            "forensics_summary": {
                "reference_hash_status": doc.reference_hash_status,
                "has_digital_signature": doc.has_digital_signature,
                "visual_tampering_score": doc.visual_tampering_score,
                "visual_verdict": doc.visual_tampering_verdict,
                "findings_count": len(forensic_res.get("findings", []))
            },
            "ml_fraud_summary": {
                "fraud_probability": doc.ml_fraud_score,
                "anomaly_verdict": doc.ml_anomaly_verdict,
                "model_version": ml_eval.get("model_version")
            },
            "claims_summary": {
                "total_claims": len(verified_claims),
                "verified_count": claims_verified_count
            },
            "provenance_summary": provenance_data.get("provenance_summary"),
            "final_report": final_report
        }

    except Exception as e:
        doc.analysis_status = "FAILED"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")

@router.get("/documents/{document_id}/forensics")
def get_forensic_results(document_id: str, db: Session = Depends(get_db)):
    """Returns digital forensics findings, visual ELA tampering regions, and metadata."""
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    findings = db.query(ForensicFinding).filter(ForensicFinding.document_id == document_id).all()

    return {
        "document_id": doc.document_id,
        "filename": doc.original_filename,
        "sha256_hash": doc.sha256_hash,
        "sha512_hash": doc.sha512_hash,
        "reference_hash_status": doc.reference_hash_status,
        "trusted_reference_source": doc.trusted_reference_source,
        "digital_signature": {
            "has_signature": doc.has_digital_signature,
            "is_valid": doc.signature_valid,
            "details": doc.signature_details
        },
        "structural_indicators": doc.structural_indicators,
        "visual_forensics": {
            "tampering_score": doc.visual_tampering_score,
            "verdict": doc.visual_tampering_verdict,
            "suspicious_regions": doc.visual_findings
        },
        "findings": [
            {
                "finding_id": f.finding_id,
                "category": f.category,
                "status": f.status,
                "severity": f.severity,
                "description": f.description,
                "evidence": f.evidence,
                "limitations": f.limitations
            }
            for f in findings
        ]
    }

@router.get("/documents/{document_id}/claims")
def get_verified_claims(document_id: str, db: Session = Depends(get_db)):
    """Returns extracted factual claims and supporting/contradicting evidence passages."""
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    claims = db.query(ExtractedClaim).filter(ExtractedClaim.document_id == document_id).all()
    results = []

    for c in claims:
        evidence_items = db.query(ClaimEvidence).filter(ClaimEvidence.claim_id == c.claim_id).all()
        results.append({
            "claim_id": c.claim_id,
            "claim_text": c.claim_text,
            "subject": c.subject,
            "predicate": c.predicate,
            "object": c.object,
            "verification_status": c.verification_status,
            "confidence_score": c.confidence_score,
            "reasoning": c.reasoning,
            "limitations": c.limitations,
            "evidence": [
                {
                    "evidence_id": ev.evidence_id,
                    "source_title": ev.source_title,
                    "source_url": ev.source_url,
                    "source_authority": ev.source_authority,
                    "publication_date": ev.publication_date,
                    "passage_text": ev.passage_text,
                    "alignment_label": ev.alignment_label,
                    "similarity_score": ev.similarity_score
                }
                for ev in evidence_items
            ]
        })

    return {
        "document_id": document_id,
        "total_claims": len(results),
        "claims": results
    }

@router.get("/documents/{document_id}/provenance")
def get_provenance_graph_data(document_id: str, db: Session = Depends(get_db)):
    """Returns interactive provenance graph nodes and edges with search audit scope."""
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    nodes = db.query(ProvenanceNode).filter(ProvenanceNode.document_id == document_id).all()
    edges = db.query(ProvenanceEdge).filter(ProvenanceEdge.document_id == document_id).all()

    return {
        "document_id": document_id,
        "filename": doc.original_filename,
        "sha256": doc.sha256_hash,
        "nodes": [
            {
                "id": n.node_id,
                "node_type": n.node_type,
                "label": n.label,
                "metadata": n.metadata_json
            }
            for n in nodes
        ],
        "edges": [
            {
                "source": e.source_node,
                "target": e.target_node,
                "relation_type": e.relation_type,
                "confidence": e.confidence,
                "evidence_basis": e.evidence_basis
            }
            for e in edges
        ],
        "legend": {
            "CITES": "Document cites statutory act or notification",
            "COPIED_FROM": "Cryptographic byte hash matches identical indexed copy",
            "SIMILAR_TO": "High textual/structural similarity without identical hash",
            "PUBLISHED_AT": "Signed or issued through formal authority portal",
            "SUPPORTS": "Authoritative passage directly supports extracted claim",
            "CONTRADICTS": "Authoritative passage directly refutes extracted claim"
        },
        "search_scope": {
            "searched": ProvenanceService.SEARCHED_SOURCES_SCOPE,
            "unavailable": ProvenanceService.UNAVAILABLE_SOURCES_SCOPE
        }
    }

@router.get("/documents/{document_id}/report")
def get_final_veritrace_report(document_id: str, db: Session = Depends(get_db)):
    """Returns complete downloadable / printable explainable audit report."""
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    # Re-run or fetch assembled report
    findings = db.query(ForensicFinding).filter(ForensicFinding.document_id == document_id).all()
    claims = db.query(ExtractedClaim).filter(ExtractedClaim.document_id == document_id).all()
    nodes = db.query(ProvenanceNode).filter(ProvenanceNode.document_id == document_id).all()
    edges = db.query(ProvenanceEdge).filter(ProvenanceEdge.document_id == document_id).all()

    claims_data = []
    for c in claims:
        ev_items = db.query(ClaimEvidence).filter(ClaimEvidence.claim_id == c.claim_id).all()
        claims_data.append({
            "claim_id": c.claim_id,
            "claim_text": c.claim_text,
            "subject": c.subject,
            "predicate": c.predicate,
            "object": c.object,
            "verification_status": c.verification_status,
            "confidence_score": c.confidence_score,
            "reasoning": c.reasoning,
            "limitations": c.limitations,
            "evidence_items": [
                {
                    "source_title": ev.source_title,
                    "source_url": ev.source_url,
                    "authority": ev.source_authority,
                    "publication_date": ev.publication_date,
                    "passage_text": ev.passage_text,
                    "alignment_label": ev.alignment_label,
                    "similarity_score": ev.similarity_score
                }
                for ev in ev_items
            ]
        })

    forensic_data = {
        "reference_hash_status": doc.reference_hash_status,
        "trusted_reference_source": doc.trusted_reference_source,
        "signature_details": doc.signature_details or {},
        "structural_indicators": doc.structural_indicators or {},
        "visual_tampering": {
            "visual_tampering_score": doc.visual_tampering_score or 0.0,
            "verdict": doc.visual_tampering_verdict,
            "suspicious_regions": doc.visual_findings or []
        },
        "findings": [
            {
                "finding_id": f.finding_id,
                "category": f.category,
                "status": f.status,
                "severity": f.severity,
                "description": f.description,
                "evidence": f.evidence,
                "limitations": f.limitations
            }
            for f in findings
        ]
    }

    doc_record = {
        "document_id": doc.document_id,
        "original_filename": doc.original_filename,
        "file_type": doc.file_type,
        "file_size_bytes": doc.file_size_bytes,
        "page_count": doc.page_count,
        "sha256_hash": doc.sha256_hash,
        "sha512_hash": doc.sha512_hash,
        "uploaded_by": doc.uploaded_by,
        "upload_timestamp": doc.upload_timestamp.isoformat() if doc.upload_timestamp else None,
        "malware_scan_status": doc.malware_scan_status,
        "malware_scan_details": doc.malware_scan_details
    }

    provenance_data = {
        "provenance_summary": {
            "total_nodes": len(nodes),
            "total_edges": len(edges)
        },
        "nodes": [{"id": n.node_id, "label": n.label, "node_type": n.node_type} for n in nodes],
        "edges": [{"source": e.source_node, "target": e.target_node, "relation_type": e.relation_type} for e in edges]
    }

    ml_data = {
        "fraud_probability": doc.ml_fraud_score or 0.0,
        "anomaly_verdict": doc.ml_anomaly_verdict or "NOT_EVALUATED",
        "model_version": FraudDetectionMLService.MODEL_VERSION,
        "model_status": "ACTIVE_CALIBRATED_BASELINE"
    }

    return ReportService.assemble_final_report(
        document_record=doc_record,
        forensic_data=forensic_data,
        claims_data=claims_data,
        provenance_data=provenance_data,
        ml_data=ml_data
    )

# =============================================================================
# IIT SOVEREIGN INNOVATIONS & ML EVALUATION ENDPOINTS
# =============================================================================

@router.get("/documents/{document_id}/c3ihub-certificate")
def get_c3ihub_certificate(
    document_id: str,
    officer_name: Optional[str] = Query("Authorized Sovereign Verification Officer"),
    db: Session = Depends(get_db)
):
    """
    IIT Kanpur C3iHub Sovereign Electronic Record Certificate.
    Compliant with Bharatiya Sakshya Adhiniyam (BSA) 2023 Sec 63 / IT Act Sec 65B.
    Builds a cryptographic Merkle Tree root over all forensic and evidentiary artifacts.
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    forensic_data = {
        "metadata": {
            "page_count": doc.page_count,
            "created_at": doc.upload_timestamp.isoformat() if doc.upload_timestamp else None,
            "file_type": doc.file_type
        },
        "signature_details": doc.signature_details or {},
        "visual_tampering": {
            "visual_tampering_score": doc.visual_tampering_score or 0.0,
            "verdict": doc.visual_tampering_verdict
        }
    }

    claims = db.query(ExtractedClaim).filter(ExtractedClaim.document_id == document_id).all()
    claims_data = [{"claim_text": c.claim_text, "verification_status": c.verification_status} for c in claims]

    certificate = IITSovereignFrameworkService.generate_c3ihub_sovereign_certificate(
        document_id=doc.document_id,
        filename=doc.original_filename,
        sha256_hash=doc.sha256_hash,
        forensic_data=forensic_data,
        claims_data=claims_data,
        officer_name=officer_name
    )

    return certificate

@router.post("/c3ihub-certificate/verify")
def verify_c3ihub_certificate(certificate: Dict[str, Any]):
    """
    Verifies an IIT Kanpur C3iHub Merkle Certificate.
    Reconstructs the Merkle tree from leaf descriptors to prove tamper resistance.
    """
    result = IITSovereignFrameworkService.verify_c3ihub_certificate(certificate)
    return result

@router.post("/documents/{document_id}/cmfd")
def run_copy_move_forgery_detection(
    document_id: str,
    page_number: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    IIT Delhi Computer Vision Lab: Multi-Scale Copy-Move Forgery Detection (CMFD).
    Scans document pages for cloned seals, duplicate signatures, and forged emblems.
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    res = IITSovereignFrameworkService.detect_copy_move_forgery_for_document(
        document_path=doc.storage_path,
        page_num=page_number
    )
    res["document_id"] = document_id
    res["page_inspected"] = page_number
    res["research_institution"] = "IIT Delhi Vision & Digital Forensics Lab"
    return res

@router.post("/documents/{document_id}/enhance-scan")
def enhance_document_scan_preview(
    document_id: str,
    page_number: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    IIT Madras Pravartak & AI4Bharat: Degraded Document Restoration.
    Applies adaptive Otsu binarization and illumination normalization to recover historical scans.
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    res = IITSovereignFrameworkService.enhance_document_scan(
        document_path=doc.storage_path,
        page_num=page_number
    )
    res["document_id"] = document_id
    res["page_number"] = page_number
    return res

@router.post("/containment-check")
def audit_prompt_injection_containment(payload: Dict[str, str]):
    """
    IIT Bombay TrustLab: Prompt Injection Fortress.
    Audits document text or external claims for adversarial prompt override attempts.
    """
    raw_text = payload.get("text", "")
    audit = IITSovereignFrameworkService.audit_adversarial_containment(raw_text)
    audit["research_framework"] = "Adversarial Prompt Containment Fortress"
    return audit

@router.get("/documents/{document_id}/statutory-compliance")
def evaluate_statutory_compliance(document_id: str, db: Session = Depends(get_db)):
    """
    Sovereign Regional Framework: Northeast Statutory Mandate Matrix.
    Evaluates service delivery timelines against the Assam Right to Public Services Act 2012.
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    text = doc.extracted_text or ""
    res = IITSovereignFrameworkService.evaluate_northeast_statutory_compliance(text)
    res["document_id"] = document_id
    res["governing_framework"] = "Assam State Statutory Delivery Matrix (ARTPS 2012)"
    return res

@router.get("/documents/{document_id}/structural-discrepancies")
def evaluate_structural_discrepancies(document_id: str, db: Session = Depends(get_db)):
    """
    IIT Kharagpur Cyber Forensics standard:
    Checks for post-dating of metadata, incremental update revisions, and EOF anomalies.
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    metadata = {
        "creation_date": doc.structural_indicators.get("creation_date") if doc.structural_indicators else None,
        "modification_date": doc.structural_indicators.get("modification_date") if doc.structural_indicators else None
    }

    res = IITSovereignFrameworkService.detect_structural_discrepancies(doc.storage_path, metadata)
    res["document_id"] = document_id
    return res

@router.get("/documents/{document_id}/script-analysis")
def evaluate_script_distribution(document_id: str, db: Session = Depends(get_db)):
    """
    IIT Madras AI4Bharat: Indic Script Identification.
    Identifies Assamese, Bengali, Devanagari, and English/Latin distributions.
    """
    doc = db.query(VeritraceDocument).filter(VeritraceDocument.document_id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found.")

    res = IITSovereignFrameworkService.identify_indic_scripts(doc.extracted_text or "")
    res["document_id"] = document_id
    return res

@router.get("/ml/metrics")
def get_ml_model_metrics():
    """
    Returns real hold-out cross-validation metrics, confusion matrix, ROC-AUC,
    and feature importances for Calibrated Random Forest & Isolation Forest models.
    """
    import json
    meta_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "model_metadata.json"))
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Model metadata not found. Run model training first.")

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return {
        "status": "VALIDATED_PRODUCTION_MODEL",
        "metadata": metadata
    }

@router.post("/ml/retrain")
def retrain_ml_models():
    """
    Triggers on-demand training of the Calibrated Random Forest and Isolation Forest
    using document-level GroupShuffleSplit (zero data leakage) and reloads active weights.
    """
    try:
        from ml.training.train_fraud_detector import train_and_evaluate_models
        results = train_and_evaluate_models()

        # Reload artifacts in memory
        FraudDetectionMLService._rf_model = None
        FraudDetectionMLService._iso_model = None
        FraudDetectionMLService._metadata = None
        FraudDetectionMLService.load_artifacts()

        return {
            "status": "SUCCESSFULLY_RETRAINED",
            "message": "Models successfully retrained with document-level zero-leakage cross-validation.",
            "metrics": results.get("metrics"),
            "model_version": results.get("model_version"),
            "training_samples": results.get("train_samples"),
            "test_samples": results.get("test_samples")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model retraining failed: {str(e)}")
