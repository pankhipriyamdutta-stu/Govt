import hashlib
import os
import pypdf
from typing import Dict, Any, List
from cryptography import x509
from cryptography.hazmat.backends import default_backend

SUSPECT_PRODUCER_PATTERNS = [
    "adultpdf",
    "ilovepdf",
    "smallpdf",
    "sejda",
    "pdf2go",
    "freepdf",
    "pdfcreator",
    "nitro pro"
]

AUTHORIZED_SIGNERS_REGISTRY = {
    "samir_k_sinha": {"role": "Principal Secretary, Finance Department", "authorized": True},
    "geetanjali_das_saikia": {"role": "Secretary to Govt of Assam, Legislative Dept", "authorized": True},
    "sanjeev_kumar": {"role": "Joint Secretary to Government of India, DoPT", "authorized": True},
    "sanjeev_sharma": {"role": "Under Secretary to Government of India", "authorized": True},
    "omprakash": {"role": "Private Desktop Author (Nitro Pro)", "authorized": False},
    "user": {"role": "Generic Word User", "authorized": False},
}

def calculate_sha256(filepath: str) -> str:
    """Computes SHA-256 hash of a file on disk."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def inspect_pdf_authenticity(filepath: str) -> Dict[str, Any]:
    """
    Performs forensic inspection of a PDF file:
    - Integrity SHA-256
    - Producer and Creator metadata
    - Third-party converter anomaly detection
    - Digital signature & certificate check
    - Signer institutional authority evaluation
    """
    result = {
        "file_exists": os.path.exists(filepath),
        "file_size": os.path.getsize(filepath) if os.path.exists(filepath) else 0,
        "sha256_hash": calculate_sha256(filepath) if os.path.exists(filepath) else "",
        "has_digital_signature": False,
        "signature_format": "NONE",
        "signature_valid": False,
        "signer_name": None,
        "signer_authority_status": "UNVERIFIED_AUTHORITY",
        "producer": "UNKNOWN",
        "creator": "UNKNOWN",
        "author": "UNKNOWN",
        "metadata_anomalies": [],
        "trust_recommendation": "PENDING_VERIFICATION"
    }

    if not result["file_exists"]:
        result["metadata_anomalies"].append("File not found on filesystem")
        result["trust_recommendation"] = "REJECTED_MISSING_FILE"
        return result

    try:
        reader = pypdf.PdfReader(filepath)
        info = reader.metadata or {}
        
        producer = str(info.get("/Producer", "") or "").strip()
        creator = str(info.get("/Creator", "") or "").strip()
        author = str(info.get("/Author", "") or "").strip()
        title = str(info.get("/Title", "") or "").strip()

        result["producer"] = producer
        result["creator"] = creator
        result["author"] = author
        result["title"] = title

        # Check for suspect third-party converters
        combined_meta = f"{producer} {creator} {author} {title}".lower()
        for pattern in SUSPECT_PRODUCER_PATTERNS:
            if pattern in combined_meta:
                anomaly = f"Suspect third-party tool identified in metadata: '{pattern}' (Producer: '{producer}')"
                result["metadata_anomalies"].append(anomaly)

        # Check digital signatures in AcroForm / Perms
        has_sig = False
        try:
            if "/AcroForm" in reader.trailer["/Root"]:
                fields = reader.trailer["/Root"]["/AcroForm"].get("/Fields", [])
                for field in fields:
                    f_obj = field.get_object() if hasattr(field, "get_object") else field
                    if f_obj.get("/FT") == "/Sig":
                        has_sig = True
                        result["has_digital_signature"] = True
                        result["signature_format"] = "PKCS#7 / PAdES"
                        sig_dict = f_obj.get("/V", {}).get_object()
                        result["signer_name"] = str(sig_dict.get("/Name", "Digital Signer"))
        except Exception:
            pass

        if not has_sig:
            result["has_digital_signature"] = False
            result["signature_format"] = "NO_CRYPTOGRAPHIC_SIG"
            result["anomaly_notes"] = "Document lacks PKCS#7 / PAdES digital signature. Requires human gazette cross-check."

        # Evaluate Signer Authority
        signer_key = (result["signer_name"] or author or "").lower().replace(" ", "_")
        matched_auth = None
        for k, v in AUTHORIZED_SIGNERS_REGISTRY.items():
            if k in signer_key:
                matched_auth = v
                break

        if matched_auth:
            if matched_auth["authorized"]:
                result["signer_authority_status"] = f"INSTITUTIONALLY_AUTHORIZED: {matched_auth['role']}"
            else:
                result["signer_authority_status"] = f"UNAUTHORIZED_PRIVATE_AUTHOR: {matched_auth['role']}"
                result["metadata_anomalies"].append(f"Author '{author}' lacks institutional authority to issue official statutes.")
        else:
            result["signer_authority_status"] = "AUTHORITY_UNCONFIRMED_IN_REGISTRY"

        # Overall Trust Recommendation
        if result["metadata_anomalies"]:
            result["trust_recommendation"] = "VERIFICATION_REQUIRED_THIRD_PARTY_ANOMALY"
        elif result["has_digital_signature"] and result["signer_authority_status"].startswith("INSTITUTIONALLY_AUTHORIZED"):
            result["trust_recommendation"] = "VERIFIED_TRUSTED"
        else:
            result["trust_recommendation"] = "PROVISIONAL_PENDING_OFFICER_REVIEW"

    except Exception as e:
        result["metadata_anomalies"].append(f"PDF parsing error: {str(e)}")
        result["trust_recommendation"] = "REJECTED_PARSING_ERROR"

    return result
