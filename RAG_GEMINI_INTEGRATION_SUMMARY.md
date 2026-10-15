# TRUSTED RAG & GEMINI INTEGRATION ARCHITECTURE — NESFIC-D-36
**Project:** NESFIC-D-36 — Trusted Government Knowledge, Rules & Document Assistant  
**Challenge:** NESFIC 2026, Challenge Stream 1  
**Author:** Antigravity AI Pair Programmer & Domain Engineering Team  
**Date:** 2026-10-14  

---

## 1. Architectural Philosophy

Project NESFIC-D-36 operationalizes **Trust-Gated, Version-Aware, Provenance-First Government RAG**. In this architecture:

> **Google Gemini is the language-generation, reasoning, and drafting engine. It is NOT the authoritative source of government truth.**

Pretrained model knowledge is never permitted to fill gaps in statutory rules, dates, penalties, timelines, or official reference numbers. Every single factual statement presented to a government official or citizen must strictly originate from authenticated, active, and applicable statutory evidence.

---

## 2. End-to-End Pipeline Workflow

```mermaid
flowchart TD
    UQ[User Query (English / Assamese)] --> AUTH[1. Authentication & Role-Based Access Control]
    AUTH --> QC[2. Query Intent Classification & Taxonomy Match]
    QC --> THR[3. Trusted Hybrid Retrieval (BM25 + Dense Embeddings)]
    THR --> AF[4. Authority Filter (Zone 1 Primary Gazettes Only)]
    AF --> VF[5. Version & Temporal Filter (Active vs Superseded)]
    VF --> AC[6. Jurisdictional Applicability Check (State vs Union)]
    AC --> ESG{7. Evidence Sufficiency Gate}
    
    ESG -- Insufficient / Unverified / Conflict --> ABS[Tripartite Output: VERIFICATION_REQUIRED / CANNOT_GENERATE]
    ESG -- Sufficient & Verified --> LLM[8. Gemini 3.8 Reasoning & Drafting Engine]
    
    LLM --> CV[9. Atomic Claim Verification against Evidence Ledger]
    CV --> CIT[10. Exact Citation & Hash Verification]
    CIT --> FTG{11. Final Trust Gate Passed?}
    
    FTG -- Failed Check --> ABS
    FTG -- Verified Grounding --> OUT[Tripartite Output: VERIFIED with Full Provenance Trail]
```

---

## 3. The Tripartite Output Decision Model

To prevent hallucinations, the Gemini integration implements three deterministic final answer states:

### 1. `VERIFIED`
- **Condition:** Sufficient, authenticated, active, and applicable evidence completely supports every atomic claim in the response.
- **Output Requirements:**
  - Clear narrative answer in user's query language (English or Assamese).
  - Verbatim excerpt from governing statute / gazette.
  - Granular citation: Document Title, Act/Notification Number, Section/Rule, Page Number, and SHA-256 evidence hash.
  - Complete provenance trail tracing back to original source file.

### 2. `VERIFICATION_REQUIRED`
- **Condition:** Relevant evidence exists in the repository, but temporal applicability, subsequent amendments, or jurisdictional boundaries remain ambiguous (e.g., state vs central procurement thresholds).
- **Output Requirements:**
  - Provision of known verified facts with explicit caveats.
  - Highlighting of specific ambiguities or potential conflicts.
  - Automated trigger routing the case to a departmental Verification Officer.

### 3. `CANNOT_GENERATE`
- **Condition:** Required evidence is missing, unauthenticated, superseded, outside jurisdiction, or involves personal PII.
- **Output Requirements:**
  - Transparent declaration of inability to answer.
  - Detailed explanation of evidentiary gaps (e.g., "No 2026 Gazette notification published").
  - Absolute prohibition against guessing or model inference.

---

## 4. How the Master Workbook Fuels the System

| Master Sheet | Database / Pipeline Layer | Operational Role in RAG System |
| :--- | :--- | :--- |
| **`Source Register`** | PostgreSQL `sources` table | Enforces network-level allowlisting and official domain trust tiers. |
| **`Document Metadata`** | PostgreSQL `documents` table | Provides structured filters (department, jurisdiction, document type, dates). |
| **`Document Versions & Lifecycle`** | Temporal State Engine | Prevents citation of superseded laws; enforces active amendments. |
| **`Authenticity & Authority`** | Cryptographic Trust Gate | Rejects tampered files; tracks Gazette authentication imprints. |
| **`Structure & Page References`** | Search Indexing Engine | Maps chunk indices to physical printed page numbers and PDF offsets. |
| **`Cleaned Text & Semantic Chunks`** | Vector Database (Embeddings) | Provides high-coherence legal passages without mid-clause fragmentation. |
| **`Evidence & Claim Ledger`** | Grounding Verification Gate | Enables automated NLI evaluation of Gemini claims against verbatim evidence. |
| **`Relationships & Conflicts`** | Knowledge Graph (Neo4j / RDF) | Resolves complex statutory hierarchies (Acts -> Rules -> Citizen Charters). |
| **`RAG Retrieval Dataset`** | CI/CD Retrieval Evaluation | Evaluates Precision@k and Recall@k across English and Assamese queries. |
| **`AI Answer Evaluation Dataset`** | Automated LLM Eval Suite | Benchmarks Gemini answer faithfulness, citation accuracy, and abstention correctness. |
| **`Abstention & Verification`** | Safety & Guardrail Engine | Provides gold-standard negative test cases to ensure strict abstention compliance. |
| **`Roles & Permissions`** | API Gateway Access Control | Enforces departmental RBAC boundaries on queries and drafts. |
| **`Security & Red-Team`** | Adversarial Defense Shield | Protects pipeline against prompt injections, spoofed citations, and PII leakage. |

---

## 5. Summary of Achievements

The generated master Excel workbook `NESFIC_D36_Government_AI_Dataset_Master.xlsx` provides an enterprise-ready, auditable, and mathematically grounded foundation for Project NESFIC-D-36. By pairing deep OCR extraction with rigorous metadata normalization and cryptographic provenance, the dataset ensures that government officials receive trusted, verifiable, and authoritative assistance at every step.
