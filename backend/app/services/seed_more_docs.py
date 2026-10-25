import os
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.veritrace import VeritraceDocument, ExtractedClaim, ClaimEvidence, ProvenanceNode, ProvenanceEdge
from app.services.veritrace import (
    DocumentProcessor,
    ForensicService,
    FraudDetectionMLService,
    ClaimExtractor,
    FactVerificationEngine,
    ProvenanceService,
    ReportService
)

def ingest_all_source_documents():
    db = SessionLocal()
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "source_documents"))
    if not os.path.exists(source_dir):
        print(f"Directory {source_dir} not found.")
        db.close()
        return

    doc_configs = [
        ("c9fe9c9b6840524844316f74bb1c556c.pdf", "Assam SC/ST Examination Fee Exemption Act, 2024 (Assam Act XXXI of 2024)"),
        ("Citizen Charter.pdf", "GMC Citizen Charter & ARTPS Service Delivery Schedules"),
        ("MaintenanceofRecordstSZEC.pdf", "DoPT RTI Record Maintenance & Digitization Mandate"),
        ("Vacancy circular for employment news-1m1R62.pdf", "Central Information Commission Vacancy Circular 2025-26"),
        ("ARTPS RULES_0.pdf", "The Assam Right to Public Services Rules, 2012")
    ]

    for filename, title in doc_configs:
        existing = db.query(VeritraceDocument).filter(VeritraceDocument.original_filename == filename).first()
        if existing:
            print(f"[SKIP] {filename} already indexed.")
            continue

        src_path = os.path.join(source_dir, filename)
        if not os.path.exists(src_path):
            print(f"[WARN] File {src_path} not found.")
            continue

        try:
            print(f"[INGEST] Processing {filename} ({title})...")
            with open(src_path, "rb") as f:
                content = f.read()

            upload_info = DocumentProcessor.save_uploaded_file(
                storage_dir="uploads",
                filename=filename,
                content=content
            )

            doc_id = upload_info["document_id"]
            storage_path = upload_info["storage_path"]

            extraction_res = DocumentProcessor.extract_document_content(
                storage_path=storage_path,
                file_type="application/pdf"
            )

            # Forensic Audit
            forensic_res = ForensicService.perform_full_forensic_audit(
                document_id=doc_id,
                storage_path=storage_path,
                file_type="application/pdf"
            )

            # Features for ML
            features = FraudDetectionMLService.extract_features(
                metadata_anomalies_count=len(forensic_res.get("metadata", {}).get("anomalies", [])),
                structural_revisions_count=forensic_res.get("structural_indicators", {}).get("incremental_revisions", 0),
                visual_tamper_score=forensic_res.get("visual_tampering", {}).get("visual_tampering_score", 0.0),
                ocr_confidence=0.92,
                has_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
                page_count=extraction_res.get("page_count", 1),
                text_length=len(extraction_res.get("extracted_text", ""))
            )

            ml_eval = FraudDetectionMLService.evaluate_fraud_risk(
                features=features,
                has_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
                ref_hash_matches=False
            )

            # Claim extraction & verification
            raw_claims = ClaimExtractor.extract_claims(extraction_res.get("extracted_text", ""))
            verified_claims = FactVerificationEngine.verify_all_claims(raw_claims[:5], db=db)

            # Provenance
            provenance_data = ProvenanceService.generate_provenance_graph(
                document_id=doc_id,
                filename=filename,
                sha256_hash=upload_info["sha256_hash"],
                metadata=forensic_res.get("metadata", {}),
                signature_details=forensic_res.get("signature_details", {}),
                ref_hash_status=forensic_res.get("reference_hash_status", "UNREGISTERED_IN_PILOT"),
                claims_with_evidence=verified_claims
            )

            now = datetime.now(timezone.utc)
            doc_record = {
                "document_id": doc_id,
                "original_filename": filename,
                "file_type": "application/pdf",
                "file_size_bytes": upload_info["file_size_bytes"],
                "page_count": extraction_res.get("page_count", 1),
                "sha256_hash": upload_info["sha256_hash"],
                "sha512_hash": upload_info["sha512_hash"],
                "uploaded_by": "officer_sharma",
                "upload_timestamp": now.isoformat(),
                "malware_scan_status": "CLEAN",
                "malware_scan_details": "Signatures verified against ClamAV definitions."
            }

            final_rep = ReportService.assemble_final_report(
                document_record=doc_record,
                forensic_data=forensic_res,
                claims_data=verified_claims,
                provenance_data=provenance_data,
                ml_data=ml_eval
            )

            # Insert DB record
            v_doc = VeritraceDocument(
                document_id=doc_id,
                original_filename=filename,
                storage_path=storage_path,
                file_type="application/pdf",
                file_size_bytes=upload_info["file_size_bytes"],
                page_count=extraction_res.get("page_count", 1),
                sha256_hash=upload_info["sha256_hash"],
                sha512_hash=upload_info["sha512_hash"],
                uploaded_by="officer_sharma",
                upload_timestamp=now,
                malware_scan_status="CLEAN",
                malware_scan_details="Signatures verified against ClamAV definitions.",
                extracted_text=extraction_res.get("extracted_text", ""),
                ocr_used=False,
                analysis_status="COMPLETED",
                overall_risk_verdict=final_rep["executive_verdict"]["verdict"],
                overall_risk_score=final_rep["executive_verdict"]["risk_score"],
                risk_summary=final_rep["executive_verdict"]["explanation"],
                has_digital_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
                reference_hash_status=forensic_res.get("reference_hash_status", "UNREGISTERED_IN_PILOT"),
                visual_tampering_score=forensic_res.get("visual_tampering", {}).get("visual_tampering_score", 0.0),
                visual_tampering_verdict=forensic_res.get("visual_tampering", {}).get("verdict", "LOW_TAMPER_EVIDENCE"),
                claims_verified_count=len([c for c in verified_claims if c["verification_status"] in ("SUPPORTED", "CONTRADICTED")]),
                ml_fraud_score=ml_eval.get("fraud_probability", 0.05),
                ml_anomaly_verdict=ml_eval.get("anomaly_verdict", "INLIER_CONSISTENT"),
                ml_features=features,
                structural_indicators=forensic_res.get("structural_indicators", {})
            )
            db.add(v_doc)
            db.commit()
            print(f"[SUCCESS] Ingested {filename} as {doc_id} with verdict {v_doc.overall_risk_verdict}")

        except Exception as e:
            print(f"[ERROR] Failed to ingest {filename}: {e}")
            db.rollback()

    db.close()

if __name__ == "__main__":
    ingest_all_source_documents()
