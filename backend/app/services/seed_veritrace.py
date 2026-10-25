import os
import shutil
import uuid
from sqlalchemy.orm import Session
from app.models.veritrace import VeritraceDocument
from app.services.veritrace import (
    DocumentProcessor,
    ForensicService,
    FraudDetectionMLService,
    ClaimExtractor,
    FactVerificationEngine,
    ProvenanceService,
    ReportService
)
from app.models.veritrace import ForensicFinding, ExtractedClaim, ClaimEvidence, ProvenanceNode, ProvenanceEdge

def seed_sample_veritrace_documents(db: Session, sample_dir: str = "source_documents"):
    """
    Seeds initial realistic Veritrace documents for immediate operational demonstration:
    1. Authentic Government Act (The Assam Right to Public Services Act)
    2. Central Gazette Notification (IAS Cadre Strength Regulations 2025)
    3. Procurement Rules 2020
    """
    if db.query(VeritraceDocument).filter(VeritraceDocument.original_filename == "ARTPS ACT.pdf").first() is not None:
        print("[VERITRACE] Master sample documents already seeded.")
        return

    sample_files = [
        ("ARTPS ACT.pdf", "The Assam Right to Public Services Act, 2012", "LOW"),
        ("ias_fixation_of_cadre_strength_second_amendment_regulations_2025.pdf", "IAS Cadre Strength Second Amendment Regulations 2025", "LOW"),
        ("dms22_assam_public_procurement_rules_2020.pdf", "Assam Public Procurement Rules 2020", "MODERATE")
    ]

    for filename, title, expected_risk in sample_files:
        src_path = os.path.join(sample_dir, filename)
        if not os.path.exists(src_path):
            continue

        try:
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

            # ML Anomaly Risk
            features = FraudDetectionMLService.extract_features(
                metadata_anomalies_count=len(forensic_res.get("metadata", {}).get("anomalies", [])),
                structural_revisions_count=forensic_res.get("structural_indicators", {}).get("incremental_revisions", 0),
                visual_tamper_score=forensic_res.get("visual_tampering", {}).get("visual_tampering_score", 0.0),
                ocr_confidence=0.92 if not extraction_res["ocr_used"] else 0.80,
                has_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
                page_count=extraction_res["page_count"],
                text_length=len(extraction_res["extracted_text"] or "")
            )

            ml_eval = FraudDetectionMLService.evaluate_fraud_risk(
                features=features,
                has_signature=forensic_res.get("signature_details", {}).get("has_signature", False),
                ref_hash_matches=(forensic_res.get("reference_hash_status") == "MATCHES_TRUSTED_REFERENCE")
            )

            # Claims & Fact Verification
            claims = ClaimExtractor.extract_claims(extraction_res["extracted_text"] or "")
            verified_claims = FactVerificationEngine.verify_all_claims(claims, db=db)

            # Provenance
            provenance_data = ProvenanceService.generate_provenance_graph(
                document_id=doc_id,
                filename=filename,
                sha256_hash=upload_info["sha256_hash"],
                metadata=forensic_res.get("metadata", {}),
                signature_details=forensic_res.get("signature_details", {}),
                ref_hash_status=forensic_res.get("reference_hash_status", "NO_TRUSTED_REFERENCE"),
                claims_with_evidence=verified_claims
            )

            doc_dict = {
                "document_id": doc_id,
                "original_filename": filename,
                "file_type": "application/pdf",
                "file_size_bytes": upload_info["file_size_bytes"],
                "page_count": extraction_res["page_count"],
                "sha256_hash": upload_info["sha256_hash"],
                "sha512_hash": upload_info["sha512_hash"],
                "uploaded_by": "Directorate of Printing & Stationery",
                "upload_timestamp": None,
                "malware_scan_status": upload_info["malware_scan_status"],
                "malware_scan_details": upload_info["malware_scan_details"]
            }

            final_report = ReportService.assemble_final_report(
                document_record=doc_dict,
                forensic_data=forensic_res,
                claims_data=verified_claims,
                provenance_data=provenance_data,
                ml_data=ml_eval
            )

            overall = final_report["executive_verdict"]

            new_doc = VeritraceDocument(
                document_id=doc_id,
                original_filename=filename,
                storage_path=storage_path,
                file_type="application/pdf",
                file_size_bytes=upload_info["file_size_bytes"],
                sha256_hash=upload_info["sha256_hash"],
                sha512_hash=upload_info["sha512_hash"],
                uploaded_by="Directorate of Printing & Stationery",
                malware_scan_status=upload_info["malware_scan_status"],
                malware_scan_details=upload_info["malware_scan_details"],
                extraction_status=extraction_res["extraction_status"],
                analysis_status="COMPLETED",
                overall_risk_score=overall["risk_score"],
                overall_risk_verdict=overall["verdict"],
                risk_summary=overall["explanation"],
                page_count=extraction_res["page_count"],
                ocr_used=extraction_res["ocr_used"],
                text_extraction_method=extraction_res["text_extraction_method"],
                extracted_text=extraction_res["extracted_text"][:8000],
                extracted_entities=extraction_res["extracted_entities"],
                has_digital_signature=forensic_res["signature_details"].get("has_signature", False),
                signature_valid=forensic_res["signature_details"].get("signature_valid", False),
                signature_details=forensic_res["signature_details"],
                reference_hash_status=forensic_res["reference_hash_status"],
                trusted_reference_source=forensic_res["trusted_reference_source"],
                structural_indicators=forensic_res["structural_indicators"],
                visual_tampering_score=forensic_res.get("visual_tampering", {}).get("visual_tampering_score", 0.0),
                visual_tampering_verdict=forensic_res.get("visual_tampering", {}).get("verdict", "NOT_EVALUATED"),
                visual_findings=forensic_res.get("visual_tampering", {}).get("suspicious_regions", []),
                ml_fraud_score=ml_eval.get("fraud_probability", 0.0),
                ml_anomaly_verdict=ml_eval.get("anomaly_verdict", "CONSISTENT"),
                ml_features=features,
                claims_count=len(verified_claims),
                claims_verified_count=sum(1 for c in verified_claims if c["verification_status"] in ("SUPPORTED", "CONTRADICTED")),
                provenance_node_count=len(provenance_data.get("nodes", []))
            )
            db.add(new_doc)
            db.commit()

            # Save findings
            for f in forensic_res.get("findings", []):
                db.add(ForensicFinding(
                    finding_id=f["finding_id"],
                    document_id=doc_id,
                    category=f["category"],
                    status=f["status"],
                    severity=f["severity"],
                    description=f["description"],
                    evidence=f["evidence"],
                    limitations=f["limitations"],
                    model_version=f.get("model_version")
                ))

            # Save claims
            for vc in verified_claims:
                db.add(ExtractedClaim(
                    claim_id=vc["claim_id"],
                    document_id=doc_id,
                    claim_text=vc["claim_text"],
                    subject=vc["subject"],
                    predicate=vc["predicate"],
                    object=vc["object"],
                    verification_status=vc["verification_status"],
                    confidence_score=vc["confidence_score"],
                    reasoning=vc["reasoning"],
                    limitations=vc["limitations"]
                ))
                for ev_idx, ev in enumerate(vc.get("evidence_items", [])):
                    db.add(ClaimEvidence(
                        evidence_id=f"EV-{vc['claim_id'][-6:]}-{ev_idx + 1}-{uuid.uuid4().hex[:6].upper()}",
                        claim_id=vc["claim_id"],
                        document_id=doc_id,
                        source_title=ev["source_title"],
                        source_url=ev["source_url"],
                        source_authority=ev.get("authority"),
                        publication_date=ev.get("publication_date"),
                        passage_text=ev["passage_text"],
                        alignment_label=ev.get("alignment_label", "NEUTRAL"),
                        similarity_score=ev.get("similarity_score", 0.0)
                    ))

            # Save provenance
            for n in provenance_data.get("nodes", []):
                db.add(ProvenanceNode(
                    document_id=doc_id,
                    node_id=n["id"],
                    node_type=n["node_type"],
                    label=n["label"],
                    metadata_json=n
                ))
            for e in provenance_data.get("edges", []):
                db.add(ProvenanceEdge(
                    document_id=doc_id,
                    source_node=e["source"],
                    target_node=e["target"],
                    relation_type=e["relation_type"],
                    confidence=e.get("confidence", 1.0),
                    evidence_basis=e.get("evidence_basis")
                ))

            db.commit()
            print(f"[VERITRACE] Seeded '{filename}' -> ID: {doc_id} (Verdict: {overall['verdict']})")

        except Exception as e:
            print(f"[VERITRACE] Seed failed for '{filename}': {str(e)}")
            db.rollback()
