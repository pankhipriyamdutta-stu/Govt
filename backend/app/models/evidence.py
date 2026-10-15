from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class EvidenceClaimLedger(Base):
    __tablename__ = "evidence_claim_ledger"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String(50), unique=True, index=True, nullable=False)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    version_id = Column(String(50), nullable=True)
    page_id = Column(String(50), nullable=True)
    section_number = Column(String(100), nullable=True)
    paragraph_id = Column(String(50), nullable=True)
    exact_evidence_text = Column(Text, nullable=False)
    evidence_hash = Column(String(64), nullable=False)
    source_status = Column(String(100), default="UNVERIFIED_DOWNLOAD_SECTION")
    authority_status = Column(String(100), default="PRINTED_NAME_ONLY_UNAUTHENTICATED")
    version_status = Column(String(100), default="ACTIVE_PROVISIONAL")
    applicability_status = Column(String(100), default="APPLICABLE_ASSAM")
    claim_id = Column(String(50), index=True, nullable=True)
    claim_text = Column(Text, nullable=True)
    support_status = Column(String(100), default="SUPPORTED_TEXTUALLY")
    citation_status = Column(String(100), default="VALIDATED")
    reviewer_notes = Column(Text, nullable=True)

class RelationshipConflict(Base):
    __tablename__ = "relationship_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    relationship_id = Column(String(50), unique=True, index=True, nullable=False)
    primary_doc_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    related_doc_id = Column(String(50), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # MODIFIES_ACT, SUPERSEDES_ORDER, IMPLEMENTS_ACT, CONFLICTS_WITH
    hierarchy_level = Column(String(50), default="PRIMARY_STATUTE")
    effective_precedence = Column(String(50), default="PRIMARY_OVER_SUBORDINATE")
    conflict_description = Column(Text, nullable=True)
    conflict_severity = Column(String(50), default="NONE")  # LOW, MEDIUM, CRITICAL
    resolution_rule = Column(Text, nullable=True)
