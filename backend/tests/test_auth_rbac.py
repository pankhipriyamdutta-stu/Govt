from app.models.user import User, Role
from app.services.auth_service import hash_password, verify_password, create_access_token, decode_token, authenticate_user

def test_password_hashing():
    pw = "SuperSecureGovt@2026"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_tamper_evidence():
    token = create_access_token({"sub": "officer_sharma", "role": "ROL-002"})
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "officer_sharma"
    assert decoded["role"] == "ROL-002"

    # Tamper with token payload
    tampered_token = token[:-4] + "ABCD"
    assert decode_token(tampered_token) is None

def test_user_authentication_rbac(db_session):
    user = authenticate_user(db_session, "officer_sharma", "GovtSecure@2026")
    assert user is not None
    assert user.role.role_id == "ROL-002"
    assert user.department.code == "DEPT-FIN"

    # Invalid login
    invalid = authenticate_user(db_session, "officer_sharma", "WrongPass")
    assert invalid is None
