import os
from typing import Optional, List

class Settings:
    PROJECT_NAME: str = "NESFIC-D-36 — Sovereign Government Knowledge & Document Security Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nesfic-d36-sovereign-gov-in-tamper-evident-ed25519-sha256-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 12 hours
    
    # Government Security & Zero-Trust Enforcement
    GOVERNMENT_SECURITY_MODE: bool = os.getenv("GOVERNMENT_SECURITY_MODE", "True").lower() == "true"
    STRICT_ZERO_TRUST: bool = os.getenv("STRICT_ZERO_TRUST", "True").lower() == "true"
    ENFORCE_MFA_FOR_ADMIN: bool = True
    
    # CERT-In Incident Response Configuration
    ENABLE_CERT_IN_REPORTING: bool = True
    CERT_IN_CONSTITUENCY: str = "Government of India / State Government of Assam"
    CERT_IN_OFFICIAL_EMAIL: str = "incident@cert-in.org.in"
    CERT_IN_TIMEZONE: str = "Asia/Kolkata (IST, UTC+05:30)"
    
    # Rate Limiting & DoS Shield
    RATE_LIMIT_LOGIN_MAX_PER_MINUTE: int = 15
    RATE_LIMIT_QUERY_MAX_PER_MINUTE: int = 60
    
    # Whitelisted Origins & Hosts (CERT-In / GIGW 3.0 Strict Origin Policy)
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*.gov.in", "*.nic.in"]
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Database (SQLite zero-dependency fallback + Postgres compatible)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend_gov.db")
    
    # Storage Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    QUARANTINE_DIR: str = os.path.join(BASE_DIR, "quarantine")
    SOURCE_DOCS_DIR: str = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "source_documents"))
    DATASET_CSV_DIR: str = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "dataset_csv_sheets"))
    
    # Environment & Sovereign Security Posture
    DEMO_MODE: bool = False
    ENVIRONMENT_NAME: str = "SOVEREIGN GOVERNMENT CLOUD // NIC SECURE ENCLAVE"
    
    # AI Engine
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    DEFAULT_MODEL_NAME: str = "gemini-2.5-flash"
    
    # Grounding & Trust Policy
    ENFORCE_PRIMARY_AUTHORITY_ONLY: bool = True
    STRICT_ABSTENTION_THRESHOLD: float = 0.85
    DPDP_ACT_2023_COMPLIANCE: bool = True

settings = Settings()

# Ensure critical storage folders exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.QUARANTINE_DIR, exist_ok=True)

