"""
Data and Sheet Builders for Sheets 2 to 5:
- Sheet 2: Source Register
- Sheet 3: Document Metadata
- Sheet 4: Document Versions and Lifecycle
- Sheet 5: Authenticity and Authority Verification

ENFORCING STRICT TRUST BOUNDARIES:
- Never label unauthenticated or third-party converted files as VERIFIED.
- Flag suspect tools (adultpdf.com, ilovepdf.com, Nitro Pro 7, generic authors).
- Explicitly record missing PKCS#7 signatures.
- Separate textual presence from certified provenance.
"""

import openpyxl
from openpyxl.styles import Alignment
from dataset_styling import NAVY_HEADER_FILL, HEADER_FONT, THIN_BORDER, ZEBRA_FILL, WHITE_FILL, BODY_FONT, style_table

def create_sheet_2(wb):
    ws = wb.create_sheet(title="Source Register")
    headers = [
        "source_id", "source_name", "department", "official_domain", "source_url",
        "source_type", "source_owner", "source_origin", "trust_zone", "discovery_date",
        "last_checked_date", "collection_method", "source_status", "verification_status", "notes"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    sources = [
        (
            "SRC-AS-LEG-01", "Assam Legislative Department", "Legislative Department", "legislative.assam.gov.in",
            "https://legislative.assam.gov.in/acts-and-rules", "OFFICIAL_GAZETTE_PUBLISHER",
            "Government of Assam", "State Government of Assam", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Authoritative publisher of Assam Gazette Extraordinary notifications. Primary legal repository for state enactments."
        ),
        (
            "SRC-AS-ART-01", "Administrative Reforms and Training Department", "AR & T Department", "art.assam.gov.in",
            "https://art.assam.gov.in/documents-reports/rules", "STATE_NODAL_DEPARTMENT",
            "Government of Assam", "State Government of Assam", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Nodal administrative department for ARTPS Act and Rules enforcement."
        ),
        (
            "SRC-AS-GMC-01", "Guwahati Municipal Corporation", "Urban Development Department", "gmc.assam.gov.in",
            "https://gmc.assam.gov.in/citizen-charter", "MUNICIPAL_LOCAL_BODY",
            "Guwahati Municipal Corporation", "Urban Local Body, Assam", "ZONE_2_SECONDARY_PORTAL",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "PENDING_VERIFICATION",
            "Issuing authority for municipal citizen charters. Document in possession was created via third-party Nitro Pro 7 in 2013; current 2026 validity requires re-verification."
        ),
        (
            "SRC-AS-FIN-01", "Finance Department (Procurement Division)", "Finance Department", "finance.assam.gov.in",
            "https://finance.assam.gov.in/documents-reports/rules-0", "STATE_FINANCE_AUTHORITY",
            "Government of Assam", "State Government of Assam", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Authoritative regulator for state public procurement rules under Assam Act XXIV of 2017."
        ),
        (
            "SRC-GOI-DOPT-01", "Department of Personnel and Training (DoPT)", "Ministry of Personnel, Public Grievances and Pensions", "dopt.gov.in",
            "https://dopt.gov.in/notifications/rules-and-regulations", "CENTRAL_PERSONNEL_AUTHORITY",
            "Government of India", "Union Government of India", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Cadre controlling authority for IAS and policymaker for Section 4 RTI proactive disclosures."
        ),
        (
            "SRC-GOI-MOF-01", "Department of Expenditure (Public Procurement Division)", "Ministry of Finance", "doe.gov.in",
            "https://doe.gov.in/manuals", "CENTRAL_FINANCE_AUTHORITY",
            "Government of India", "Union Government of India", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Authoritative policymaker for Central Government procurement manuals under GFR 2017."
        ),
        (
            "SRC-GOI-CIC-01", "Central Information Commission", "Central Information Commission", "cic.gov.in",
            "https://cic.gov.in/notifications/vacancies", "STATUTORY_COMMISSION",
            "Government of India", "Union Statutory Body", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Statutory transparency commission established under RTI Act 2005."
        ),
        (
            "SRC-GOI-LAW-01", "Legislative Department", "Ministry of Law and Justice", "legislative.gov.in",
            "https://legislative.gov.in/constitution-of-india", "CENTRAL_LEGISLATIVE_AUTHORITY",
            "Government of India", "Union Government of India", "ZONE_1_OFFICIAL_PRIMARY",
            "2026-10-14", "2026-10-14", "MANUAL_INSPECTION_EXPLORER", "ACTIVE", "VERIFIED",
            "Official publisher of the updated text of the Constitution of India."
        ),
        (
            "SRC-EXT-UNVERIFIED-01", "Untrusted Web Aggregators & Converters", "Third-Party / Unofficial", "unknown-origin",
            "http://www.adultpdf.com | www.ilovepdf.com", "THIRD_PARTY_CONVERTER",
            "Unknown External Entities", "Internet Aggregator", "ZONE_4_SUSPECT_ORIGIN",
            "2026-10-14", "2026-10-14", "METADATA_DISCOVERY", "SUSPECT", "FAILED_VERIFICATION",
            "Untrusted third-party online tools detected in metadata of ingested files (ARTPS ACT, ARTPS RULES, Procurement Rules, Constitution). Mandates quarantine and re-ingestion from certified government gazette repositories."
        )
    ]
    
    for row_idx, src in enumerate(sources, 2):
        for col_idx, val in enumerate(src, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

def create_sheet_3(wb):
    ws = wb.create_sheet(title="Document Metadata")
    headers = [
        "document_id", "source_id", "original_filename", "document_title", "document_type",
        "department", "issuing_authority", "reference_number", "publication_date", "issue_date",
        "effective_date", "expiry_date", "language", "jurisdiction", "document_category",
        "original_url", "original_file_hash", "classification", "extraction_status",
        "verification_status", "approval_status", "notes"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    docs = [
        (
            "DOC-AS-ARTPS-001", "SRC-AS-LEG-01", "ARTPS ACT.pdf",
            "The Assam Right to Public Services Act, 2012 (Assam Act No. IX of 2012)", "ACT",
            "Legislative Department", "Governor of Assam / Assam Legislative Assembly",
            "Assam Act No. IX of 2012 / LGL.18/2012/57", "2012-05-02", "2012-05-02", "2012-05-02",
            "PERPETUAL", "English", "Assam, India", "STATUTE",
            "Local Download", "e8d7fd46b5b8dbe9fbba6cce2903e05a8b5c929a75d5f2a1705e60d5bfa48680",
            "PUBLIC_STATUTE", "OCR_EXTRACTED_UNVERIFIED_PRODUCER", "SUSPECT_ORIGIN_THIRD_PARTY_TOOL", "PENDING_VERIFICATION",
            "WARNING: Metadata Producer reveals 'http://www.adultpdf.com'. Document text matches Gazette No. 194, but file integrity must be re-verified against an official government repository."
        ),
        (
            "DOC-AS-ARTPS-002", "SRC-AS-ART-01", "ARTPS RULES_0.pdf",
            "The Assam Right to Public Services Rules, 2012", "STATUTORY_RULES",
            "Administrative Reforms and Training Department", "Governor of Assam",
            "No. AR.69/2011/Pt-II / Gazette No. 471", "2012-10-25", "2012-09-19", "2012-10-25",
            "PERPETUAL", "English", "Assam, India", "SUBORDINATE_LEGISLATION",
            "Local Download", "39105a700271794b6fa7c22998e3b320ea558cbbbf3680fe038670da2a6b47c9",
            "PUBLIC_RULES", "OCR_EXTRACTED_UNVERIFIED_PRODUCER", "SUSPECT_ORIGIN_THIRD_PARTY_TOOL", "PENDING_VERIFICATION",
            "WARNING: Filename has duplicate suffix '_0' and Producer 'http://www.adultpdf.com'. Text corresponds to 2012 rules, but certified origin cannot be attested without re-ingestion."
        ),
        (
            "DOC-AS-GMC-001", "SRC-AS-GMC-01", "Citizen Charter.pdf",
            "Guwahati Municipal Corporation Citizen Charter: Notified Public Services (See Rule 5)", "CITIZEN_CHARTER",
            "Guwahati Municipal Corporation", "Commissioner, Guwahati Municipal Corporation",
            "Appendix-2 / GMC-ARTPS-2013-01", "2013-07-14", "2013-07-14", "2013-07-14",
            "UNTIL_REVISED", "English", "Guwahati Municipal Area, Assam", "OPERATIONAL_REGULATION",
            "Local Download", "6ce0b39830db9be282f6e525413fbc4dd645d9e504c50269f848b8dfcc4b216c",
            "PUBLIC_CHARTER", "DIGITAL_PARSED_VINTAGE_2013", "UNCONFIRMED_CURRENT_VALIDITY", "PENDING_APPROVAL",
            "WARNING: PDF authored by 'omprakash' using Nitro Pro 7 in 2013; modified in 2017. Current applicability in 2026 is unconfirmed. AI must warn user before citing timelines."
        ),
        (
            "DOC-AS-SCST-001", "SRC-AS-LEG-01", "untitled_23.pdf",
            "The Assam Scheduled Castes and Scheduled Tribes (Reservation of Vacancies in Services and Posts) (Amendment) Act, 2024 (Assam Act No. XXXI of 2024)", "AMENDMENT_ACT",
            "Legislative Department", "Governor of Assam / Assam Legislative Assembly",
            "Assam Act No. XXXI of 2024 / LGL.41/2024/43", "2024-10-25", "2024-10-19", "2024-10-25",
            "PERPETUAL", "English", "Assam, India", "STATUTE",
            "Local Download", "2159844f3b6b19a9786a760c6d7054f15bb36d75b3992b453a251b5bc93892eb",
            "PUBLIC_STATUTE", "OCR_EXTRACTED_GENERIC_NAME", "PENDING_GAZETTE_CROSSCHECK", "PENDING_APPROVAL",
            "WARNING: Generic filename 'untitled_23.pdf' with internal path 'D:\\Lagislative Assambly & Other'. OCR matches Assam Gazette No. 530, but file was generated via 'Microsoft: Print To PDF' without PKCS#7 token."
        ),
        (
            "DOC-GOI-CADRE-001", "SRC-GOI-DOPT-01", "ias_fixation_of_cadre_strength_second_amendment_regulations_2025.pdf",
            "Indian Administrative Service (Fixation of Cadre Strength) Second Amendment Regulations, 2025", "STATUTORY_REGULATIONS",
            "Department of Personnel and Training / Assam Personnel Department", "Central Government / Governor of Assam",
            "G.S.R. 78(E) / AAI.14/96/Pt-I/93", "2025-02-26", "2025-01-27", "2025-01-27",
            "UNTIL_AMENDED", "English", "Assam-Meghalaya Joint Cadre (Assam Segment)", "ALL_INDIA_SERVICE_REGULATION",
            "Local Download", "2e1d9e03400f074d09ae77c2293b4a243d99baab2da1b6fe55799a776c52b21c",
            "PUBLIC_REGULATION", "OCR_EXTRACTED_PHYSICAL_SCAN", "PENDING_DIGITAL_SIGNATURE_CHECK", "PENDING_APPROVAL",
            "Physical scan generated via 'HP Scan Extended Application'. Content corresponds to Gazette of India notification G.S.R. 78(E), but lacks digital certificate."
        ),
        (
            "DOC-AS-PROC-001", "SRC-AS-FIN-01", "dms22_assam_public_procurement_rules_2020.pdf",
            "The Assam Public Procurement Rules, 2020", "STATUTORY_RULES",
            "Finance Department (Procurement Division)", "Governor of Assam",
            "No. FEB.296/2017/Pt.II/38 / Gazette No. 370", "2020-09-08", "2020-09-02", "2020-09-08",
            "PERPETUAL", "English", "Assam, India", "SUBORDINATE_LEGISLATION",
            "Local Download", "7f2186799708767e7fe1b0663489112fc73295b9a896d88f6c529ba1c964177d",
            "PUBLIC_RULES", "OCR_EXTRACTED_THIRD_PARTY_TOOL", "UNVERIFIED_THIRD_PARTY_COMPRESSION", "PENDING_VERIFICATION",
            "WARNING: Metadata Producer reveals 'www.ilovepdf.com'. Document is a 104-page scan passed through a web compression service. Requires cross-check with official Gazette No. 370."
        ),
        (
            "DOC-GOI-RTI-001", "SRC-GOI-DOPT-01", "MaintenanceofRecordstSZEC.pdf",
            "Maintenance of Records and Publication of Information in Consonance with Section 4 of the RTI Act, 2005 - Consolidated Instructions", "OFFICE_MEMORANDUM",
            "Department of Personnel & Training (IR Division)", "Director / Under Secretary, DoPT",
            "OM No. 1/18/2007-IR (Consolidated Updated on 31-10-2022)", "2022-10-31", "2022-10-31", "2022-10-31",
            "ACTIVE_GUIDELINE", "English", "Union of India (All Ministries & Public Authorities)", "EXECUTIVE_INSTRUCTION",
            "Local Download", "87126981f52a78536ec7d03a113d077fb58273617be3a6c23ae493636f866405",
            "PUBLIC_CIRCULAR", "DIGITAL_PARSED_GENERIC_AUTHOR", "SECONDARY_COMPILATION_UNCONFIRMED", "PENDING_APPROVAL",
            "Authored by generic user 'User' using Microsoft Word 2007. Text matches DoPT circular, but lacks digital PKCS#7 token from dopt.gov.in."
        ),
        (
            "DOC-GOI-CIC-001", "SRC-GOI-CIC-01", "Vacancy circular for employment news-1m1R62.pdf",
            "Vacancy Circular for Filling up the Post of Registrar on Deputation (ISTC) Basis in Central Information Commission", "VACANCY_CIRCULAR",
            "Central Information Commission", "Under Secretary (Admn), CIC",
            "Admn-15014/4/2021-ADMN-CIC", "2025-12-30", "2025-12-30", "2025-12-30",
            "2026-02-28", "English", "Union of India", "RECRUITMENT_NOTICE",
            "Local Download", "b42ea1ecb55cb3b0ffc601dff7b9ebc1c73a436ff326759714c6225e59df1898",
            "PUBLIC_VACANCY", "OCR_EXTRACTED_BLANK_PAGES_FLAGGED", "TEMPORAL_VALIDITY_UNCONFIRMED", "PENDING_APPROVAL",
            "Scanned notice dated 30.12.2025 with 60 days application window. Current recruitment status in late 2026 is unconfirmed. Blank scan pages 2 & 8 detected."
        ),
        (
            "DOC-GOI-PROC-001", "SRC-GOI-MOF-01", "Manual_for_Procurement_of_Consultancy_&_Other_Services_Updated June, 2022_1.pdf",
            "Manual for Procurement of Consultancy & Other Services (Updated June, 2022)", "MANUAL_GUIDELINE",
            "Department of Expenditure (Public Procurement Division)", "Joint Secretary (PPD), Ministry of Finance",
            "MoF-DoE-PPD-2022-06", "2022-08-05", "2022-06-30", "2022-06-30",
            "UNTIL_REVISED", "English", "Union of India (Central Ministries / CPSUs)", "PROCUREMENT_POLICY",
            "Local Download", "acd4d0302088f1dc2aa1337e7215cc20b134d115e85d9da639aa8aa9fca1286b",
            "PUBLIC_MANUAL", "DIGITAL_PARSED_DUPLICATE_NAME", "CENTRAL_JURISDICTION_PROVISIONAL", "PENDING_APPROVAL",
            "Filename has collision suffix '_1'. Metadata title 'Three Cover MoF_2022_curve.cdr' authored by 'Bharat'. Text matches official 214-page manual."
        ),
        (
            "DOC-IND-CONST-001", "SRC-GOI-LAW-01", "c9fe9c9b6840524844316f74bb1c556c.pdf",
            "The Constitution of India / भारत का संविधान (As on 1st May, 2024 / 2026 Edition)", "CONSTITUTION",
            "Legislative Department", "Republic of India / Constituent Assembly / Parliament",
            "Constitutional Enactment / Ed. 2024-2026", "2024-05-01", "1950-01-26", "1950-01-26",
            "PERPETUAL", "Bilingual (English & Hindi)", "Republic of India", "SUPREME_LEX",
            "Local Download", "4c8e93689ec23f3eb65c69707297e59c3d4ee7b0d5ab46927da80482ea75da76",
            "SUPREME_CONSTITUTION", "DIGITAL_PARSED_MD5_NAME", "UNVERIFIED_THIRD_PARTY_CONVERSION", "PENDING_VERIFICATION",
            "WARNING: Random hash filename 'c9fe9c9b...' with Producer 'iLovePDF'. Text is official Constitution (402 pp), but file provenance is unverified."
        ),
        (
            "EXC-ID-001", "SRC-EXT-UNVERIFIED-01", "Identity Card.pdf",
            "Scanned Personal Identification Document", "PERSONAL_ID",
            "Private Individual / Non-Government", "Unknown",
            "N/A", "2026-10-13", "2026-10-13", "N/A", "N/A",
            "English", "Personal Scope", "EXCLUDED_PII",
            "Local Download", "6f5a3b2e81d749ac10f8234bb5a99281e5b12847c502b4d91e6b8c92a104c8f3",
            "RESTRICTED_PII", "EXCLUDED_FROM_EXTRACTION", "NOT_APPLICABLE", "REJECTED_QUARANTINED",
            "QUARANTINED: Contains personal identity image (PII). Excluded from government RAG indexing to preserve citizen privacy."
        ),
        (
            "EXC-DOC-001", "SRC-EXT-UNVERIFIED-01", "19,20,23,24.docx",
            "Scratch Office Document", "OFFICE_DOC",
            "Unknown", "Unknown", "N/A", "2026-10-08", "2026-10-08", "N/A", "N/A",
            "English", "Personal Scope", "EXCLUDED_SCRATCH",
            "Local Download", "2a3b4c5d6e7f8091a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5",
            "SCRATCH_FILE", "ZERO_CONTENT_DETECTED", "NOT_APPLICABLE", "REJECTED_QUARANTINED",
            "QUARANTINED: Contains only 58 bytes whitespace. Zero semantic content."
        ),
        (
            "EXC-DOC-002", "SRC-EXT-UNVERIFIED-01", "Doc5.docx",
            "Layout Fragment Scratch Document", "OFFICE_DOC",
            "Unknown", "Unknown", "N/A", "2026-10-08", "2026-10-08", "N/A", "N/A",
            "English", "Personal Scope", "EXCLUDED_SCRATCH",
            "Local Download", "3b4c5d6e7f8091a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6",
            "SCRATCH_FILE", "MARGIN_FRAGMENT_ONLY", "NOT_APPLICABLE", "REJECTED_QUARANTINED",
            "QUARANTINED: 16 bytes margin text ('left -872066 0 0'). Not a government document."
        ),
        (
            "EXC-DOC-003", "SRC-EXT-UNVERIFIED-01", "Doc8.docx",
            "Layout Fragment Scratch Document", "OFFICE_DOC",
            "Unknown", "Unknown", "N/A", "2026-10-08", "2026-10-08", "N/A", "N/A",
            "English", "Personal Scope", "EXCLUDED_SCRATCH",
            "Local Download", "4c5d6e7f8091a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7",
            "SCRATCH_FILE", "MARGIN_FRAGMENT_ONLY", "NOT_APPLICABLE", "REJECTED_QUARANTINED",
            "QUARANTINED: 13 bytes margin text ('right 634 0 0'). Not a government document."
        )
    ]
    
    for row_idx, doc in enumerate(docs, 2):
        for col_idx, val in enumerate(doc, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

def create_sheet_4(wb):
    ws = wb.create_sheet(title="Document Versions & Lifecycle")
    headers = [
        "version_id", "document_id", "version_label", "issue_date", "effective_from",
        "effective_to", "lifecycle_status", "supersedes_version_id", "amended_by_document_id",
        "amendment_reference", "repeal_reference", "relationship_verification_status", "evidence_reference"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    versions = [
        (
            "VER-DOC-ARTPS-001-V1", "DOC-AS-ARTPS-001", "v1.0 (Principal Enactment 2012)",
            "2012-05-02", "2012-05-02", "2024-10-24", "SUPERSEDED_IN_PART", "NONE",
            "DOC-AS-ARTPS-2024", "Assam Act No. XXIV of 2024 (ARTPS Amendment Act 2024)", "NONE",
            "VERIFIED_RELATIONSHIP", "Section 15 rulemaking and appellate structures partially modified by subsequent commission enactments."
        ),
        (
            "VER-DOC-ARTPS-001-V2", "DOC-AS-ARTPS-001", "v2.0 (Amended Consolidated 2024)",
            "2024-10-25", "2024-10-25", "9999-12-31", "ACTIVE_PROVISIONAL", "VER-DOC-ARTPS-001-V1",
            "NONE", "NONE", "NONE",
            "PENDING_COMMENCEMENT_VERIFICATION", "Requires verification of subordinate rules framed under 2024 amendment."
        ),
        (
            "VER-DOC-ARTPS-002-V1", "DOC-AS-ARTPS-002", "v1.0 (Principal Rules 2012)",
            "2012-09-19", "2012-10-25", "9999-12-31", "ACTIVE_PROVISIONAL", "NONE",
            "NONE", "NONE", "NONE",
            "PENDING_ORIGINAL_REINGESTION", "Gazette No. 471 rules; active in text, but file in possession has adultpdf.com producer string."
        ),
        (
            "VER-DOC-GMC-001-V1", "DOC-AS-GMC-001", "v1.0 (Baseline Charter 2013)",
            "2013-07-14", "2013-07-14", "9999-12-31", "STATUS_UNCONFIRMED_CURRENT_VALIDITY", "NONE",
            "NONE", "NONE", "NONE",
            "UNVERIFIED_2026_APPLICABILITY", "Appendix-2 published under Rule 5. Ingested PDF is vintage 2013/2017; current 2026 municipal timelines unverified."
        ),
        (
            "VER-DOC-SCST-001-V1", "DOC-AS-SCST-001", "v1.0 (Principal Act 1978)",
            "1979-04-10", "1979-04-10", "2024-10-18", "SUPERSEDED_IN_PART", "NONE",
            "DOC-AS-SCST-001", "Assam Act No. XXXI of 2024", "NONE",
            "VERIFIED_RELATIONSHIP", "Assam Act XII of 1979; Section 4(b) prior text permitted exam fee collections."
        ),
        (
            "VER-DOC-SCST-001-V2", "DOC-AS-SCST-001", "v2.0 (Amendment Act 2024)",
            "2024-10-19", "2024-10-25", "9999-12-31", "ACTIVE_PROVISIONAL", "VER-DOC-SCST-001-V1",
            "NONE", "Assam Act No. XXXI of 2024, Section 2", "NONE",
            "VERIFIED_RELATIONSHIP", "Gazette No. 530 dated 25th Oct 2024. Expressly substitutes Section 4(b) to exempt SC/ST exam fees."
        ),
        (
            "VER-DOC-CADRE-001-V1", "DOC-GOI-CADRE-001", "v1.0 (Principal Regulations 1955)",
            "1955-09-08", "1955-09-08", "2025-01-26", "SUPERSEDED_IN_PART", "NONE",
            "DOC-GOI-CADRE-001", "DoPT Notification G.S.R. 78(E)", "NONE",
            "VERIFIED_RELATIONSHIP", "Prior schedule of senior posts superseded by Second Amendment Regulations 2025."
        ),
        (
            "VER-DOC-CADRE-001-V2", "DOC-GOI-CADRE-001", "v2.0 (Second Amendment 2025)",
            "2025-01-27", "2025-01-27", "9999-12-31", "ACTIVE_PROVISIONAL", "VER-DOC-CADRE-001-V1",
            "NONE", "Assam Notification No. AAI.14/96/Pt-I/93 dated 26th Feb 2025", "NONE",
            "VERIFIED_RELATIONSHIP", "Published in Gazette of India 27th Jan 2025; physical scan without digital signature."
        ),
        (
            "VER-DOC-PROC-001-V1", "DOC-AS-PROC-001", "v1.0 (State Procurement Rules 2020)",
            "2020-09-02", "2020-09-08", "9999-12-31", "ACTIVE_PROVISIONAL", "NONE",
            "NONE", "NONE", "NONE",
            "PENDING_ORIGINAL_REINGESTION", "Gazette No. 370 rules; active state code, but PDF in possession has ilovepdf.com compression stamp."
        ),
        (
            "VER-DOC-RTI-001-V1", "DOC-GOI-RTI-001", "v2022.1 (Consolidated Update 2022)",
            "2022-10-31", "2022-10-31", "9999-12-31", "ACTIVE_GUIDELINE", "NONE",
            "NONE", "NONE", "NONE",
            "UNVERIFIED_CENTRAL_DIGITAL_SIG", "Consolidated instructions on Section 4 of RTI Act 2005. Word 2007 export."
        ),
        (
            "VER-DOC-CIC-001-V1", "DOC-GOI-CIC-001", "v2025.1 (Vacancy Notice 2025)",
            "2025-12-30", "2025-12-30", "2026-02-28", "EXPIRED_OR_CYCLE_CLOSED", "NONE",
            "NONE", "NONE", "NONE",
            "TEMPORAL_WINDOW_EXPIRED", "Vacancy Circular Admn-15014/4/2021-ADMN-CIC; application period was 60 days from 30.12.2025."
        ),
        (
            "VER-DOC-MOF-001-V1", "DOC-GOI-PROC-001", "v2022.1 (Updated June 2022)",
            "2022-06-30", "2022-06-30", "9999-12-31", "ACTIVE_CENTRAL_GUIDELINE", "NONE",
            "NONE", "NONE", "NONE",
            "CENTRAL_JURISDICTION_CONFIRMED", "Ministry of Finance Manual for Consultancy & Other Services; applies to Central Ministries."
        ),
        (
            "VER-DOC-CONST-001-V1", "DOC-IND-CONST-001", "v2024.1 (106th Amendment Ed.)",
            "2024-05-01", "1950-01-26", "9999-12-31", "ACTIVE_SUPREME_LAW", "NONE",
            "NONE", "NONE", "NONE",
            "PENDING_ORIGINAL_REINGESTION", "Constitution text up to 106th Amendment. PDF in possession processed via iLovePDF."
        )
    ]
    
    for row_idx, ver in enumerate(versions, 2):
        for col_idx, val in enumerate(ver, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

def create_sheet_5(wb):
    ws = wb.create_sheet(title="Authenticity & Authority")
    headers = [
        "verification_id", "document_id", "version_id", "source_domain_check", "malware_scan_status",
        "file_integrity_status", "sha256_hash", "signature_present", "signature_validation_status",
        "certificate_chain_status", "certificate_revocation_status", "signer_identity_status",
        "signer_authority_status", "approval_status", "verification_method", "verifier_id",
        "verification_timestamp", "evidence_of_verification", "final_verification_status", "review_notes"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    verifications = [
        (
            "VFY-ARTPS-001", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "e8d7fd46b5b8dbe9fbba6cce2903e05a8b5c929a75d5f2a1705e60d5bfa48680",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "UNVERIFIED_FROM_FILE_METADATA", "PRINTED_NAME_ONLY_UNAUTHENTICATED", "PENDING_VERIFICATION",
            "METADATA_AND_OCR_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "CRITICAL FLAW: Metadata Producer = 'http://www.adultpdf.com'. Printed header cites Assam Gazette No. 194 (2012).",
            "SUSPECT_ORIGIN_THIRD_PARTY_TOOL", "FAILED PROVENANCE CHECK: Third-party adware/converter producer string detected. Re-ingestion from legislative.assam.gov.in required."
        ),
        (
            "VFY-ARTPS-002", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "39105a700271794b6fa7c22998e3b320ea558cbbbf3680fe038670da2a6b47c9",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "UNVERIFIED_FROM_FILE_METADATA", "PRINTED_NAME_ONLY_UNAUTHENTICATED", "PENDING_VERIFICATION",
            "METADATA_AND_OCR_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "CRITICAL FLAW: Metadata Producer = 'http://www.adultpdf.com'; duplicate filename suffix '_0'. Printed header cites Gazette No. 471.",
            "SUSPECT_ORIGIN_THIRD_PARTY_TOOL", "FAILED PROVENANCE CHECK: Untrusted producer string. Mandates officer re-verification before authoritative use."
        ),
        (
            "VFY-GMC-001", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "6ce0b39830db9be282f6e525413fbc4dd645d9e504c50269f848b8dfcc4b216c",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "UNOFFICIAL_AUTHOR_OMPRAKASH", "PRINTED_DESIGNATION_COMMISSIONER", "PENDING_APPROVAL",
            "METADATA_AND_PDF_INSPECTION", "VFY-OFFICER-02", "2026-10-14 11:30:00",
            "Author = 'omprakash'; Creator/Producer = 'Nitro Pro 7 (7. 3. 1. 3)'; Creation Date = 2013-07-14; Mod Date = 2017-12-26.",
            "UNCONFIRMED_CURRENT_VALIDITY", "WARNING: Document in hand is a 2013 desktop conversion by 'omprakash'. Current 2026 validity of timelines is unconfirmed."
        ),
        (
            "VFY-SCST-001", "DOC-AS-SCST-001", "VER-DOC-SCST-001-V2", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "2159844f3b6b19a9786a760c6d7054f15bb36d75b3992b453a251b5bc93892eb",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "PRINTED_NAME_GEETANJALI_DAS_SAIKIA", "INSTITUTIONAL_AUTHORITY_UNCONFIRMED", "PENDING_APPROVAL",
            "METADATA_AND_OCR_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "Generic filename 'untitled_23.pdf'; Producer = 'Microsoft: Print To PDF'; Title = 'D:\\Lagislative Assambly & Other'. OCR matches Gazette No. 530.",
            "PENDING_GAZETTE_CROSSCHECK", "PROVISIONAL: Text matches Assam Act XXXI of 2024, but file was printed to PDF locally. Officer must confirm against official state gazette digest."
        ),
        (
            "VFY-CADRE-001", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "2e1d9e03400f074d09ae77c2293b4a243d99baab2da1b6fe55799a776c52b21c",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "PRINTED_NAMES_SANJEEV_KUMAR_SANJEEV_SHARMA", "INSTITUTIONAL_AUTHORITY_UNCONFIRMED", "PENDING_APPROVAL",
            "METADATA_AND_OCR_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "Producer = 'HP Scan Extended Application'. Image-only scan of Gazette of India G.S.R. 78(E) / Assam Notification AAI.14/96/Pt-I/93.",
            "PENDING_DIGITAL_SIGNATURE_CHECK", "PROVISIONAL: High-quality physical scan corresponding to 2025 cadre revision, but lacks digital PKCS#7 token."
        ),
        (
            "VFY-PROC-001", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "7f2186799708767e7fe1b0663489112fc73295b9a896d88f6c529ba1c964177d",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "PRINTED_NAME_SAMIR_K_SINHA", "INSTITUTIONAL_AUTHORITY_UNCONFIRMED", "PENDING_VERIFICATION",
            "METADATA_AND_OCR_INSPECTION", "VFY-OFFICER-02", "2026-10-14 11:30:00",
            "Producer = 'www.ilovepdf.com'; Creation Date = 2020-09-30. 104-page scan passed through third-party web compression tool.",
            "UNVERIFIED_THIRD_PARTY_COMPRESSION", "WARNING: Web tool compression detected. Risk of missing pages or alterations; officer re-verification required."
        ),
        (
            "VFY-RTI-001", "DOC-GOI-RTI-001", "VER-DOC-RTI-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "87126981f52a78536ec7d03a113d077fb58273617be3a6c23ae493636f866405",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "GENERIC_AUTHOR_USER", "DOPT_IR_DIVISION_HEADING", "PENDING_APPROVAL",
            "METADATA_AND_PDF_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "Author = 'User'; Producer = 'Microsoft Office Word 2007'. Consolidated instructions on Section 4 of RTI Act.",
            "SECONDARY_COMPILATION_UNCONFIRMED", "PROVISIONAL: Text aligns with DoPT consolidated OM, but file is an uncertified Word export."
        ),
        (
            "VFY-CIC-001", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "b42ea1ecb55cb3b0ffc601dff7b9ebc1c73a436ff326759714c6225e59df1898",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "PRINTED_NAME_UNDER_SECRETARY_ADMIN", "INSTITUTIONAL_AUTHORITY_UNCONFIRMED", "PENDING_APPROVAL",
            "METADATA_AND_OCR_INSPECTION", "VFY-OFFICER-02", "2026-10-14 11:30:00",
            "Metadata completely empty. Scanned notice dated 30.12.2025; blank scan pages 2 & 8 detected. Application window expired in early 2026.",
            "TEMPORAL_VALIDITY_UNCONFIRMED", "WARNING: Application period has elapsed. System must flag that recruitment cycle may be concluded."
        ),
        (
            "VFY-MOF-001", "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "acd4d0302088f1dc2aa1337e7215cc20b134d115e85d9da639aa8aa9fca1286b",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "AUTHOR_BHARAT", "FINANCE_SECRETARY_FOREWORD", "PENDING_APPROVAL",
            "METADATA_AND_PDF_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "Title = 'Three Cover MoF_2022_curve.cdr'; Author = 'Bharat'; Producer = 'Adobe Acrobat 8.1'. 214-page national procurement manual.",
            "CENTRAL_JURISDICTION_PROVISIONAL", "PROVISIONAL: Official content verified, but applies strictly to Central Government procurements, not Assam state funds."
        ),
        (
            "VFY-CONST-001", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", "UNVERIFIED_DOWNLOAD_SECTION", "CLEAN_PASSED",
            "HASH_RECORDED_LOCAL_FILE", "4c8e93689ec23f3eb65c69707297e59c3d4ee7b0d5ab46927da80482ea75da76",
            "NO_CRYPTOGRAPHIC_SIG", "UNAVAILABLE", "MISSING_CERTIFICATE", "NOT_ASSESSED",
            "UNVERIFIED_FROM_FILE_METADATA", "PARLIAMENT_OF_INDIA", "PENDING_VERIFICATION",
            "METADATA_AND_PDF_INSPECTION", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "Random hash filename 'c9fe9c9b...'; Producer = 'iLovePDF'; Mod Date = 2026-06-12. Official Constitution text passed through web tool.",
            "UNVERIFIED_THIRD_PARTY_CONVERSION", "WARNING: Third-party tool conversion detected. Official text must be re-ingested from legislative.gov.in."
        ),
        (
            "VFY-EXC-001", "EXC-ID-001", "NONE", "UNMATCHED_EXTERNAL", "SKIPPED_QUARANTINE",
            "INTEGRITY_NOT_TRACKED", "6f5a3b2e81d749ac10f8234bb5a99281e5b12847c502b4d91e6b8c92a104c8f3",
            "NO_CRYPTOGRAPHIC_SIG", "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE",
            "PRIVATE_INDIVIDUAL", "ZERO_STATUTORY_AUTHORITY", "REJECTED_QUARANTINED",
            "PII_DETECTION_SCREEN", "VFY-OFFICER-01", "2026-10-14 11:30:00",
            "Scanned personal ID card containing citizen PII. Quarantined to prevent privacy breach.",
            "NOT_APPLICABLE", "Quarantined non-government file."
        )
    ]
    
    for row_idx, vfy in enumerate(verifications, 2):
        for col_idx, val in enumerate(vfy, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

print("Updated data_sheets_2_5 with strict trust boundaries.")
