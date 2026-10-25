from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from app.database import Base

class VeritraceDocument(Base):
    __tablename__ = "veritrace_documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(64), unique=True, index=True, nullable=False)
    original_filename = Column(String(255), nullable=False)
    storage_path = Column(String(512), nullable=False)
    file_type = Column(String(64), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    sha256_hash = Column(String(64), index=True, nullable=False)
    sha512_hash = Column(String(128), nullable=True)
    uploaded_by = Column(String(128), default="authorized_officer")
    upload_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Malware scanning status
    malware_scan_status = Column(String(32), default="NOT_PERFORMED")
    malware_scan_details = Column(Text, default="Malware scanning not performed (no external scanner configured)")

    # Processing and analysis state
    extraction_status = Column(String(32), default="PENDING")
    analysis_status = Column(String(32), default="PENDING")

    # Overall risk aggregation
    overall_risk_score = Column(Float, default=0.0)
    overall_risk_verdict = Column(String(32), default="INSUFFICIENT_DATA")
    risk_summary = Column(Text, nullable=True)

    # Document properties
    page_count = Column(Integer, default=0)
    ocr_used = Column(Boolean, default=False)
    text_extraction_method = Column(String(64), default="pdf_text_extraction")
    extracted_text = Column(Text, nullable=True)
    extracted_entities = Column(JSON, default=list)

    # Forensic indicators
    has_digital_signature = Column(Boolean, default=False)
    signature_valid = Column(Boolean, default=False)
    signature_details = Column(JSON, default=dict)
    reference_hash_status = Column(String(64), default="NO_TRUSTED_REFERENCE")
    trusted_reference_source = Column(String(255), nullable=True)

    # Structural & Visual analysis
    structural_indicators = Column(JSON, default=dict)
    visual_tampering_score = Column(Float, nullable=True)
    visual_tampering_verdict = Column(String(64), default="NOT_EVALUATED")
    visual_findings = Column(JSON, default=list)

    # Machine Learning risk assessment
    ml_fraud_score = Column(Float, nullable=True)
    ml_anomaly_verdict = Column(String(64), default="MODEL_BASELINE_NOT_EVALUATED")
    ml_features = Column(JSON, default=dict)

    # Fact & Provenance high-level metrics
    claims_count = Column(Integer, default=0)
    claims_verified_count = Column(Integer, default=0)
    provenance_node_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class ForensicFinding(Base):
    __tablename__ = "veritrace_forensic_findings"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(String(64), unique=True, index=True, nullable=False)
    document_id = Column(String(64), index=True, nullable=False)
    category = Column(String(64), nullable=False)  # file_integrity, digital_signature, visual_manipulation, document_structure, ml_fraud_risk, factual_accuracy, source_provenance
    status = Column(String(64), nullable=False)    # VERIFIED_AUTHENTIC, SUSPICIOUS_INDICATOR, DEFINITIVE_ALTERATION, UNVERIFIED, INFO
    severity = Column(String(32), default="medium") # low, medium, high, critical, informational
    description = Column(Text, nullable=False)
    evidence = Column(JSON, default=list)
    limitations = Column(JSON, default=list)
    model_version = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ExtractedClaim(Base):
    __tablename__ = "veritrace_extracted_claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String(64), unique=True, index=True, nullable=False)
    document_id = Column(String(64), index=True, nullable=False)
    claim_text = Column(Text, nullable=False)
    subject = Column(String(255), nullable=True)
    predicate = Column(String(255), nullable=True)
    object = Column(String(255), nullable=True)
    verification_status = Column(String(64), default="NOT_CHECKED")  # SUPPORTED, CONTRADICTED, INSUFFICIENT_EVIDENCE, CONFLICTING_SOURCES, NOT_CHECKED
    confidence_score = Column(Float, default=0.0)
    reasoning = Column(Text, nullable=True)
    limitations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ClaimEvidence(Base):
    __tablename__ = "veritrace_claim_evidence"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String(64), unique=True, index=True, nullable=False)
    claim_id = Column(String(64), index=True, nullable=False)
    document_id = Column(String(64), index=True, nullable=False)
    source_title = Column(String(255), nullable=False)
    source_url = Column(String(512), nullable=False)
    source_authority = Column(String(255), nullable=True)
    publication_date = Column(String(64), nullable=True)
    retrieval_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    passage_text = Column(Text, nullable=False)
    alignment_label = Column(String(64), default="NEUTRAL")  # SUPPORTS, CONTRADICTS, NEUTRAL
    similarity_score = Column(Float, default=0.0)


class ProvenanceNode(Base):
    __tablename__ = "veritrace_provenance_nodes"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(64), index=True, nullable=False)
    node_id = Column(String(64), nullable=False)
    node_type = Column(String(64), nullable=False)  # DOCUMENT, SOURCE, ISSUER, CLAIM, COPIED_INSTANCE
    label = Column(String(255), nullable=False)
    metadata_json = Column(JSON, default=dict)


class ProvenanceEdge(Base):
    __tablename__ = "veritrace_provenance_edges"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(64), index=True, nullable=False)
    source_node = Column(String(64), nullable=False)
    target_node = Column(String(64), nullable=False)
    relation_type = Column(String(64), nullable=False)  # CITES, COPIED_FROM, SIMILAR_TO, PUBLISHED_AT, SUPPORTS, CONTRADICTS
    confidence = Column(Float, default=1.0)
    evidence_basis = Column(Text, nullable=True)
