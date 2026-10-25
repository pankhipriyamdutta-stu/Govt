import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.services.auth_service import create_access_token

client = TestClient(app)

def test_sovereign_security_headers():
    """Verifies mandatory CERT-In and GIGW 3.0 government security headers."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    headers = response.headers
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-xss-protection") == "1; mode=block"
    assert "Strict-Transport-Security" in headers or "strict-transport-security" in headers
    assert "Content-Security-Policy" in headers or "content-security-policy" in headers
    assert headers.get("x-govt-security-zone") == "RESTRICTED-SOVEREIGN-SECURE"

def test_zero_trust_unauthenticated_rejection():
    """Verifies that unauthenticated requests to protected identity endpoints are blocked with 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert "credentials missing or invalid" in response.json()["detail"].lower()

def test_demo_login_and_authenticated_access():
    """Verifies issuing a cryptographically signed token and authenticating with it."""
    # 1. Obtain demo token
    login_res = client.post("/api/v1/auth/demo-login", json={"username": "officer_sharma"})
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    token = data["access_token"]
    assert len(token.split(".")) == 3

    # 2. Access protected profile
    profile_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_res.status_code == 200
    profile_data = profile_res.json()
    assert profile_data["username"] == "officer_sharma"
    assert profile_data["security_clearance"] == "SOVEREIGN_GOVERNMENT_AUTHORIZED"

def test_session_logout_and_revocation():
    """Verifies that logging out revokes the JWT and blocks replay attacks."""
    login_res = client.post("/api/v1/auth/demo-login", json={"username": "reviewer_baruah"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # Profile access works
    res1 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res1.status_code == 200

    # Logout to revoke
    logout_res = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
        json={"token": token}
    )
    assert logout_res.status_code == 200

    # Subseqent access with revoked token is blocked
    res2 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res2.status_code == 401
    assert "revoked" in res2.json()["detail"].lower()

def test_cca_trust_store_endpoint():
    """Verifies Controller of Certifying Authorities (CCA) India root trust anchors."""
    response = client.get("/api/v1/security/cca-trust-store")
    assert response.status_code == 200
    data = response.json()
    anchors = data["trust_anchors"]
    assert "nic_ca" in anchors
    assert "emudhra" in anchors
    assert "cdac" in anchors
    assert anchors["nic_ca"]["licensed_under_cca"] is True
    assert anchors["nic_ca"]["trust_tier"] == "SOVEREIGN_GOVERNMENT_ROOT"

def test_security_posture_endpoint():
    """Verifies live security posture and threat intelligence metrics."""
    response = client.get("/api/v1/security/posture")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SOVEREIGN_GOVERNMENT_HARDENED"
    assert data["cert_in_compliance"]["status"] == "COMPLIANT"
    assert data["cryptographic_integrity"]["dual_hash_engine"] == "SHA-256 + SHA-512"

def test_automated_penetration_test():
    """Executes the automated ethical hacking suite and asserts 100% defense score."""
    response = client.post("/api/v1/security/run-penetration-test")
    assert response.status_code == 200
    data = response.json()
    assert data["defense_score_percentage"] == 100.0
    assert data["overall_status"] == "SECURE_AND_GOVERNMENT_READY"
    assert len(data["test_results"]) >= 6

def test_cert_in_incident_reporting():
    """Verifies official Form CERT-In-IR-01 incident reporting generation."""
    response = client.get("/api/v1/security/cert-in/incidents")
    assert response.status_code == 200
    incidents = response.json()
    assert isinstance(incidents, list)
    if len(incidents) > 0:
        inc = incidents[0]
        assert inc["cert_in_form_id"] == "CERT-In-IR-01"
        assert "reporting_organization" in inc
        assert inc["reporting_organization"]["ntp_synchronized"] is True
