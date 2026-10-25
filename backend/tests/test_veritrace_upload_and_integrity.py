import pytest
import io
import os
from fastapi.testclient import TestClient
from app.main import app
from app.services.veritrace.hashing_service import HashingService
from app.services.veritrace.document_processor import DocumentProcessor

client = TestClient(app)

def test_veritrace_health():
    response = client.get("/api/v1/veritrace/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["capabilities"]["dual_hashing_sha256_sha512"] is True
    assert data["malware_scanner_configured"] is False
    assert "no external scanner configured" in data["malware_scanner_notice"]

def test_hashing_service_calculation():
    sample_bytes = b"VERITRACE AI Cryptographic Integrity Attestation"
    sha256_val = HashingService.calculate_bytes_sha256(sample_bytes)
    sha512_val = HashingService.calculate_bytes_sha512(sample_bytes)
    assert len(sha256_val) == 64
    assert len(sha512_val) == 128

def test_reference_hash_evaluation_registered():
    # Test known registered official gazette hash
    known_hash = "3f3bf438dd8b95fb1b1e6191b9b00cb318d1844bca1dd13a5e8c148ca7c6f011"
    res = HashingService.evaluate_reference_hash(known_hash)
    assert res["status"] == "MATCHES_TRUSTED_REFERENCE"
    assert res["is_match"] is True
    assert "Assam Goods and Services Tax Act" in res["trusted_source"]

def test_reference_hash_evaluation_unregistered():
    unregistered_hash = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    res = HashingService.evaluate_reference_hash(unregistered_hash)
    assert res["status"] == "NO_TRUSTED_REFERENCE"
    assert res["is_match"] is False

def create_valid_test_pdf(text: str = "Official Gazette Verification Record") -> bytes:
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((50, 72), text, fontsize=12)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def test_upload_valid_minimal_pdf():
    valid_pdf = create_valid_test_pdf("The Assam Right to Public Services Act Notification 2012")

    response = client.post(
        "/api/v1/veritrace/upload",
        files={"file": ("test_doc.pdf", io.BytesIO(valid_pdf), "application/pdf")},
        data={"uploaded_by": "test_officer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UPLOAD_ACCEPTED"
    assert data["document_id"].startswith("VT-DOC-")
    assert len(data["sha256_hash"]) == 64
    assert data["malware_scan"]["status"] == "NOT_PERFORMED"
    assert "no external scanner configured" in data["malware_scan"]["details"]

def test_upload_empty_file_rejected():
    response = client.post(
        "/api/v1/veritrace/upload",
        files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_upload_unsupported_file_extension():
    response = client.post(
        "/api/v1/veritrace/upload",
        files={"file": ("malicious.exe", io.BytesIO(b"MZ\x90\x00executable"), "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "unsupported file extension" in response.json()["detail"].lower()

def test_upload_disguised_file_signature_mismatch():
    # .pdf extension but binary header is not a valid PDF
    fake_pdf = b"NOT_A_PDF_HEADER_DATA_STREAM"
    response = client.post(
        "/api/v1/veritrace/upload",
        files={"file": ("fake.pdf", io.BytesIO(fake_pdf), "application/pdf")}
    )
    assert response.status_code == 400
    assert "file signature does not match" in response.json()["detail"].lower()

def test_upload_path_traversal_sanitization():
    valid_pdf = create_valid_test_pdf("Path traversal defense verification document")
    response = client.post(
        "/api/v1/veritrace/upload",
        files={"file": ("../../../../etc/passwd.pdf", io.BytesIO(valid_pdf), "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    # Filename must be sanitized and contain no directory traversal
    assert ".." not in data["filename"]
    assert "/" not in data["filename"]
    assert "\\" not in data["filename"]
