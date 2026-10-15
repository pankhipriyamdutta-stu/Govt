import os
from app.services.crypto_service import inspect_pdf_authenticity, calculate_sha256
from app.config import settings

def test_sha256_calculation():
    # Test on real Assam ARTPS Act PDF if exists
    test_pdf = os.path.join(settings.SOURCE_DOCS_DIR, "ARTPS ACT.pdf")
    if os.path.exists(test_pdf):
        sha = calculate_sha256(test_pdf)
        assert len(sha) == 64
        # Validate deterministic hash calculation on physical PDF
        assert sha.startswith("e8d7fd46b5b8")

def test_suspect_producer_anomaly_detection():
    # In ARTPS ACT.pdf, producer is 'http://www.adultpdf.com'
    test_pdf = os.path.join(settings.SOURCE_DOCS_DIR, "ARTPS ACT.pdf")
    if os.path.exists(test_pdf):
        inspection = inspect_pdf_authenticity(test_pdf)
        assert len(inspection["metadata_anomalies"]) > 0
        assert any("adultpdf" in a.lower() for a in inspection["metadata_anomalies"])
        assert inspection["trust_recommendation"].startswith("VERIFICATION_REQUIRED")

def test_unsigned_document_honesty():
    # Physical scans lack digital signatures; system must report NO_CRYPTOGRAPHIC_SIG rather than faking
    test_pdf = os.path.join(settings.SOURCE_DOCS_DIR, "untitled_23.pdf")
    if os.path.exists(test_pdf):
        inspection = inspect_pdf_authenticity(test_pdf)
        assert inspection["has_digital_signature"] is False
        assert inspection["signature_format"] == "NO_CRYPTOGRAPHIC_SIG"
