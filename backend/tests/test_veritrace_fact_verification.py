import pytest
from app.services.veritrace.claim_extractor import ClaimExtractor
from app.services.veritrace.evidence_retrieval import EvidenceRetrievalService
from app.services.veritrace.fact_verification import FactVerificationEngine

def test_claim_extraction_statute():
    text = "The Assam Right to Public Services Act was enacted in 2012 by the State Assembly."
    claims = ClaimExtractor.extract_claims(text)
    assert len(claims) > 0
    c = claims[0]
    assert "claim_text" in c
    assert "Assam Right to Public Services Act" in c["subject"]
    assert c["predicate"] == "established_in"
    assert "2012" in c["object"]

def test_evidence_retrieval_official_corpus():
    query = "The Assam Right to Public Services Act delivery of public services stipulated time limit"
    evidence = EvidenceRetrievalService.retrieve_evidence_for_claim(query, subject="Assam Right to Public Services Act")
    assert len(evidence) > 0
    assert any("artpsa.assam.gov.in" in e["source_url"] for e in evidence)
    assert any("stipulated time limit" in e["passage_text"] for e in evidence)

def test_fact_verification_supported():
    claim = {
        "claim_text": "The Assam Right to Public Services Act was enacted in 2012 to provide public services within stipulated time limit.",
        "subject": "Assam Right to Public Services Act",
        "predicate": "established_in",
        "object": "2012"
    }
    res = FactVerificationEngine.verify_claim(claim)
    assert res["verification_status"] == "SUPPORTED"
    assert res["confidence_score"] >= 0.70
    assert len(res["evidence_items"]) > 0
    assert res["evidence_items"][0]["alignment_label"] == "SUPPORTS"

def test_fact_verification_contradicted():
    # Claim asserting incorrect year 1985 for an Act enacted in 2012
    claim = {
        "claim_text": "The Assam Right to Public Services Act was enacted in 1985 by Dispur.",
        "subject": "Assam Right to Public Services Act",
        "predicate": "established_in",
        "object": "1985"
    }
    res = FactVerificationEngine.verify_claim(claim)
    assert res["verification_status"] == "CONTRADICTED"
    assert res["confidence_score"] >= 0.75
    assert "contradicts" in res["reasoning"].lower()

def test_fact_verification_insufficient_evidence():
    claim = {
        "claim_text": "Random Martian University signed a bilateral memorandum of understanding on Mars in 2099.",
        "subject": "Random Martian University",
        "predicate": "signed_mou",
        "object": "Mars"
    }
    res = FactVerificationEngine.verify_claim(claim)
    assert res["verification_status"] == "INSUFFICIENT_EVIDENCE"
    assert res["confidence_score"] == 0.0
    assert len(res["evidence_items"]) == 0
