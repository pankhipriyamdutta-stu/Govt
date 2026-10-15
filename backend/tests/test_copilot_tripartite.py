from app.services.ai_service import AIService

def test_tripartite_verified_statute(db_session):
    # Assam Act XXXI of 2024: SC/ST candidates examination fee exemption
    res = AIService.process_query(
        db_session,
        "Do SC and ST applicants have to pay fees for Assam government exams?"
    )
    assert res["status"] == "VERIFIED"
    assert "exemption" in res["answer"].lower() or "exempted" in res["answer"].lower()
    assert len(res["claims"]) >= 1
    assert len(res["citations"]) >= 1
    assert res["citations"][0]["document_id"] == "DOC-AS-SCST-001"

def test_tripartite_verification_required_caveat(db_session):
    # GMC 2013 Citizen Charter: Birth Certificate 15 days, authored by omprakash on Nitro Pro
    res = AIService.process_query(
        db_session,
        "What is the time limit for issuing a Birth Certificate in Guwahati Municipal Corporation?"
    )
    assert res["status"] == "VERIFICATION_REQUIRED"
    assert "15 days" in res["answer"]
    assert "omprakash" in res["answer"] or "2013" in res["answer"]
    assert len(res["citations"]) >= 1

def test_tripartite_cannot_generate_abstention(db_session):
    # Asking for 2026 cadre notification before published
    res = AIService.process_query(
        db_session,
        "What is the IAS Cadre strength for Assam under the 2026 notification?"
    )
    assert res["status"] == "CANNOT_GENERATE"
    assert "abstains" in res["answer"].lower() or "no 2026 cadre revision" in res["answer"].lower()
    assert len(res["claims"]) == 0
    assert len(res["citations"]) == 0
