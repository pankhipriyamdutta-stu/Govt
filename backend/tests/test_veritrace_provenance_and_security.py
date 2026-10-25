import pytest
from app.services.veritrace.provenance_service import ProvenanceService
from app.services.veritrace.evidence_retrieval import EvidenceRetrievalService

def test_provenance_graph_generation():
    claims_sample = [
        {
            "claim_id": "CLM-TEST-01",
            "claim_text": "Section 4 provides public services within stipulated time limit.",
            "subject": "Section 4",
            "verification_status": "SUPPORTED",
            "evidence_items": [
                {
                    "source_title": "The Assam Right to Public Services Act, 2012",
                    "source_url": "https://artpsa.assam.gov.in/acts/artps-act-2012.pdf",
                    "authority": "Administrative Reforms and Training Department",
                    "publication_date": "2nd May, 2012",
                    "passage_text": "Every eligible person shall have the right to obtain public service within stipulated time limit.",
                    "alignment_label": "SUPPORTS",
                    "similarity_score": 0.88
                }
            ]
        }
    ]

    graph = ProvenanceService.generate_provenance_graph(
        document_id="VT-DOC-TEST99",
        filename="gazette_test.pdf",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        metadata={"author": "Govt of Assam Secretariat"},
        signature_details={"has_signature": True, "signer_name": "Samir K. Sinha, IAS", "cca_ca": "NIC-CA"},
        ref_hash_status="MATCHES_TRUSTED_REFERENCE",
        claims_with_evidence=claims_sample
    )

    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) >= 3
    assert len(graph["edges"]) >= 2

    node_types = [n["node_type"] for n in graph["nodes"]]
    assert "DOCUMENT" in node_types
    assert "ISSUER" in node_types
    assert "CLAIM" in node_types

    edge_relations = [e["relation_type"] for e in graph["edges"]]
    assert any(r in edge_relations for r in ["CITES", "PUBLISHED_AT", "COPIED_FROM", "SUPPORTS"])

    # Verify audit scope reporting
    assert "search_audit" in graph
    assert len(graph["search_audit"]["searched_sources"]) > 0
    assert len(graph["search_audit"]["unavailable_sources"]) > 0

def test_ssrf_protection():
    # Loopback addresses
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://127.0.0.1/admin") is False
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://localhost:8000/keys") is False
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://[::1]/secret") is False

    # Cloud metadata service (AWS/GCP/Azure)
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://169.254.169.254/latest/meta-data/") is False
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://metadata.google.internal/computeMetadata/v1/") is False

    # Private RFC 1918 addresses
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://10.0.0.1/internal") is False
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://192.168.1.1/router") is False
    assert EvidenceRetrievalService.is_ssrf_safe_url("http://172.16.0.5/docker") is False

    # Non-HTTP protocols
    assert EvidenceRetrievalService.is_ssrf_safe_url("file:///etc/passwd") is False
    assert EvidenceRetrievalService.is_ssrf_safe_url("gopher://evil.com") is False

    # Legitimate external URLs
    assert EvidenceRetrievalService.is_ssrf_safe_url("https://artpsa.assam.gov.in/acts/artps-act-2012.pdf") is True
    assert EvidenceRetrievalService.is_ssrf_safe_url("https://tax.assam.gov.in/gazette/agst-act-2017.pdf") is True
