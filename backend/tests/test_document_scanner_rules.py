import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_service import AIService
from app.database import SessionLocal

client = TestClient(app)

def test_document_scanner_scst_rules():
    """Verify scanning and rule extraction on Assam SC/ST Amendment Act 2024."""
    db = SessionLocal()
    try:
        res = AIService.scan_and_extract_document_rules(db, document_id="DOC-AS-SCST-001")
        assert res["document_id"] == "DOC-AS-SCST-001"
        assert "XXXI of 2024" in res["document_title"]
        assert res["trust_and_compliance"]["tripartite_verdict"] == "VERIFIED"
        assert res["trust_and_compliance"]["authority_tier"] == "ZONE_1_PRIMARY_STATE_GAZETTE"
        
        # Verify extracted rules
        rules = res["statutory_rules"]
        assert len(rules) >= 2
        sec5a1 = next((r for r in rules if "5A(1)" in r["section_number"]), None)
        assert sec5a1 is not None
        assert "Exemption of Examination Fees" in sec5a1["rule_title"]
        assert "Scheduled Castes and Scheduled Tribes" in sec5a1["exact_statutory_text"]
        
        # Verify forensic scan
        assert len(res["forensic_scan"]["sha256_hash"]) == 64
        assert "Print To PDF" in res["forensic_scan"]["producer"]
    finally:
        db.close()

def test_document_scanner_artps_converter_anomaly():
    """Verify forensic converter anomaly detection on ARTPS Act 2012."""
    db = SessionLocal()
    try:
        res = AIService.scan_and_extract_document_rules(db, document_id="DOC-AS-ARTPS-001")
        assert res["document_id"] == "DOC-AS-ARTPS-001"
        assert res["trust_and_compliance"]["tripartite_verdict"] == "VERIFICATION_REQUIRED"
        assert res["forensic_scan"]["has_converter_anomaly"] is True
        assert "adultpdf" in res["forensic_scan"]["producer"]
        
        # Verify extracted penalty clause
        sec7 = next((r for r in rules if "7(1)" in r["section_number"]), None) if "rules" in locals() else None
        rules = res["statutory_rules"]
        sec7 = next((r for r in rules if "7(1)" in r["section_number"]), None)
        assert sec7 is not None
        assert "250 per day" in sec7["exact_statutory_text"]
        assert "25,000" in sec7["exact_statutory_text"]
    finally:
        db.close()

def test_document_scanner_pii_quarantine():
    """Verify quarantine defense when scanning citizen personal ID card."""
    db = SessionLocal()
    try:
        res = AIService.scan_and_extract_document_rules(db, document_id="EXC-ID-001")
        assert res["trust_and_compliance"]["tripartite_verdict"] == "CANNOT_GENERATE"
        assert "CRITICAL" in res["trust_and_compliance"]["pii_risk_detected"]
        assert len(res["statutory_rules"]) == 0
    finally:
        db.close()

def test_document_scanner_api_endpoint():
    """Verify POST /api/v1/documents/scan-rules endpoint."""
    response = client.post("/api/v1/documents/scan-rules", json={"document_id": "DOC-AS-SCST-001"})
    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == "DOC-AS-SCST-001"
    assert data["trust_and_compliance"]["tripartite_verdict"] == "VERIFIED"
    assert len(data["statutory_rules"]) >= 2
