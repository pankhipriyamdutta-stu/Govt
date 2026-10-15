from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(50), unique=True, index=True, nullable=False)
    source_name = Column(String(255), nullable=False)
    authority_tier = Column(String(50), default="ZONE_1_PRIMARY_GAZETTE")
    department = Column(String(100), nullable=False)
    official_url = Column(String(500), nullable=True)
    verified_domain = Column(String(100), nullable=True)
    collection_method = Column(String(100), default="PORTAL_DOWNLOAD")

    documents = relationship("Document", back_populates="source")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), unique=True, index=True, nullable=False)
    source_id = Column(String(50), ForeignKey("sources.source_id"), nullable=True)
    original_filename = Column(String(255), nullable=False)
    document_title = Column(String(500), nullable=False)
    document_type = Column(String(50), nullable=False)  # ACT, STATUTORY_RULES, CITIZEN_CHARTER, etc.
    department = Column(String(100), nullable=False)
    issuing_authority = Column(String(255), nullable=False)
    reference_number = Column(String(255), nullable=True)
    publication_date = Column(String(50), nullable=True)
    issue_date = Column(String(50), nullable=True)
    effective_date = Column(String(50), nullable=True)
    expiry_date = Column(String(50), nullable=True)
    language = Column(String(50), default="English")
    jurisdiction = Column(String(100), default="Assam, India")
    document_category = Column(String(50), default="STATUTE")
    original_url = Column(String(500), nullable=True)
    original_file_hash = Column(String(64), nullable=False)  # SHA-256
    classification = Column(String(50), default="PUBLIC_STATUTE")
    extraction_status = Column(String(50), default="PARSED")
    verification_status = Column(String(50), default="PENDING_VERIFICATION")
    approval_status = Column(String(50), default="PENDING_APPROVAL")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    source = relationship("Source", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    files = relationship("DocumentFile", back_populates="document", cascade="all, delete-orphan")
    page_references = relationship("StructurePageReference", back_populates="document", cascade="all, delete-orphan")
    chunks = relationship("CleanedTextChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(String(50), unique=True, index=True, nullable=False)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    version_number = Column(String(20), default="v1.0")
    is_active_version = Column(Boolean, default=True)
    amendment_count = Column(Integer, default=0)
    superseded_by_version_id = Column(String(50), nullable=True)
    effective_from = Column(String(50), nullable=True)
    effective_to = Column(String(50), nullable=True)

    document = relationship("Document", back_populates="versions")

class DocumentFile(Base):
    __tablename__ = "document_files"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    version_id = Column(String(50), nullable=True)
    storage_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    mime_type = Column(String(100), default="application/pdf")
    sha256_hash = Column(String(64), nullable=False)
    is_quarantined = Column(Boolean, default=False)
    quarantine_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    document = relationship("Document", back_populates="files")

class StructurePageReference(Base):
    __tablename__ = "structure_page_references"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String(50), index=True, nullable=False)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    version_id = Column(String(50), nullable=True)
    printed_page_number = Column(String(20), nullable=True)
    physical_pdf_page = Column(Integer, nullable=True)
    section_title = Column(String(255), nullable=True)
    section_number = Column(String(100), nullable=True)
    content_type = Column(String(50), default="BODY_TEXT")

    document = relationship("Document", back_populates="page_references")

class CleanedTextChunk(Base):
    __tablename__ = "cleaned_text_chunks"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(50), unique=True, index=True, nullable=False)
    document_id = Column(String(50), ForeignKey("documents.document_id"), nullable=False)
    version_id = Column(String(50), nullable=True)
    page_id = Column(String(50), nullable=True)
    section_number = Column(String(100), nullable=True)
    cleaned_chunk_text = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    chunk_hash = Column(String(64), nullable=False)
    language = Column(String(50), default="English")

    document = relationship("Document", back_populates="chunks")
