from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from app.database import Base

class QueryAuditLog(Base):
    __tablename__ = "query_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="ANONYMOUS")
    department_id = Column(String(100), default="PUBLIC")
    query_text = Column(Text, nullable=False)
    query_language = Column(String(20), default="English")
    response_status = Column(String(50), nullable=False)  # VERIFIED, VERIFICATION_REQUIRED, CANNOT_GENERATE
    model_used = Column(String(100), default="gemini-2.5-flash")
    claims_count = Column(Integer, default=0)
    citations_count = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    previous_hash = Column(String(64), nullable=True)
    tamper_hash = Column(String(64), nullable=False)  # SHA-256 of log record + previous_hash

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False)  # PROMPT_INJECTION, PII_ATTEMPT, QUARANTINE_VIOLATION, UNAUTHORIZED_ACCESS
    severity = Column(String(50), default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    source_ip = Column(String(50), default="127.0.0.1")
    user_id = Column(String(100), default="SYSTEM")
    details = Column(Text, nullable=False)
    payload_sample = Column(Text, nullable=True)
    action_taken = Column(String(100), default="BLOCKED_AND_LOGGED")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EvaluationCase(Base):
    __tablename__ = "evaluation_cases"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String(50), unique=True, index=True, nullable=False)
    query = Column(Text, nullable=False)
    query_language = Column(String(20), default="English")
    retrieved_documents = Column(String(255), nullable=True)
    expected_answer = Column(Text, nullable=False)
    expected_claims = Column(String(255), nullable=True)
    expected_citations = Column(Text, nullable=True)
    expected_status = Column(String(50), nullable=False)
    factual_support_score = Column(Float, default=1.0)
    citation_accuracy = Column(Float, default=1.0)
    version_accuracy = Column(Float, default=1.0)
    authority_accuracy = Column(Float, default=1.0)
    applicability_accuracy = Column(Float, default=1.0)
    abstention_correctness = Column(Float, default=1.0)
    reviewer = Column(String(100), default="REV-EVAL-01")
    evaluation_result = Column(String(50), default="PASS")
    notes = Column(Text, nullable=True)
