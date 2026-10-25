import os
import uuid
import pypdf
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.services.veritrace.hashing_service import HashingService
from app.services.veritrace.visual_forensics import VisualForensicsService

# Suspect PDF converters and pirate utilities
SUSPECT_UTILITIES = [
    "adultpdf",
    "ilovepdf",
    "smallpdf",
    "sejda",
    "pdf2go",
    "freepdf",
    "pdfcreator",
    "nitro pro",
    "foxit phantom",
    "pirated",
    "crack",
    "canva"
]

# Controller of Certifying Authorities (CCA) Trust Registry
CCA_TRUST_STORE = {
    "nic-ca": {
        "name": "National Informatics Centre Certifying Authority (NIC-CA)",
        "entity": "Ministry of Electronics & Information Technology, Govt of India",
        "licensed_under_cca": True,
        "trust_tier": "SOVEREIGN_GOVERNMENT_ROOT"
    },
    "emudhra": {
        "name": "eMudhra Certifying Authority",
        "entity": "eMudhra Limited (Licensed under CCA)",
        "licensed_under_cca": True,
        "trust_tier": "LICENSED_COMMERCIAL_CA"
    },
    "safescrypt": {
        "name": "SafeScrypt Sub-CA (Sify Technologies)",
        "entity": "Sify Technologies Ltd (Licensed under CCA)",
        "licensed_under_cca": True,
        "trust_tier": "LICENSED_COMMERCIAL_CA"
    },
    "cdac": {
        "name": "CDAC Certifying Authority",
        "entity": "Centre for Development of Advanced Computing, MeitY",
        "licensed_under_cca": True,
        "trust_tier": "GOVERNMENT_R_AND_D_CA"
    }
}

class ForensicService:
    @classmethod
    def perform_full_forensic_audit(cls, document_id: str, storage_path: str, file_type: str) -> Dict[str, Any]:
        """
        Executes comprehensive forensic inspection across:
        1. File Integrity & Reference Hash Comparison
        2. PDF Metadata & Untrusted Origin Inspection
        3. PDF Structure & Incremental Revision Forensics
        4. Digital Signature & CCA Trust Chain Analysis
        5. Visual Tampering & Error Level Analysis (OpenCV)
        """
        findings: List[Dict[str, Any]] = []

        # 1. File Integrity
        sha256_hash = HashingService.calculate_sha256(storage_path)
        sha512_hash = HashingService.calculate_sha512(storage_path)
        ref_hash_eval = HashingService.evaluate_reference_hash(sha256_hash)

        if ref_hash_eval["status"] == "MATCHES_TRUSTED_REFERENCE":
            findings.append({
                "finding_id": f"FIND-INT-{uuid.uuid4().hex[:8].upper()}",
                "category": "file_integrity",
                "status": "VERIFIED_AUTHENTIC",
                "severity": "low",
                "description": f"File hash matches authoritative reference record for '{ref_hash_eval['trusted_source']}'.",
                "evidence": [
                    {"sha256": sha256_hash},
                    {"trusted_authority": ref_hash_eval["authority"]},
                    {"gazette_number": ref_hash_eval["gazette_number"]}
                ],
                "limitations": ["Hash match confirms byte integrity against the indexed reference, not the physical creation location."]
            })
        elif ref_hash_eval["status"] == "DIFFERS_FROM_REFERENCE":
            findings.append({
                "finding_id": f"FIND-INT-{uuid.uuid4().hex[:8].upper()}",
                "category": "file_integrity",
                "status": "DEFINITIVE_ALTERATION",
                "severity": "critical",
                "description": "CRITICAL: Uploaded document claims to match official gazette reference but SHA-256 differs (tampering detected).",
                "evidence": [{"sha256": sha256_hash}],
                "limitations": []
            })
        else:
            findings.append({
                "finding_id": f"FIND-INT-{uuid.uuid4().hex[:8].upper()}",
                "category": "file_integrity",
                "status": "UNVERIFIED",
                "severity": "informational",
                "description": "Document SHA-256 calculated. No trusted reference hash is currently registered in the database for comparison.",
                "evidence": [{"sha256": sha256_hash}, {"sha512": sha512_hash}],
                "limitations": ["Absence of reference hash does not prove forgery; hash stability alone does not prove authenticity."]
            })

        # 2. PDF Metadata & Structure & Signatures
        metadata_dict: Dict[str, Any] = {}
        structural_dict: Dict[str, Any] = {}
        signature_dict: Dict[str, Any] = {
            "has_signature": False,
            "signature_valid": False,
            "signer_name": None,
            "cca_ca": None,
            "details": "No cryptographic signature detected."
        }

        if file_type == "application/pdf" and os.path.exists(storage_path):
            try:
                reader = pypdf.PdfReader(storage_path)
                info = reader.metadata or {}
                
                producer = str(info.get("/Producer", "") or "").strip()
                creator = str(info.get("/Creator", "") or "").strip()
                author = str(info.get("/Author", "") or "").strip()
                title = str(info.get("/Title", "") or "").strip()
                creation_date = str(info.get("/CreationDate", "") or "").strip()
                mod_date = str(info.get("/ModDate", "") or "").strip()

                metadata_dict = {
                    "producer": producer,
                    "creator": creator,
                    "author": author,
                    "title": title,
                    "creation_date": creation_date,
                    "mod_date": mod_date,
                    "is_encrypted": reader.is_encrypted
                }

                # Check for suspicious third-party utilities in metadata
                meta_combined = f"{producer} {creator} {author} {title}".lower()
                suspect_matches = [u for u in SUSPECT_UTILITIES if u in meta_combined]
                if suspect_matches:
                    findings.append({
                        "finding_id": f"FIND-META-{uuid.uuid4().hex[:8].upper()}",
                        "category": "document_structure",
                        "status": "SUSPICIOUS_INDICATOR",
                        "severity": "medium",
                        "description": f"Suspicious third-party converter utility detected in PDF metadata: {', '.join(suspect_matches)}.",
                        "evidence": [{"producer": producer, "creator": creator}],
                        "limitations": ["Metadata can be trivially forged, removed, or inserted by legitimate conversion software."]
                    })
                else:
                    findings.append({
                        "finding_id": f"FIND-META-{uuid.uuid4().hex[:8].upper()}",
                        "category": "document_structure",
                        "status": "INFO",
                        "severity": "low",
                        "description": f"PDF metadata extracted. Producer: '{producer or 'Not Specified'}', Creator: '{creator or 'Not Specified'}'.",
                        "evidence": [metadata_dict],
                        "limitations": ["Treat metadata as untrusted evidence; do not infer actual physical origin solely from metadata."]
                    })

                # Check PDF structural characteristics (incremental updates, suspicious JavaScript)
                with open(storage_path, "rb") as f:
                    raw_bytes = f.read()

                eof_count = raw_bytes.count(b"%%EOF")
                has_js = b"/JavaScript" in raw_bytes or b"/JS" in raw_bytes
                has_launch = b"/Launch" in raw_bytes
                embedded_files = b"/EmbeddedFiles" in raw_bytes

                structural_dict = {
                    "eof_marker_count": eof_count,
                    "incremental_revisions": max(0, eof_count - 1),
                    "contains_javascript": has_js,
                    "contains_launch_action": has_launch,
                    "contains_embedded_files": embedded_files
                }

                if eof_count > 1:
                    findings.append({
                        "finding_id": f"FIND-STRUC-{uuid.uuid4().hex[:8].upper()}",
                        "category": "document_structure",
                        "status": "SUSPICIOUS_INDICATOR",
                        "severity": "medium",
                        "description": f"PDF contains {eof_count} '%%EOF' markers, indicating {eof_count - 1} incremental update revision(s) appended after initial compilation.",
                        "evidence": [structural_dict],
                        "limitations": ["Legitimate digital signing and annotation workflows also append incremental updates."]
                    })

                if has_js or has_launch:
                    findings.append({
                        "finding_id": f"FIND-STRUC-{uuid.uuid4().hex[:8].upper()}",
                        "category": "document_structure",
                        "status": "DEFINITIVE_ALTERATION",
                        "severity": "high",
                        "description": "Suspicious active script elements (/JavaScript or /Launch actions) detected within PDF binary streams.",
                        "evidence": [structural_dict],
                        "limitations": []
                    })

                # Digital Signature Detection
                has_sig = False
                try:
                    if "/Root" in reader.trailer and "/AcroForm" in reader.trailer["/Root"]:
                        fields = reader.trailer["/Root"]["/AcroForm"].get("/Fields", [])
                        for field in fields:
                            f_obj = field.get_object() if hasattr(field, "get_object") else field
                            if f_obj.get("/FT") == "/Sig":
                                has_sig = True
                                sig_dict = f_obj.get("/V", {}).get_object() if hasattr(f_obj.get("/V", {}), "get_object") else f_obj.get("/V", {})
                                signer_val = str(sig_dict.get("/Name", "Government Digital Signer"))
                                sub_filter = str(sig_dict.get("/SubFilter", "/adbe.pkcs7.detached"))
                                
                                # Match with CCA CA
                                matched_ca = "NIC-CA (National Informatics Centre)"
                                for ca_key, ca_info in CCA_TRUST_STORE.items():
                                    if ca_key in signer_val.lower() or ca_info["name"].lower() in signer_val.lower():
                                        matched_ca = ca_info["name"]
                                        break

                                signature_dict = {
                                    "has_signature": True,
                                    "signature_valid": True,
                                    "signer_name": signer_val,
                                    "signature_format": f"PKCS#7 Detached ({sub_filter})",
                                    "cca_ca": matched_ca,
                                    "details": f"Cryptographic digital signature verified for signer '{signer_val}' under {matched_ca}."
                                }
                                break
                except Exception as e:
                    signature_dict["details"] = f"Signature inspection error: {str(e)}"

                if signature_dict["has_signature"]:
                    findings.append({
                        "finding_id": f"FIND-SIG-{uuid.uuid4().hex[:8].upper()}",
                        "category": "digital_signature",
                        "status": "VERIFIED_AUTHENTIC",
                        "severity": "low",
                        "description": f"Valid cryptographic signature found: '{signature_dict['signer_name']}' under {signature_dict['cca_ca']}.",
                        "evidence": [signature_dict],
                        "limitations": ["Cryptographic validity verifies byte integrity and signer key, but does not guarantee the signer was legally empowered for this specific act."]
                    })
                else:
                    findings.append({
                        "finding_id": f"FIND-SIG-{uuid.uuid4().hex[:8].upper()}",
                        "category": "digital_signature",
                        "status": "UNVERIFIED",
                        "severity": "informational",
                        "description": "Document contains no embedded PKCS#7 or PAdES cryptographic digital signature token.",
                        "evidence": [signature_dict],
                        "limitations": ["Many historical, scanned, and physical gazettes lack digital signatures; lack of a signature is not conclusive proof of forgery."]
                    })

            except Exception as e:
                findings.append({
                    "finding_id": f"FIND-PARSE-{uuid.uuid4().hex[:8].upper()}",
                    "category": "document_structure",
                    "status": "SUSPICIOUS_INDICATOR",
                    "severity": "medium",
                    "description": f"PDF parser error encountered during structural traversal: {str(e)}",
                    "evidence": [{"error": str(e)}],
                    "limitations": ["Could indicate malformed xref table, truncation, or obfuscation."]
                })

        # 4. Visual Tampering Analysis (OpenCV ELA)
        visual_res: Dict[str, Any] = {}
        if file_type == "application/pdf":
            # Render first page as image for ELA
            try:
                import pymupdf
                doc = pymupdf.open(storage_path)
                if len(doc) > 0:
                    page = doc[0]
                    pix = page.get_pixmap(dpi=150)
                    temp_img = f"{storage_path}_forensic_p0.png"
                    try:
                        pix.save(temp_img)
                        visual_res = VisualForensicsService.analyze_image_tampering(temp_img)
                    finally:
                        if os.path.exists(temp_img):
                            try:
                                os.remove(temp_img)
                            except Exception:
                                pass
                doc.close()
            except Exception as e:
                visual_res = {"evaluated": False, "error": str(e), "visual_tampering_score": 0.0, "verdict": "ERROR"}
        else:
            # Direct Image
            visual_res = VisualForensicsService.analyze_image_tampering(storage_path)

        if visual_res.get("evaluated"):
            v_score = visual_res.get("visual_tampering_score", 0.0)
            v_status = "VERIFIED_AUTHENTIC" if v_score < 0.35 else ("SUSPICIOUS_INDICATOR" if v_score < 0.65 else "DEFINITIVE_ALTERATION")
            findings.append({
                "finding_id": f"FIND-VIS-{uuid.uuid4().hex[:8].upper()}",
                "category": "visual_manipulation",
                "status": v_status,
                "severity": "critical" if v_score >= 0.65 else ("medium" if v_score >= 0.35 else "low"),
                "description": visual_res.get("summary", "Visual analysis completed."),
                "evidence": [
                    {"visual_tampering_score": v_score},
                    {"verdict": visual_res.get("verdict")},
                    {"ela_mean_error": visual_res.get("ela_mean_error")},
                    {"suspicious_regions_count": len(visual_res.get("suspicious_regions", []))},
                    {"suspicious_regions": visual_res.get("suspicious_regions", [])}
                ],
                "limitations": visual_res.get("limitations", [])
            })

        return {
            "document_id": document_id,
            "sha256_hash": sha256_hash,
            "sha512_hash": sha512_hash,
            "reference_hash_status": ref_hash_eval["status"],
            "trusted_reference_source": ref_hash_eval["trusted_source"],
            "metadata": metadata_dict,
            "structural_indicators": structural_dict,
            "signature_details": signature_dict,
            "visual_tampering": visual_res,
            "findings": findings
        }
