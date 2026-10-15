import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "NESFIC-D-36 — Trusted Government Knowledge, Rules & Document Assistant"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nesfic-d36-secure-tamper-evident-jwt-secret-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 12 hours
    
    # Database (SQLite zero-dependency fallback + Postgres compatible)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend_gov.db")
    
    # Storage Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    QUARANTINE_DIR: str = os.path.join(BASE_DIR, "quarantine")
    SOURCE_DOCS_DIR: str = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "source_documents"))
    DATASET_CSV_DIR: str = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "dataset_csv_sheets"))
    
    # Demo and Security Modes
    DEMO_MODE: bool = True
    ENVIRONMENT_NAME: str = "DEMONSTRATION & PILOT ENVIRONMENT — NESFIC 2026"
    
    # AI Engine
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    DEFAULT_MODEL_NAME: str = "gemini-2.5-flash"
    
    # Grounding & Trust Policy
    ENFORCE_PRIMARY_AUTHORITY_ONLY: bool = True
    STRICT_ABSTENTION_THRESHOLD: float = 0.85

settings = Settings()

# Ensure critical storage folders exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.QUARANTINE_DIR, exist_ok=True)
