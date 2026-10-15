import csv
import os
import hashlib
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.config import settings
from app.database import Base, engine
from app.models.user import Department, Role, User
from app.models.document import Source, Document, DocumentVersion, DocumentFile, StructurePageReference, CleanedTextChunk
from app.models.verification import SignatureVerificationRecord, VerificationQueue
from app.models.evidence import EvidenceClaimLedger, RelationshipConflict
from app.models.audit import QueryAuditLog, SecurityEvent, EvaluationCase
from app.services.auth_service import hash_password

def read_csv(filename: str):
    path = os.path.join(settings.DATASET_CSV_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f)
        return list(reader)

def seed_database(db: Session):
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)
    
    # Check if already seeded
    if db.query(Document).first() is not None:
        print("[SEED] Database already populated. Skipping duplicate seed.")
        return

    print("[SEED] Starting initial database seeding from master CSV sheets...")

    # 1. Departments
    dept_names = [
        ("DEPT-AASC", "Assam Administrative Staff College (AASC)", "Training & Capacity"),
        ("DEPT-STCCD", "Science, Technology & Climate Change Department (STCCD)", "State Technology"),
        ("DEPT-ASTEC", "Assam Science Technology and Environment Council (ASTEC)", "Scientific Council"),
        ("DEPT-FIN", "Finance Department (Procurement Division)", "State Finance"),
        ("DEPT-LEG", "Assam Legislative Department", "Legislative & Gazettes"),
        ("DEPT-ART", "Administrative Reforms and Training Department", "Public Services Nodal"),
        ("DEPT-GMC", "Guwahati Municipal Corporation", "Urban Local Body"),
        ("DEPT-DOPT", "Department of Personnel and Training (DoPT)", "Central Personnel"),
        ("DEPT-MOF", "Department of Expenditure (Public Procurement Division)", "Central Finance"),
        ("DEPT-CIC", "Central Information Commission", "Statutory Transparency"),
        ("DEPT-AUDIT", "Directorate of Audit & Vigilance", "Security & Compliance"),
        ("DEPT-PUB", "Public Portal Services", "Citizen Access Scope")
    ]
    dept_map = {}
    for code, name, desc in dept_names:
        dept = Department(code=code, name=name, state="Assam", description=desc)
        db.add(dept)
        db.flush()
        dept_map[code] = dept.id

    # 2. Roles from 14_Roles_and_Permissions.csv
    role_rows = read_csv("14_Roles_and_Permissions.csv")
    role_map = {}
    for r in role_rows:
        role = Role(
            role_id=r.get("role_id", ""),
            role_name=r.get("role_name", ""),
            department_scope=r.get("department_scope", "Department Specific"),
            permission_name=r.get("permission_name", ""),
            permitted_action=r.get("permitted_action", ""),
            restriction=r.get("restriction", ""),
            approval_required=r.get("approval_required", "NO").upper() == "YES",
            audit_required=r.get("audit_required", "YES").upper() == "YES"
        )
        db.add(role)
        db.flush()
        role_map[role.role_id] = role.id

    # 3. Default Demo Users
    demo_users = [
        ("officer_sharma", "officer.sharma@assam.gov.in", "Bikash Sharma, DPS", dept_map["DEPT-FIN"], role_map.get("ROL-002", 1)),
        ("reviewer_baruah", "reviewer.baruah@assam.gov.in", "Dr. Mridul Baruah, Verification Officer", dept_map["DEPT-LEG"], role_map.get("ROL-003", 1)),
        ("legal_gogoi", "legal.gogoi@assam.gov.in", "Ananya Gogoi, Legal Reviewer", dept_map["DEPT-LEG"], role_map.get("ROL-004", 1)),
        ("admin_kalita", "admin.kalita@assam.gov.in", "Pranjal Kalita, Dept Administrator", dept_map["DEPT-ART"], role_map.get("ROL-005", 1)),
        ("auditor_das", "auditor.das@assam.gov.in", "Himanta Das, System Security Auditor", dept_map["DEPT-AUDIT"], role_map.get("ROL-006", 1)),
        ("citizen_user", "citizen@assam.gov.in", "Gitanjali Saikia, Citizen", dept_map["DEPT-PUB"], role_map.get("ROL-001", 1))
    ]
    for username, email, full_name, dept_id, r_id in demo_users:
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hash_password("GovtSecure@2026"),
            department_id=dept_id,
            role_id=r_id,
            is_active=True,
            mfa_enabled=True
        )
        db.add(user)

    # 4. Sources from 02_Source_Register.csv
    source_rows = read_csv("02_Source_Register.csv")
    for s in source_rows:
        src = Source(
            source_id=s.get("source_id", ""),
            source_name=s.get("source_name", ""),
            authority_tier=s.get("trust_zone", "ZONE_1_OFFICIAL_PRIMARY"),
            department=s.get("department", "Government of Assam"),
            official_url=s.get("source_url", ""),
            verified_domain=s.get("official_domain", ""),
            collection_method=s.get("collection_method", "PORTAL_DOWNLOAD")
        )
        db.add(src)

    # 5. Documents from 03_Document_Metadata.csv
    doc_rows = read_csv("03_Document_Metadata.csv")
    for d in doc_rows:
        doc_id = d.get("document_id", "").strip()
        if not doc_id:
            continue
        is_quarantine = "REJECTED_QUARANTINED" in d.get("approval_status", "") or "EXCLUDED" in d.get("document_category", "")
        doc = Document(
            document_id=doc_id,
            source_id=d.get("source_id", ""),
            original_filename=d.get("original_filename", ""),
            document_title=d.get("document_title", ""),
            document_type=d.get("document_type", "ACT"),
            department=d.get("department", "Government of Assam"),
            issuing_authority=d.get("issuing_authority", "Governor of Assam"),
            reference_number=d.get("reference_number", ""),
            publication_date=d.get("publication_date", ""),
            issue_date=d.get("issue_date", ""),
            effective_date=d.get("effective_date", ""),
            expiry_date=d.get("expiry_date", ""),
            language=d.get("language", "English"),
            jurisdiction=d.get("jurisdiction", "Assam, India"),
            document_category=d.get("document_category", "STATUTE"),
            original_url=d.get("original_url", ""),
            original_file_hash=d.get("original_file_hash", ""),
            classification=d.get("classification", "PUBLIC_STATUTE"),
            extraction_status=d.get("extraction_status", "PARSED"),
            verification_status=d.get("verification_status", "PENDING_VERIFICATION"),
            approval_status=d.get("approval_status", "PENDING_APPROVAL"),
            notes=d.get("notes", "")
        )
        db.add(doc)
        
        # Link File
        doc_file = DocumentFile(
            document_id=doc_id,
            version_id=f"VER-{doc_id}-V1",
            storage_path=os.path.join(settings.SOURCE_DOCS_DIR, d.get("original_filename", "")),
            file_size_bytes=1024 * 150,
            mime_type="application/pdf" if d.get("original_filename", "").endswith(".pdf") else "application/octet-stream",
            sha256_hash=d.get("original_file_hash", ""),
            is_quarantined=is_quarantine,
            quarantine_reason=d.get("notes", "") if is_quarantine else None
        )
        db.add(doc_file)

    # 6. Document Versions from 04_Document_Versions_and_Lifecycle.csv
    ver_rows = read_csv("04_Document_Versions_and_Lifecycle.csv")
    for v in ver_rows:
        vid = v.get("version_id", "").strip()
        did = v.get("document_id", "").strip()
        if vid and did:
            ver = DocumentVersion(
                version_id=vid,
                document_id=did,
                version_number=v.get("version_number", "v1.0"),
                is_active_version=v.get("is_active", "TRUE").upper() == "TRUE",
                amendment_count=int(v.get("amendment_count", "0")) if v.get("amendment_count", "").isdigit() else 0,
                superseded_by_version_id=v.get("superseded_by", None),
                effective_from=v.get("effective_from", ""),
                effective_to=v.get("effective_to", "")
            )
            db.add(ver)

    # 7. Authenticity & Verification from 05_Authenticity_and_Authority.csv
    vfy_rows = read_csv("05_Authenticity_and_Authority.csv")
    for v in vfy_rows:
        did = v.get("document_id", "").strip()
        if not did:
            continue
        vrecord = SignatureVerificationRecord(
            document_id=did,
            has_digital_signature=v.get("signature_present", "") not in ("NO_CRYPTOGRAPHIC_SIG", "NOT_APPLICABLE", ""),
            signature_format=v.get("signature_present", "NONE"),
            certificate_subject=v.get("signer_identity_status", "PRINTED_NAME_ONLY"),
            certificate_issuer=v.get("certificate_chain_status", "MISSING_CERTIFICATE"),
            signature_valid=v.get("signature_validation_status", "") == "VALID",
            cert_chain_valid=v.get("certificate_chain_status", "") == "VALID",
            signing_time=v.get("verification_timestamp", ""),
            signer_authority_status=v.get("signer_authority_status", "UNVERIFIED_AUTHORITY"),
            anomaly_notes=v.get("evidence_of_verification", "")
        )
        db.add(vrecord)

        # Add to Verification Queue if review required
        if "PENDING" in v.get("approval_status", "") or "SUSPECT" in v.get("final_verification_status", ""):
            v_queue = VerificationQueue(
                document_id=did,
                submission_type="PORTAL_AUTO_INGEST",
                submitted_by="SYSTEM_CRON",
                assigned_to_role="ROL-003",
                current_status="PENDING_REVIEW",
                reviewer_notes=v.get("review_notes", "")
            )
            db.add(v_queue)

    # 8. Structure & Page References from 06_Structure_and_Page_References.csv
    page_rows = read_csv("06_Structure_and_Page_References.csv")
    for p in page_rows:
        pid = p.get("page_id", "").strip()
        did = p.get("document_id", "").strip()
        if pid and did:
            pref = StructurePageReference(
                page_id=pid,
                document_id=did,
                version_id=p.get("version_id", ""),
                printed_page_number=p.get("printed_page_number", ""),
                physical_pdf_page=int(p.get("physical_pdf_page", "1")) if p.get("physical_pdf_page", "").isdigit() else 1,
                section_title=p.get("section_title", ""),
                section_number=p.get("section_number", ""),
                content_type=p.get("content_type", "BODY_TEXT")
            )
            db.add(pref)

    # 9. Cleaned Text Chunks from 07_Cleaned_Text_and_Semantic_Chunks.csv
    chunk_rows = read_csv("07_Cleaned_Text_and_Semantic_Chunks.csv")
    for c in chunk_rows:
        cid = c.get("chunk_id", "").strip()
        did = c.get("document_id", "").strip()
        if cid and did:
            chk = CleanedTextChunk(
                chunk_id=cid,
                document_id=did,
                version_id=c.get("version_id", ""),
                page_id=c.get("page_id", ""),
                section_number=c.get("section_number", ""),
                cleaned_chunk_text=c.get("cleaned_chunk_text", ""),
                token_count=int(c.get("token_count", "0")) if c.get("token_count", "").isdigit() else 0,
                chunk_hash=c.get("chunk_hash", hashlib.sha256(c.get("cleaned_chunk_text", "").encode()).hexdigest()),
                language=c.get("language", "English")
            )
            db.add(chk)

    # 10. Evidence & Claim Ledger from 08_Evidence_and_Claim_Ledger.csv
    evd_rows = read_csv("08_Evidence_and_Claim_Ledger.csv")
    for e in evd_rows:
        eid = e.get("evidence_id", "").strip()
        did = e.get("document_id", "").strip()
        if eid and did:
            evd = EvidenceClaimLedger(
                evidence_id=eid,
                document_id=did,
                version_id=e.get("version_id", ""),
                page_id=e.get("page_id", ""),
                section_number=e.get("section_number", ""),
                paragraph_id=e.get("paragraph_id", ""),
                exact_evidence_text=e.get("exact_evidence_text", ""),
                evidence_hash=e.get("evidence_hash", hashlib.sha256(e.get("exact_evidence_text", "").encode()).hexdigest()),
                source_status=e.get("source_status", ""),
                authority_status=e.get("authority_status", ""),
                version_status=e.get("version_status", ""),
                applicability_status=e.get("applicability_status", ""),
                claim_id=e.get("claim_id", ""),
                claim_text=e.get("claim_text", ""),
                support_status=e.get("support_status", ""),
                citation_status=e.get("citation_status", ""),
                reviewer_notes=e.get("reviewer_notes", "")
            )
            db.add(evd)

    # 11. Relationships & Conflicts from 09_Relationships_and_Conflicts.csv
    rel_rows = read_csv("09_Relationships_and_Conflicts.csv")
    for r in rel_rows:
        rid = r.get("relationship_id", "").strip()
        pdoc = r.get("primary_doc_id", "").strip()
        if rid and pdoc:
            rel = RelationshipConflict(
                relationship_id=rid,
                primary_doc_id=pdoc,
                related_doc_id=r.get("related_doc_id", ""),
                relationship_type=r.get("relationship_type", ""),
                hierarchy_level=r.get("hierarchy_level", ""),
                effective_precedence=r.get("effective_precedence", ""),
                conflict_description=r.get("conflict_description", ""),
                conflict_severity=r.get("conflict_severity", "LOW"),
                resolution_rule=r.get("resolution_rule", "")
            )
            db.add(rel)

    # 12. Evaluation Cases from 11_AI_Answer_Evaluation_Dataset.csv
    eval_rows = read_csv("11_AI_Answer_Evaluation_Dataset.csv")
    for ev in eval_rows:
        e_id = ev.get("evaluation_id", "").strip()
        if e_id:
            eval_case = EvaluationCase(
                evaluation_id=e_id,
                query=ev.get("query", ""),
                query_language=ev.get("query_language", "English"),
                retrieved_documents=ev.get("retrieved_documents", ""),
                expected_answer=ev.get("expected_answer", ""),
                expected_claims=ev.get("expected_claims", ""),
                expected_citations=ev.get("expected_citations", ""),
                expected_status=ev.get("expected_status", "VERIFIED"),
                factual_support_score=float(ev.get("factual_support_score", "1.0")),
                citation_accuracy=float(ev.get("citation_accuracy", "1.0")),
                version_accuracy=float(ev.get("version_accuracy", "1.0")),
                authority_accuracy=float(ev.get("authority_accuracy", "1.0")),
                applicability_accuracy=float(ev.get("applicability_accuracy", "1.0")),
                abstention_correctness=float(ev.get("abstention_correctness", "1.0")),
                reviewer=ev.get("reviewer", "REV-EVAL-01"),
                evaluation_result=ev.get("evaluation_result", "PASS"),
                notes=ev.get("notes", "")
            )
            db.add(eval_case)

    # 13. Security Events from 15_Security_and_Red-Team.csv
    sec_rows = read_csv("15_Security_and_Red-Team.csv")
    for s in sec_rows:
        tid = s.get("test_id", "")
        if tid:
            sec_ev = SecurityEvent(
                event_type=s.get("attack_category", "ADVERSARIAL_TEST"),
                severity=s.get("severity", "HIGH"),
                source_ip="10.14.20.1",
                user_id="RED_TEAM_AUDITOR",
                details=f"{s.get('attack_description', '')} | Result: {s.get('evidence_of_test', '')}",
                payload_sample=s.get("test_input", ""),
                action_taken=s.get("expected_system_behavior", "BLOCKED_AND_LOGGED")
            )
            db.add(sec_ev)

    # 14. Initial Query Audit Log Chain with SHA-256 Tamper Evident Link
    prev_hash = "GENESIS_GOVT_BLOCK_000000000000000000000000000000000000000000000000"
    init_logs = [
        ("officer_sharma", "DEPT-FIN", "What is the timeline for issuing a birth certificate under GMC charter?", "English", "VERIFICATION_REQUIRED", 1, 1, 120),
        ("citizen_user", "DEPT-PUB", "Do SC and ST applicants have to pay examination fees for Assam govt posts?", "English", "VERIFIED", 1, 1, 95),
        ("officer_sharma", "DEPT-FIN", "Can an Assam government department split procurement orders to bypass approval?", "English", "VERIFIED", 1, 1, 110),
        ("reviewer_baruah", "DEPT-LEG", "What is the IAS Cadre strength for Assam under the 2026 notification?", "English", "CANNOT_GENERATE", 0, 0, 45),
    ]
    for uid, did, qtext, qlang, rstatus, clm_cnt, cit_cnt, lat in init_logs:
        log_payload = f"{uid}|{did}|{qtext}|{rstatus}|{clm_cnt}|{cit_cnt}|{prev_hash}"
        cur_hash = hashlib.sha256(log_payload.encode()).hexdigest()
        audit_entry = QueryAuditLog(
            user_id=uid,
            department_id=did,
            query_text=qtext,
            query_language=qlang,
            response_status=rstatus,
            model_used="gemini-2.5-flash",
            claims_count=clm_cnt,
            citations_count=cit_cnt,
            latency_ms=lat,
            previous_hash=prev_hash,
            tamper_hash=cur_hash
        )
        db.add(audit_entry)
        prev_hash = cur_hash

    db.commit()
    print("[SEED] Successfully seeded complete relational dataset from master sheets!")
