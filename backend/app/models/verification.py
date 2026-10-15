from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from app.database import Base

class SignatureVerificationRecord(Base):
    __tablename__ = "signature_verification_records"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    has_digital_signature = Column(Boolean, default=False)
    signature_format = Column(String(50), default="NONE")  # PKCS#7, CAdES, PAdES, RAW_HASH
    certificate_subject = Column(String(255), nullable=True)
    certificate_issuer = Column(String(255), nullable=True)
    signature_valid = Column(Boolean, default=False)
    cert_chain_valid = Column(Boolean, default=False)
    signing_time = Column(String(50), nullable=True)
    signer_authority_status = Column(String(100), default="UNVERIFIED_AUTHORITY")
    anomaly_notes = Column(Text, nullable=True)
    verified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class VerificationQueue(Base):
    __tablename__ = "verification_queue"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    submission_type = Column(String(50), default="SYSTEM_INGEST")
    submitted_by = Column(String(100), default="SYSTEM")
    assigned_to_role = Column(String(50), default="ROL-003")  # Verification Officer
    current_status = Column(String(50), default="PENDING_REVIEW")  # PENDING_REVIEW, APPROVED, REJECTED
    reviewer_notes = Column(Text, nullable=True)
    decision = Column(String(50), nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EffectiveDateRecord(Base):
    __tablename__ = "effective_date_records"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    rule_number = Column(String(100), nullable=False)
    provision_title = Column(String(255), nullable=False)
    in_force_date = Column(String(50), nullable=False)
    sunset_date = Column(String(50), nullable=True)
    applicability_scope = Column(String(100), default="STATE_WIDE")
