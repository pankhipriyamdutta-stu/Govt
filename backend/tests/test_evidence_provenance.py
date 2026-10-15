from app.services.detective_service import SourceDetectiveService
from app.models.audit import QueryAuditLog

def test_source_detective_forensic_trail(db_session):
    trail = SourceDetectiveService.get_claim_evidence_trail(db_session, "CLM-SCST-001")
    assert trail is not None
    assert trail["claim_id"] == "CLM-SCST-001"
    assert trail["document_id"] == "DOC-AS-SCST-001"
    assert "Section 2" in trail["locator"]["section_number"]
    assert len(trail["source_file_hash"]) == 64
    assert len(trail["evidence_hash"]) == 64
    assert trail["cryptographic_verification"]["signature_format"] == "NO_CRYPTOGRAPHIC_SIG"

def test_tamper_evident_audit_log_chain(db_session):
    logs = db_session.query(QueryAuditLog).order_by(QueryAuditLog.id.asc()).all()
    assert len(logs) >= 4
    for i in range(1, len(logs)):
        # Verify previous_hash connects directly to previous entry's tamper_hash
        assert logs[i].previous_hash == logs[i-1].tamper_hash, f"Tamper chain broken between log {logs[i-1].id} and {logs[i].id}"
