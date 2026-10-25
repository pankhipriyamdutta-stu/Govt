from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class ReportService:
    """
    Module Eight: Explainable Risk Assessment & Final Report Generation.
    Aggregates separate independent dimensions:
    - File Integrity
    - Digital Signatures
    - Visual Manipulation (OpenCV ELA)
    - Document Structure & PDF Revisions
    - Machine Learning Fraud Anomaly
    - Factual Claims Verification
    - Source Provenance Coverage
    Outputs explainable overall verdict: LOW, MODERATE, HIGH, or INSUFFICIENT_DATA.
    """

    @classmethod
    def calculate_overall_risk(
        cls,
        ref_hash_status: str,
        signature_valid: bool,
        visual_tamper_score: float,
        structural_indicators: Dict[str, Any],
        ml_fraud_score: float,
        claims_summary: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Documented risk aggregation policy:
        Avoids double-counting; missing data is classified as INSUFFICIENT_DATA rather than fraud.
        """
        # 1. Definitive Hash match check
        if ref_hash_status == "MATCHES_TRUSTED_REFERENCE":
            return {
                "verdict": "LOW",
                "risk_score": 0.05,
                "confidence": "HIGH",
                "explanation": "Cryptographic byte hash matches authoritative registered gazette in sovereign registry. Low overall fraud risk.",
                "policy_applied": "POLICY_EXACT_REFERENCE_MATCH"
            }

        if ref_hash_status == "DIFFERS_FROM_REFERENCE":
            return {
                "verdict": "HIGH",
                "risk_score": 0.95,
                "confidence": "VERY_HIGH",
                "explanation": "CRITICAL TAMPER ALERT: Document claims identity of registered official gazette but cryptographic hash differs.",
                "policy_applied": "POLICY_REFERENCE_MISMATCH_TAMPER"
            }

        # 2. Critical visual or structural tampering
        has_active_scripts = structural_indicators.get("contains_javascript", False) or structural_indicators.get("contains_launch_action", False)
        if has_active_scripts or visual_tamper_score >= 0.65:
            return {
                "verdict": "HIGH",
                "risk_score": max(0.75, visual_tamper_score),
                "confidence": "HIGH",
                "explanation": "Definitive tampering or active binary script execution tags detected within the document structure or visual layers.",
                "policy_applied": "POLICY_STRUCTURAL_VISUAL_TAMPER"
            }

        # 3. Factual contradictions
        contradicted_count = claims_summary.get("CONTRADICTED", 0)
        if contradicted_count >= 2:
            return {
                "verdict": "HIGH",
                "risk_score": 0.80,
                "confidence": "HIGH",
                "explanation": f"Multiple core factual statements ({contradicted_count}) are directly contradicted by authoritative gazette records.",
                "policy_applied": "POLICY_FACTUAL_CONTRADICTION"
            }

        # 4. Moderate risk factors
        incremental_updates = structural_indicators.get("incremental_revisions", 0)
        moderate_flags = (visual_tamper_score >= 0.35) or (incremental_updates > 2) or (ml_fraud_score >= 0.40) or (contradicted_count == 1)

        if moderate_flags:
            return {
                "verdict": "MODERATE",
                "risk_score": round(max(0.40, visual_tamper_score, ml_fraud_score), 2),
                "confidence": "MEDIUM",
                "explanation": "Moderate anomalies detected: elevated visual compression variance, multiple revision trailers, or unverified claims. Verification officer review required.",
                "policy_applied": "POLICY_MODERATE_ANOMALY"
            }

        # 5. Check data sufficiency
        total_claims = sum(claims_summary.values())
        if total_claims == 0 and not signature_valid and visual_tamper_score == 0.0:
            return {
                "verdict": "INSUFFICIENT_DATA",
                "risk_score": 0.20,
                "confidence": "LOW",
                "explanation": "Document lacks cryptographic signatures, reference hashes, or extractable factual statements. Data insufficient for definitive authenticity attestation.",
                "policy_applied": "POLICY_INSUFFICIENT_DATA"
            }

        # 6. Default clean status
        return {
            "verdict": "LOW",
            "risk_score": 0.15 if not signature_valid else 0.08,
            "confidence": "MEDIUM" if not signature_valid else "HIGH",
            "explanation": "No visual splicing, structural anomalies, or factual contradictions identified. Document exhibits normal distribution characteristics.",
            "policy_applied": "POLICY_STANDARD_CLEAN"
        }

    @classmethod
    def assemble_final_report(
        cls,
        document_record: Dict[str, Any],
        forensic_data: Dict[str, Any],
        claims_data: List[Dict[str, Any]],
        provenance_data: Dict[str, Any],
        ml_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assembles the comprehensive, explainable forensic and verification audit report.
        """
        claims_summary = {
            "SUPPORTED": 0,
            "CONTRADICTED": 0,
            "INSUFFICIENT_EVIDENCE": 0,
            "CONFLICTING_SOURCES": 0,
            "NOT_CHECKED": 0
        }
        for c in claims_data:
            st = c.get("verification_status", "NOT_CHECKED")
            claims_summary[st] = claims_summary.get(st, 0) + 1

        overall = cls.calculate_overall_risk(
            ref_hash_status=forensic_data.get("reference_hash_status", "NO_TRUSTED_REFERENCE"),
            signature_valid=forensic_data.get("signature_details", {}).get("signature_valid", False),
            visual_tamper_score=forensic_data.get("visual_tampering", {}).get("visual_tampering_score", 0.0),
            structural_indicators=forensic_data.get("structural_indicators", {}),
            ml_fraud_score=ml_data.get("fraud_probability", 0.0),
            claims_summary=claims_summary
        )

        return {
            "report_metadata": {
                "report_id": f"REP-{document_record.get('document_id', 'DOC')}",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "system_name": "VERITRACE AI Sovereign CyberSecurity Framework",
                "system_version": "v2.0-SOVEREIGN"
            },
            "document_summary": {
                "document_id": document_record.get("document_id"),
                "filename": document_record.get("original_filename"),
                "file_type": document_record.get("file_type"),
                "file_size_bytes": document_record.get("file_size_bytes"),
                "page_count": document_record.get("page_count", 1),
                "sha256_hash": document_record.get("sha256_hash"),
                "sha512_hash": document_record.get("sha512_hash"),
                "uploaded_by": document_record.get("uploaded_by"),
                "upload_timestamp": document_record.get("upload_timestamp"),
                "malware_scan": {
                    "status": document_record.get("malware_scan_status", "NOT_PERFORMED"),
                    "details": document_record.get("malware_scan_details", "Malware scanning not performed (no external scanner configured)")
                }
            },
            "executive_verdict": overall,
            "independent_dimensions": {
                "file_integrity": {
                    "sha256": document_record.get("sha256_hash"),
                    "reference_hash_status": forensic_data.get("reference_hash_status"),
                    "trusted_source": forensic_data.get("trusted_reference_source")
                },
                "digital_signatures": forensic_data.get("signature_details", {}),
                "visual_tampering_forensics": forensic_data.get("visual_tampering", {}),
                "document_structure_and_metadata": {
                    "metadata": forensic_data.get("metadata", {}),
                    "structural_indicators": forensic_data.get("structural_indicators", {})
                },
                "ml_fraud_risk": ml_data,
                "factual_accuracy": {
                    "total_claims_extracted": len(claims_data),
                    "claims_summary": claims_summary,
                    "claims": claims_data
                },
                "source_provenance": provenance_data.get("provenance_summary", {})
            },
            "all_forensic_findings": forensic_data.get("findings", []),
            "provenance_lineage": provenance_data,
            "limitations_and_assumptions": [
                "Absence of cryptographic signature in historical gazette does not constitute proof of forgery.",
                "Visual Error Level Analysis may be influenced by multiple generations of digital photocopies.",
                "Machine Learning probabilities are model estimates calibrated against standard sovereign publication baselines.",
                "Fact verification is bounded by indexed government acts, gazettes, and official department rules."
            ],
            "recommended_next_steps": [
                "If overall risk is HIGH: Dispatch original document to State Forensic Science Laboratory (FSL) and verify physical dispatch seals.",
                "If MODERATE: Request verification officer to audit cited gazette volume numbers and verify signatory appointment records.",
                "If LOW with exact reference hash match: Document is authenticated and eligible for sovereign administrative reliance."
            ]
        }
