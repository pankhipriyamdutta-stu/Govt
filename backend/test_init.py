import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, SessionLocal
from app.services.seed_service import seed_database
from app.models.document import Document
from app.models.user import User
from app.models.audit import QueryAuditLog
from app.services.ai_service import AIService
from app.services.detective_service import SourceDetectiveService

def test_system_initialization():
    print("[TEST] Initializing database and running master seed...")
    db = SessionLocal()
    try:
        seed_database(db)
        
        # Verify Document count
        doc_count = db.query(Document).count()
        print(f"[TEST PASS] Seeded Documents: {doc_count}")
        assert doc_count > 0, "No documents seeded!"

        # Verify User count
        user_count = db.query(User).count()
        print(f"[TEST PASS] Seeded Users: {user_count}")
        assert user_count >= 6, "Expected at least 6 demo users for RBAC!"

        # Verify Tripartite Query Execution
        # Case 1: VERIFIED (SC/ST Exemption Assam Act XXXI of 2024)
        res1 = AIService.process_query(db, "Do SC and ST applicants have to pay fees for Assam government exams?")
        print(f"[TEST PASS] Query 1 Status: {res1['status']} (Expected: VERIFIED)")
        assert res1['status'] == "VERIFIED", f"Expected VERIFIED, got {res1['status']}"

        # Case 2: VERIFICATION_REQUIRED (GMC 2013 Citizen Charter)
        res2 = AIService.process_query(db, "What is the time limit for issuing a Birth Certificate in Guwahati Municipal Corporation?")
        print(f"[TEST PASS] Query 2 Status: {res2['status']} (Expected: VERIFICATION_REQUIRED)")
        assert res2['status'] == "VERIFICATION_REQUIRED", f"Expected VERIFICATION_REQUIRED, got {res2['status']}"

        # Case 3: CANNOT_GENERATE (Cadre 2026 non-existent gazette trap)
        res3 = AIService.process_query(db, "What is the IAS Cadre strength for Assam under the 2026 notification?")
        print(f"[TEST PASS] Query 3 Status: {res3['status']} (Expected: CANNOT_GENERATE)")
        assert res3['status'] == "CANNOT_GENERATE", f"Expected CANNOT_GENERATE, got {res3['status']}"

        # Case 4: Source Detective Forensic Inspection
        trail = SourceDetectiveService.get_claim_evidence_trail(db, "CLM-SCST-001")
        print(f"[TEST PASS] Source Detective Claim Trail: {trail['claim_id']} -> {trail['document_title']}")
        assert trail['document_id'] == "DOC-AS-SCST-001", "Detective returned wrong document!"

        print("\nALL SYSTEM INITIALIZATION AND TRUST TESTS PASSED SUCCESSFULLY!")
    finally:
        db.close()

if __name__ == "__main__":
    test_system_initialization()
