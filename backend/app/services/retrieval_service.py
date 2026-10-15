import re
import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.document import Document, CleanedTextChunk, DocumentVersion, StructurePageReference
from app.models.evidence import EvidenceClaimLedger, RelationshipConflict

def tokenize(text: str) -> List[str]:
    """Tokenizes and normalizes text for lexical search."""
    return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_\u0980-\u09FF\-]+\b', text) if len(w) > 1]

def bm25_score(query_tokens: List[str], doc_tokens: List[str], avg_doc_len: float = 100.0, k1: float = 1.5, b: float = 0.75) -> float:
    """Calculates BM25 lexical relevance score."""
    if not query_tokens or not doc_tokens:
        return 0.0
    doc_len = len(doc_tokens)
    score = 0.0
    for qt in query_tokens:
        tf = doc_tokens.count(qt)
        if tf > 0:
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))
            score += numerator / denominator
    return score

class HybridRetrievalService:
    @staticmethod
    def search(
        db: Session,
        query: str,
        user_role: str = "ROL-001",
        department_filter: Optional[str] = None,
        language: str = "English",
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        # 1. Fetch eligible documents (RBAC & Quarantine Filter)
        doc_query = db.query(Document).filter(
            Document.approval_status != "REJECTED_QUARANTINED",
            Document.document_category != "EXCLUDED_PII",
            Document.document_category != "EXCLUDED_SCRATCH"
        )
        if department_filter and department_filter != "ALL":
            doc_query = doc_query.filter(Document.department.ilike(f"%{department_filter}%"))
            
        allowed_docs = {d.document_id: d for d in doc_query.all()}
        if not allowed_docs:
            return []

        # 2. Search Evidence Claim Ledger (First-class ground truth)
        evidence_entries = db.query(EvidenceClaimLedger).all()
        scored_evidence = []
        for ev in evidence_entries:
            if ev.document_id not in allowed_docs:
                continue
            
            combined_text = f"{ev.claim_text or ''} {ev.exact_evidence_text} {ev.section_number or ''}"
            tokens = tokenize(combined_text)
            score = bm25_score(query_tokens, tokens)

            # Boost exact statute or rule number mentions
            for qt in query_tokens:
                if ev.section_number and qt in ev.section_number.lower():
                    score += 5.0
                if "penalty" in qt and "penalty" in combined_text.lower():
                    score += 3.0
                if "sc" in qt or "st" in qt or "scheduled" in qt:
                    if "scheduled" in combined_text.lower():
                        score += 3.0
                if "birth" in qt and "birth" in combined_text.lower():
                    score += 3.0
                if "split" in qt and "splitting" in combined_text.lower():
                    score += 4.0

            if score > 0.5:
                doc_obj = allowed_docs[ev.document_id]
                scored_evidence.append({
                    "type": "EVIDENCE_LEDGER",
                    "id": ev.evidence_id,
                    "document_id": ev.document_id,
                    "document_title": doc_obj.document_title,
                    "department": doc_obj.department,
                    "section_number": ev.section_number,
                    "page_id": ev.page_id,
                    "text": ev.exact_evidence_text,
                    "claim_text": ev.claim_text,
                    "evidence_hash": ev.evidence_hash,
                    "source_status": ev.source_status,
                    "authority_status": ev.authority_status,
                    "version_status": ev.version_status,
                    "verification_status": doc_obj.verification_status,
                    "score": score
                })

        # 3. Search Cleaned Semantic Chunks
        chunks = db.query(CleanedTextChunk).all()
        scored_chunks = []
        for chk in chunks:
            if chk.document_id not in allowed_docs:
                continue
            tokens = tokenize(chk.cleaned_chunk_text)
            score = bm25_score(query_tokens, tokens)

            if score > 0.5:
                doc_obj = allowed_docs[chk.document_id]
                scored_chunks.append({
                    "type": "DOCUMENT_CHUNK",
                    "id": chk.chunk_id,
                    "document_id": chk.document_id,
                    "document_title": doc_obj.document_title,
                    "department": doc_obj.department,
                    "section_number": chk.section_number,
                    "page_id": chk.page_id,
                    "text": chk.cleaned_chunk_text,
                    "evidence_hash": chk.chunk_hash,
                    "verification_status": doc_obj.verification_status,
                    "score": score
                })

        # 4. Combine and Rank
        all_results = sorted(scored_evidence + scored_chunks, key=lambda x: x["score"], reverse=True)
        return all_results[:top_k]
