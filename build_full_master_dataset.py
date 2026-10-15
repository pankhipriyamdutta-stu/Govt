"""
Main Master Dataset Orchestration Builder for NESFIC-D-36
Trusted Government Knowledge, Rules & Document Assistant
"""

import sys
import openpyxl
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Import sheet generators
from data_sheets_2_5 import create_sheet_2, create_sheet_3, create_sheet_4, create_sheet_5
from data_sheets_6_9 import create_sheet_6, create_sheet_7, create_sheet_8, create_sheet_9
from data_sheets_10_13 import create_sheet_10, create_sheet_11, create_sheet_12, create_sheet_13
from data_sheets_14_19 import create_sheet_14, create_sheet_15, create_sheet_16, create_sheet_17, create_sheet_18, create_sheet_19

# Import Sheet 1 builder from current file
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from dataset_styling import (
    NAVY_HEADER_FILL, HEADER_FONT, TITLE_FONT, SUBTITLE_FONT, SECTION_FONT,
    BODY_FONT, THIN_BORDER, ZEBRA_FILL, WHITE_FILL, style_table
)

def create_sheet_1(wb):
    ws = wb.create_sheet(title="README & Dataset Guide")
    ws.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws.cell(row=1, column=1, value="NESFIC-D-36: TRUSTED GOVERNMENT AI DATASET MASTER").font = TITLE_FONT
    ws.cell(row=2, column=1, value="Challenge: NESFIC 2026 (Challenge Stream 1) | Innovation: Trust-Gated, Version-Aware, Provenance-First Government RAG").font = SUBTITLE_FONT
    ws.cell(row=3, column=1, value="Prepared on: 2026-10-14 | Authority: Antigravity Government AI Pair Programmer & Domain Engineering Team").font = SUBTITLE_FONT
    
    # Section: Executive Summary
    ws.cell(row=5, column=1, value="1. EXECUTIVE SUMMARY & ARCHITECTURAL FOUNDATION").font = SECTION_FONT
    summary_text = (
        "This master workbook constitutes the gold-standard, auditable, and machine-readable government knowledge corpus "
        "engineered for Project NESFIC-D-36. The central architectural principle of this dataset is that Large Language Models "
        "(including Google Gemini) are language-generation, reasoning, and drafting engines—NOT authoritative repositories of government truth. "
        "All official knowledge must strictly originate from authenticated statutory evidence that has satisfied an immutable Trust Gate "
        "comprising SHA-256 integrity checks, Official Gazette publication verification, institutional authority validation, temporal "
        "applicability tracking, and claim-level provenance."
    )
    ws.cell(row=6, column=1, value=summary_text).font = BODY_FONT
    ws.cell(row=6, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells("A6:G6")
    ws.row_dimensions[6].height = 45
    
    # Section: Workbook Structure
    ws.cell(row=8, column=1, value="2. WORKBOOK ARCHITECTURE & SHEET DIRECTORY").font = SECTION_FONT
    
    headers = ["Sheet Number", "Sheet Name", "Primary Entity", "Key Identifier", "Core Purpose in RAG Pipeline"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=9, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[9].height = 25
    
    sheet_catalog = [
        ("Sheet 1", "README & Dataset Guide", "Dataset Governance", "N/A", "Master project documentation, operational guide, status definitions, and update protocols."),
        ("Sheet 2", "Source Register", "Government Authorities / Domains", "source_id", "Registry of authoritative issuing departments, gazettes, official domains, and trust tiers."),
        ("Sheet 3", "Document Metadata", "Government Documents", "document_id", "Formal legal metadata (Acts, Rules, Charters, Manuals, Notifications, Reference Numbers)."),
        ("Sheet 4", "Document Versions & Lifecycle", "Document Versions", "version_id", "Temporal validity, supersession, amendment lineages, and active lifecycle enforcement."),
        ("Sheet 5", "Authenticity & Authority", "Cryptographic / Gazette Audits", "verification_id", "SHA-256 hashes, digital signature audits, Gazette publisher seals, and institutional authority."),
        ("Sheet 6", "Structure & Page References", "Document Physical Layout", "page_id", "Printed vs PDF page indexing, section demarcations, annexures, tables, and blank-page detection."),
        ("Sheet 7", "Cleaned Text & Semantic Chunks", "Semantic Retrieval Units", "chunk_id", "Normalized, structurally coherent legal text chunks preserving statutory context and token counts."),
        ("Sheet 8", "Evidence & Claim Ledger", "Atomic Factual Assertions", "evidence_id", "Verbatim statutory citations mapped to atomic factual claims with cryptographic evidence hashes."),
        ("Sheet 9", "Relationships & Conflicts", "Relational Graph & Conflicts", "relationship_id", "Formal inter-document links (AMENDS, SUPERSEDES) and documented jurisdictional conflicts."),
        ("Sheet 10", "RAG Retrieval Dataset", "Retrieval Evaluation Benchmarks", "example_id", "Curated multilingual (English & Assamese) retrieval benchmark queries with gold-standard targets."),
        ("Sheet 11", "AI Answer Evaluation Dataset", "Generation Evaluation Benchmarks", "evaluation_id", "Comprehensive evaluation cases assessing answer groundedness, citations, and version accuracy."),
        ("Sheet 12", "Abstention & Verification", "Safety & Abstention Cases", "case_id", "Edge cases requiring AI abstention, conflict escalation, or mandatory officer review."),
        ("Sheet 13", "Query Intent & Taxonomy", "Task Taxonomy", "intent_id", "Classification of 10 primary government tasks (RULE_LOOKUP, DRAFT, TRANSLATE, COMPARE, etc.)."),
        ("Sheet 14", "Roles & Permissions", "Access Control (RBAC)", "role_id", "Synthetic role definitions and departmental access controls for government officials."),
        ("Sheet 15", "Security & Red-Team", "Adversarial Test Suites", "test_id", "Red-team test cases covering prompt injection, citation spoofing, and privilege escalation."),
        ("Sheet 16", "Data Quality & Correction", "ETL Quality Ledger", "quality_issue_id", "Audit log of raw anomalies detected (generic names, scanned pages, blank scans) and corrections."),
        ("Sheet 17", "Ingestion & Processing Log", "ETL Pipeline Execution", "job_id", "Machine ingestion status, OCR engine passes, hashing, and parsing status per input file."),
        ("Sheet 18", "Audit & Provenance", "System Audit Trail", "audit_id", "Tamper-evident production-grade audit log tracing all system operations and officer queries."),
        ("Sheet 19", "Summary & Quality Metrics", "Aggregated KPI Metrics", "metric_id", "Dynamically aggregated dataset counts, quality percentages, and operational readiness metrics.")
    ]
    
    for row_idx, r in enumerate(sheet_catalog, 10):
        for col_idx, val in enumerate(r, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = BODY_FONT
            cell.border = THIN_BORDER
            cell.fill = ZEBRA_FILL if row_idx % 2 == 0 else WHITE_FILL
            if col_idx in [1, 3, 4]:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top")
    
    start_r = 10 + len(sheet_catalog) + 2
    ws.cell(row=start_r, column=1, value="3. TRUST-GATE VERIFICATION LIFECYCLE & STATE MACHINE").font = SECTION_FONT
    lifecycle_desc = (
        "The RAG engine evaluates every document and answer through a 5-tier Trust Gate:\n"
        "1. File Integrity Tier: Validates immutable SHA-256 hash against original collection manifest.\n"
        "2. Gazette & Cryptographic Tier: Inspects digital signatures (PKCS#7) where available, or authenticates Official Gazette seals/imprints.\n"
        "3. Institutional Authority Tier: Verifies that the issuing officer (Governor, Secretary, Director) possesses statutory jurisdiction.\n"
        "4. Temporal & Version Tier: Assesses whether the provision is ACTIVE, AMENDED, or SUPERSEDED as of the query date.\n"
        "5. Evidence Sufficiency Gate: If evidence is complete, generates VERIFIED answer. If conflicting or unverified, routes to "
        "VERIFICATION_REQUIRED or CANNOT_GENERATE."
    )
    ws.cell(row=start_r + 1, column=1, value=lifecycle_desc).font = BODY_FONT
    ws.cell(row=start_r + 1, column=1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(f"A{start_r+1}:G{start_r+1}")
    ws.row_dimensions[start_r + 1].height = 90
    
    # Controlled Vocabularies
    vocab_r = start_r + 3
    ws.cell(row=vocab_r, column=1, value="4. CONTROLLED STATUS VOCABULARIES & DEFINITIONS").font = SECTION_FONT
    
    v_headers = ["Status Category", "Status Token", "Operational Definition", "RAG Pipeline Action"]
    for col_idx, h in enumerate(v_headers, 1):
        cell = ws.cell(row=vocab_r + 1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[vocab_r + 1].height = 24
    
    vocabs = [
        ("Answer State", "VERIFIED", "Sufficient authenticated, active, and applicable statutory evidence fully grounds the response.", "Output answer with exact section/page citations and provenance trail."),
        ("Answer State", "VERIFICATION_REQUIRED", "Relevant evidence exists, but version applicability, amendment status, or authority is ambiguous.", "Present provisional facts, highlight ambiguity, and trigger human officer review."),
        ("Answer State", "CANNOT_GENERATE", "Required evidence is missing, unauthenticated, superseded, or completely outside jurisdiction.", "Abstain explicitly; explain the evidentiary gap; do not guess or hallucinate."),
        ("Document Lifecycle", "ACTIVE", "Document is formally enacted/notified, currently in force, and not superseded.", "Eligible for standard retrieval and citation."),
        ("Document Lifecycle", "SUPERSEDED", "Document or specific section has been replaced by a subsequent statutory enactment.", "Excluded from active rule generation; retrieved only for historical/comparative queries."),
        ("Document Lifecycle", "PENDING_VERIFICATION", "Document ingested but cryptographic or Gazette authority checks are incomplete.", "Quarantined from authoritative generation until officer validation."),
        ("Evidence Support", "SUPPORTED", "Factual claim directly matches the verbatim text of the cited statutory provision.", "Grounding score 1.0; permitted in verified answer."),
        ("Evidence Support", "PARTIALLY_SUPPORTED", "Claim is inferred from statutory context but lacks explicit verbatim wording.", "Grounding score 0.5; requires hedging or verification notice."),
        ("Evidence Support", "CONTRADICTED", "Claim conflicts directly with an authoritative statutory clause or amendment.", "Strictly prohibited; triggers security/evaluation alert.")
    ]
    
    for row_idx, v in enumerate(vocabs, vocab_r + 2):
        for col_idx, val in enumerate(v, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = BODY_FONT
            cell.border = THIN_BORDER
            cell.fill = ZEBRA_FILL if row_idx % 2 == 0 else WHITE_FILL
            if col_idx in [1, 2]:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top")
                
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 32
    ws.column_dimensions["D"].width = 24
    ws.column_dimensions["E"].width = 50
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 20

def main():
    wb = openpyxl.Workbook()
    # Remove initial blank sheet
    initial_sheet = wb.active
    
    print("Building Sheet 1: README & Dataset Guide...")
    create_sheet_1(wb)
    
    print("Building Sheet 2: Source Register...")
    create_sheet_2(wb)
    
    print("Building Sheet 3: Document Metadata...")
    create_sheet_3(wb)
    
    print("Building Sheet 4: Document Versions & Lifecycle...")
    create_sheet_4(wb)
    
    print("Building Sheet 5: Authenticity & Authority...")
    create_sheet_5(wb)
    
    print("Building Sheet 6: Structure & Page References...")
    create_sheet_6(wb)
    
    print("Building Sheet 7: Cleaned Text & Semantic Chunks...")
    create_sheet_7(wb)
    
    print("Building Sheet 8: Evidence & Claim Ledger...")
    create_sheet_8(wb)
    
    print("Building Sheet 9: Relationships & Conflicts...")
    create_sheet_9(wb)
    
    print("Building Sheet 10: RAG Retrieval Dataset...")
    create_sheet_10(wb)
    
    print("Building Sheet 11: AI Answer Evaluation Dataset...")
    create_sheet_11(wb)
    
    print("Building Sheet 12: Abstention & Verification...")
    create_sheet_12(wb)
    
    print("Building Sheet 13: Query Intent & Taxonomy...")
    create_sheet_13(wb)
    
    print("Building Sheet 14: Roles & Permissions...")
    create_sheet_14(wb)
    
    print("Building Sheet 15: Security & Red-Team...")
    create_sheet_15(wb)
    
    print("Building Sheet 16: Data Quality & Correction...")
    create_sheet_16(wb)
    
    print("Building Sheet 17: Ingestion & Processing Log...")
    create_sheet_17(wb)
    
    print("Building Sheet 18: Audit & Provenance...")
    create_sheet_18(wb)
    
    print("Building Sheet 19: Summary & Quality Metrics...")
    create_sheet_19(wb)
    
    wb.remove(initial_sheet)
    
    out_file = Path("c:/Users/pankh/OneDrive/Desktop/Govt/NESFIC_D36_Government_AI_Dataset_Master.xlsx")
    wb.save(out_file)
    print(f"\n=======================================================")
    print(f"SUCCESS: Master workbook generated with 19 sheets!")
    print(f"File path: {out_file} (Size: {out_file.stat().st_size} bytes)")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
