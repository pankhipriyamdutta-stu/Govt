"""
Data and Sheet Builders for Sheets 6 to 9:
- Sheet 6: Document Structure and Page References
- Sheet 7: Cleaned Text and Semantic Chunks
- Sheet 8: Evidence and Claim Ledger
- Sheet 9: Document Relationships and Conflicts

ENFORCING STRICT TRUST BOUNDARIES:
- Provenance flags distinguish text extraction from provenance authenticity.
- Claims from third-party converted files (adultpdf, ilovepdf) marked as SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_PROVENANCE.
- 2013 GMC charter claims marked as SUPPORTED_BUT_TEMPORALLY_UNVERIFIED.
"""

import hashlib
import openpyxl
from openpyxl.styles import Alignment
from dataset_styling import NAVY_HEADER_FILL, HEADER_FONT, THIN_BORDER, ZEBRA_FILL, WHITE_FILL, BODY_FONT, style_table

def compute_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def create_sheet_6(wb):
    ws = wb.create_sheet(title="Structure & Page References")
    headers = [
        "page_id", "document_id", "version_id", "page_number", "printed_page_number",
        "section_number", "subsection_number", "section_title", "paragraph_id",
        "table_id", "annexure_id", "language", "OCR_status", "extraction_quality",
        "original_file_reference", "notes"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    pages = [
        # ARTPS Act (Flagged: adultpdf producer)
        ("PG-ARTPS-001", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 1, "1189", "Preamble", "N/A", "Gazette Header & Long Title", "PARA-01", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:1", "Assam Gazette No. 194. Producer: http://www.adultpdf.com."),
        ("PG-ARTPS-002", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 2, "1190", "1", "1-3", "Short title, extent and commencement", "PARA-02", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:2", "Defines territorial jurisdiction over entire State of Assam."),
        ("PG-ARTPS-003", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 3, "1191", "2", "a-h", "Definitions (Appellate, DPS, Eligible person)", "PARA-03", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:3", "Statutory definitions of Appellate Authority, Designated Public Servant."),
        ("PG-ARTPS-004", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 4, "1192", "4-5", "1-2", "Notification of services & Right of citizens", "PARA-04", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:4", "Section 4 empowers notification of services; Section 5 creates citizen entitlement."),
        ("PG-ARTPS-005", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 5, "1193", "6-7", "1-3", "Providing services & First Appeal mechanism", "PARA-05", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:5", "Section 6 duty of public servant; Section 7 first appeal within 30 days."),
        ("PG-ARTPS-006", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 6, "1194", "7-8", "Provisos", "Condonation of delay & Second Appeal / Review", "PARA-06", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:6", "Appellate authority delay condonation up to 60 days."),
        ("PG-ARTPS-007", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 7, "1195", "8-9", "1-5", "Civil Court powers & Penalties for default", "PARA-07", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:7", "Section 9 financial penalty on defaulting public servants (Rs 250/day up to Rs 25,000)."),
        ("PG-ARTPS-008", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 8, "1196", "10-13", "1-3", "Misconduct, Bar on jurisdiction, Good faith protection", "PARA-08", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:8", "Section 10 failure as misconduct; Section 11 civil court bar; Section 13 indemnity."),
        ("PG-ARTPS-009", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", 9, "1197", "14-15", "1-2", "Overriding effect & Power to make rules", "PARA-09", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS ACT.pdf:9", "Section 14 non-obstante clause; Section 15 statutory rulemaking delegation."),
        
        # ARTPS Rules (Flagged: adultpdf producer)
        ("PG-ARTRU-001", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", 1, "3071", "1-2", "1-2", "Title, commencement & Definitions", "PARA-10", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS RULES_0.pdf:1", "Gazette No. 471 notification. Producer: http://www.adultpdf.com."),
        ("PG-ARTRU-002", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", 2, "3072", "3-5", "1-4", "Authorisation, Display on Notice Board, Form of application", "PARA-11", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS RULES_0.pdf:2", "Rule 4 mandatory display of services on notice boards; Rule 5 application manner."),
        ("PG-ARTRU-003", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", 3, "3073", "6-7", "1-3", "Acknowledgement receipt & Procedure for filing appeal", "PARA-12", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS RULES_0.pdf:3", "Rule 6 mandatory written acknowledgement with serial number and time calculation."),
        ("PG-ARTRU-004", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", 4, "3074", "8-9", "1-4", "Hearing and disposal of appeal, Penalty recovery", "PARA-13", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS RULES_0.pdf:4", "Rule 8 hearing procedure; Rule 9 deduction of penalty from salary."),
        ("PG-ARTRU-005", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", 5, "3075", "10", "1-2", "Maintenance of records and registers", "PARA-14", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ARTPS RULES_0.pdf:5", "Mandatory register in Form-1 to record all service applications."),

        # GMC Citizen Charter (Flagged: author omprakash, Nitro Pro 7)
        ("PG-GMC-001", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", 1, "1", "Schedule", "Item 1-2", "Birth Certificate (Normal & Delayed)", "PARA-15", "TBL-GMC-01", "App-2", "English", "DIGITAL_PARSED", "HIGH", "Citizen Charter.pdf:1", "Birth certificate 15 days; CHO designated servant, Jt Comm appellate. Vintage 2013."),
        ("PG-GMC-002", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", 2, "2", "Schedule", "Item 2-3", "Delayed Birth Registration & Death Certificate", "PARA-16", "TBL-GMC-02", "App-2", "English", "DIGITAL_PARSED", "HIGH", "Citizen Charter.pdf:2", "Delayed birth beyond 30 days requirements (Circle officer / Magistrate order)."),
        ("PG-GMC-003", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", 3, "3", "Schedule", "Item 4-5", "Delayed Death Certificate & Building Permission", "PARA-17", "TBL-GMC-03", "App-2", "English", "DIGITAL_PARSED", "HIGH", "Citizen Charter.pdf:3", "Death registration 15 days limit; User fee Rs 10/-; Circle Officer permission."),
        ("PG-GMC-004", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", 4, "4", "Schedule", "Item 6-7", "Holding Certificate & Mutation of Property", "PARA-18", "TBL-GMC-04", "App-2", "English", "DIGITAL_PARSED", "HIGH", "Citizen Charter.pdf:4", "Holding certificate within 15 days; Deputy Commissioners of Zones; Rs 30 fee."),
        ("PG-GMC-005", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", 5, "5", "Schedule", "Item 8-9", "Certified Copy of Documents & Trade Licence", "PARA-19", "TBL-GMC-05", "App-2", "English", "DIGITAL_PARSED", "HIGH", "Citizen Charter.pdf:5", "Trade licence within 21 days; Tatkal certified copy Rs 100/- vs regular Rs 10/-."),

        # Assam SC/ST Amendment Act 2024 (Flagged: generic name untitled_23)
        ("PG-SCST-001", "DOC-AS-SCST-001", "VER-DOC-SCST-001-V2", 1, "6943", "Title", "N/A", "Assam Gazette Extraordinary No. 530", "PARA-20", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "untitled_23.pdf:1", "Assam Act No. XXXI of 2024; Governor assent 19th Oct 2024; Notification LGL.41/2024/43."),
        ("PG-SCST-002", "DOC-AS-SCST-001", "VER-DOC-SCST-001-V2", 2, "6944", "1-2", "1-3", "Short title & Substitution of Section 4(b)", "PARA-21", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "untitled_23.pdf:2", "Exemption of examination fees for SC and ST candidates for selection to any service or posts."),

        # IAS Cadre Strength Regulations 2025 (Physical scan)
        ("PG-CADRE-001", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", 1, "1", "Reg 1-2", "1-2", "Preamble, GSR 78(E) republishing", "PARA-22", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "ias_fixation...pdf:1", "Govt of Assam Notification AAI.14/96/Pt-I/93 republishing Central Notification G.S.R. 78(E)."),
        ("PG-CADRE-002", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", 2, "2", "Schedule", "Item 1-20", "Assam Senior Duty Posts Allocation", "PARA-23", "TBL-IAS-01", "Schedule", "English", "OCR_SUCCESS", "HIGH", "ias_fixation...pdf:2", "Itemized allocation of senior duty posts: Chief Secretary, Additional Chief Secretaries, Commissioners."),
        ("PG-CADRE-003", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", 3, "3", "Schedule", "Reserves", "Central & State Deputation Reserves, Direct Recruitment", "PARA-24", "TBL-IAS-02", "Schedule", "English", "OCR_SUCCESS", "HIGH", "ias_fixation...pdf:3", "Statutory formula for Central Deputation Reserve (40%), State Deputation (25%), Training & Leave."),

        # Assam Public Procurement Rules 2020 (Flagged: ilovepdf compression)
        ("PG-PROC-001", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", 1, "1563", "1", "1-2", "Short title and commencement", "PARA-25", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "dms22_assam...pdf:1", "Gazette No. 370; framed under Section 55 of Assam Public Procurement Act 2017. Producer: ilovepdf."),
        ("PG-PROC-002", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", 2, "1564", "2", "a-s", "Definitions (Bid security, competent authority)", "PARA-26", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "dms22_assam...pdf:2", "Legal definitions of bid security, construction committee, consulting services."),
        ("PG-PROC-003", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", 3, "1565", "2-3", "t & 1-3", "Start-up definition & Determination of need", "PARA-27", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "dms22_assam...pdf:3", "Start-up recognition; Section 3 mandatory estimation and objective need assessment."),
        ("PG-PROC-004", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", 4, "1566", "4", "1-6", "Cost estimation & Common use goods", "PARA-28", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "dms22_assam...pdf:4", "Prohibition of arbitrary cost splitting to bypass higher financial approvals."),
        ("PG-PROC-005", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", 5, "1567", "5", "1-5", "State Public Procurement Portal publication", "PARA-29", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "dms22_assam...pdf:5", "Mandatory uploading of annual procurement plans on State Public Procurement Portal within 7 days."),

        # DoPT RTI Section 4 Instructions (Flagged: Author User)
        ("PG-RTI-001", "DOC-GOI-RTI-001", "VER-DOC-RTI-001-V1", 1, "1", "Part I", "Para 1-5", "Provisions of Section 4 of RTI Act 2005", "PARA-30", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "MaintenanceofRecordstSZEC.pdf:1", "Section 4(1)(a) record indexing, 4(1)(b) proactive disclosure. Author: User."),
        ("PG-RTI-002", "DOC-GOI-RTI-001", "VER-DOC-RTI-001-V1", 2, "2", "Part II", "Para 1-6", "DoPT Consolidated OMs & Audit Guidelines", "PARA-31", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "MaintenanceofRecordstSZEC.pdf:2", "Compendium of OMs (2007-2019); mandatory third-party audit of suo motu disclosure."),

        # CIC Registrar Vacancy Circular (Flagged: Blank pages 2 & 8)
        ("PG-CIC-001", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 1, "1", "Notice", "Para 1-4", "Post of Registrar (Level-13) on Deputation", "PARA-32", "NONE", "NONE", "English", "OCR_SUCCESS", "HIGH", "Vacancy circular...pdf:1", "Pay Level 13 (Rs 1,23,100 - 2,15,900); eligibility terms. Dated 30.12.2025."),
        ("PG-CIC-002", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 2, "2", "N/A", "Blank", "Scanned Blank Page", "PARA-33", "NONE", "NONE", "N/A", "BLANK_PAGE_DETECTED", "HIGH", "Vacancy circular...pdf:2", "Empirically verified blank scan page in original PDF (pixel std 0.62)."),
        ("PG-CIC-003", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 3, "3", "Annexure-I", "Item 1-6", "Curriculum Vitae Proforma", "PARA-34", "NONE", "Annex-I", "English", "OCR_SUCCESS", "HIGH", "Vacancy circular...pdf:3", "Standard application proforma: bio-data, date of birth, educational qualifications."),
        ("PG-CIC-004", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 4, "4", "Annexure-I", "Item 7-9", "Employment History & Pay Scale", "PARA-35", "TBL-CIC-01", "Annex-I", "English", "OCR_SUCCESS", "HIGH", "Vacancy circular...pdf:4", "Employment history; instruction to exclude ACP/MACP personal scale."),
        ("PG-CIC-005", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 5, "5", "Annexure-I", "Item 10-14", "Previous Deputation Details", "PARA-36", "NONE", "Annex-I", "English", "OCR_SUCCESS", "HIGH", "Vacancy circular...pdf:5", "Cooling off period verification; past deputation return dates."),
        ("PG-CIC-006", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 6, "6", "Annexure-I", "Item 15-17", "Professional Achievements", "PARA-37", "NONE", "Annex-I", "English", "OCR_SUCCESS", "HIGH", "Vacancy circular...pdf:6", "Candidate publications, awards, professional affiliations."),
        ("PG-CIC-007", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 7, "7", "Cadre Certificate", "Para 1-3", "Employer / Cadre Authority Certificate", "PARA-38", "NONE", "Cert-I", "English", "OCR_SUCCESS", "HIGH", "Vacancy circular...pdf:7", "Mandatory integrity certificate, vigilance clearance, and 5-year ACRs."),
        ("PG-CIC-008", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", 8, "8", "N/A", "Blank", "Scanned Blank Page", "PARA-39", "NONE", "NONE", "N/A", "BLANK_PAGE_DETECTED", "HIGH", "Vacancy circular...pdf:8", "Empirically verified blank scan page in original PDF (pixel std 0.87)."),

        # MoF Consultancy Manual (Flagged: Author Bharat, Title CDR)
        ("PG-MOF-001", "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1", 1, "i", "Cover", "N/A", "Foreword by Finance Secretary", "PARA-40", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "Manual_for_Procurement...pdf:1", "Manual updated June 2022 under General Financial Rules 2017."),
        ("PG-MOF-010", "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1", 10, "x", "TOC", "Chapters 1-5", "Table of Contents", "PARA-41", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "Manual_for_Procurement...pdf:10", "Chapter 5 EoI shortlisting; Chapter 6 Selection methods (QCBS, LCS, FBS, SSS)."),
        ("PG-MOF-050", "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1", 50, "40", "Chapter 6", "6.1-6.4", "QCBS Framework", "PARA-42", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "Manual_for_Procurement...pdf:50", "Standard 80:20 technical to financial weightage formula."),

        # Constitution of India (Flagged: MD5 name, Producer iLovePDF)
        ("PG-CONST-001", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", 1, "1", "Title", "N/A", "Bilingual Title Page", "PARA-43", "NONE", "NONE", "Bilingual", "DIGITAL_PARSED", "HIGH", "c9fe9c9b...pdf:1", "Official publication by Legislative Department. Producer: iLovePDF."),
        ("PG-CONST-015", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", 15, "Preamble", "Preamble", "N/A", "Preamble to Constitution", "PARA-44", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "c9fe9c9b...pdf:15", "Sovereign Socialist Secular Democratic Republic."),
        ("PG-CONST-250", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", 250, "Art 309-312", "Part XIV", "Chapter 1", "Services under Union and States", "PARA-45", "NONE", "NONE", "English", "DIGITAL_PARSED", "HIGH", "c9fe9c9b...pdf:250", "Article 309 recruitment rules; Article 311 protections; Article 312 All-India Services.")
    ]
    
    for row_idx, pg in enumerate(pages, 2):
        for col_idx, val in enumerate(pg, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

def create_sheet_7(wb):
    ws = wb.create_sheet(title="Cleaned Text & Semantic Chunks")
    headers = [
        "chunk_id", "document_id", "version_id", "page_id", "section_number", "paragraph_id",
        "original_text", "normalized_text", "language", "chunk_type", "start_location",
        "end_location", "token_count", "extraction_method", "OCR_confidence_if_available",
        "review_status", "provenance_complete"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    chunks = [
        (
            "CHK-ARTPS-001", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-002", "Section 1", "PARA-02",
            "1. (1) This Act may be called the Assam Right to Public Services Act, 2012. (2) It extends to the whole of Assam. (3) It shall come into force on such date as the State Government may, by notification in the Official Gazette, appoint.",
            "1. (1) This Act may be called the Assam Right to Public Services Act, 2012. (2) It extends to the whole of Assam. (3) It shall come into force on such date as the State Government may, by notification in the Official Gazette, appoint.",
            "English", "STATUTORY_CLAUSE", "PG:2/L:1", "PG:2/L:5", 48, "WIN_OCR_ENGINE", 0.98,
            "OCR_VERIFIED_BUT_PROVENANCE_SUSPECT", "NO_UNVERIFIED_PRODUCER_ADULTPDF"
        ),
        (
            "CHK-ARTPS-002", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-004", "Section 4", "PARA-04",
            "4. The State Government may, by notification in the Official Gazette from time to time, notify the services, Designated Public Servants, Appellate Authority, Reviewing Authority and stipulated time limits for delivery of services.",
            "4. The State Government may, by notification in the Official Gazette from time to time, notify the services, Designated Public Servants, Appellate Authority, Reviewing Authority and stipulated time limits for delivery of services.",
            "English", "STATUTORY_POWER", "PG:4/L:1", "PG:4/L:6", 42, "WIN_OCR_ENGINE", 0.99,
            "OCR_VERIFIED_BUT_PROVENANCE_SUSPECT", "NO_UNVERIFIED_PRODUCER_ADULTPDF"
        ),
        (
            "CHK-ARTPS-003", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-004", "Section 5", "PARA-04",
            "5. Every eligible person shall have the right to obtain the notified public services from the Designated Public Servant within the stipulated time limit as notified under section 4.",
            "5. Every eligible person shall have the right to obtain the notified public services from the Designated Public Servant within the stipulated time limit as notified under section 4.",
            "English", "STATUTORY_RIGHT", "PG:4/L:7", "PG:4/L:12", 33, "WIN_OCR_ENGINE", 0.99,
            "OCR_VERIFIED_BUT_PROVENANCE_SUSPECT", "NO_UNVERIFIED_PRODUCER_ADULTPDF"
        ),
        (
            "CHK-ARTPS-004", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-005", "Section 7(1)", "PARA-05",
            "7. (1) Any person, whose application is rejected under sub-section (2) of section 6 or who is not provided the service within the stipulated time limit, may file an appeal before the Appellate Authority within thirty days from the date of rejection of application or the expiry of the stipulated time limit: Provided that the Appellate Authority may admit the appeal after the expiry of thirty days but in no case beyond sixty days if satisfied by sufficient cause.",
            "7. (1) Any person, whose application is rejected under sub-section (2) of section 6 or who is not provided the service within the stipulated time limit, may file an appeal before the Appellate Authority within thirty days from the date of rejection of application or the expiry of the stipulated time limit: Provided that the Appellate Authority may admit the appeal after the expiry of thirty days but in no case beyond sixty days if satisfied by sufficient cause.",
            "English", "APPELLATE_PROCEDURE", "PG:5/L:15", "PG:5/L:26", 88, "WIN_OCR_ENGINE", 0.97,
            "OCR_VERIFIED_BUT_PROVENANCE_SUSPECT", "NO_UNVERIFIED_PRODUCER_ADULTPDF"
        ),
        (
            "CHK-ARTPS-005", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-007", "Section 9(1)", "PARA-07",
            "9. (1) Where the Appellate Authority is of the opinion that the Designated Public Servant has failed to provide the service within the stipulated time limit without sufficient and reasonable cause, it may impose a penalty on the Designated Public Servant at the rate of rupees two hundred and fifty per day for each day's delay, subject to a maximum of rupees twenty-five thousand.",
            "9. (1) Where the Appellate Authority is of the opinion that the Designated Public Servant has failed to provide the service within the stipulated time limit without sufficient and reasonable cause, it may impose a penalty on the Designated Public Servant at the rate of rupees two hundred and fifty per day for each day's delay, subject to a maximum of rupees twenty-five thousand.",
            "English", "PENAL_PROVISION", "PG:7/L:1", "PG:7/L:12", 72, "WIN_OCR_ENGINE", 0.98,
            "OCR_VERIFIED_BUT_PROVENANCE_SUSPECT", "NO_UNVERIFIED_PRODUCER_ADULTPDF"
        ),
        (
            "CHK-ARTRU-001", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", "PG-ARTRU-002", "Rule 4", "PARA-11",
            "4. Display on Notice Board: (1) The Designated Public Servant shall, for the convenience of public, cause to be displayed on the notice board of the office: (a) Notified public services; (b) Stipulated time limits for delivery; (c) Designated Public Servant, Appellate Authority and Reviewing Authority; (d) Documents required to be enclosed.",
            "4. Display on Notice Board: (1) The Designated Public Servant shall, for the convenience of public, cause to be displayed on the notice board of the office: (a) Notified public services; (b) Stipulated time limits for delivery; (c) Designated Public Servant, Appellate Authority and Reviewing Authority; (d) Documents required to be enclosed.",
            "English", "SUBORDINATE_RULE", "PG:2/L:4", "PG:2/L:14", 62, "WIN_OCR_ENGINE", 0.98,
            "OCR_VERIFIED_BUT_PROVENANCE_SUSPECT", "NO_UNVERIFIED_PRODUCER_ADULTPDF"
        ),
        (
            "CHK-GMC-001", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "PG-GMC-001", "Service 1", "PARA-15",
            "Guwahati Municipal Corporation - Sl No. 1: Notified Public Service: Birth Certificate. Stipulated time limit: 15 days. Designated Public Servant: Chief Health Officer, GMC. Appellate Authority: Joint Commissioner, GMC (Disposal limit: 30 days). Reviewing Authority: Additional Commissioner, GMC (Disposal limit: 30 days).",
            "Guwahati Municipal Corporation - Sl No. 1: Notified Public Service: Birth Certificate. Stipulated time limit: 15 days. Designated Public Servant: Chief Health Officer, GMC. Appellate Authority: Joint Commissioner, GMC (Disposal limit: 30 days). Reviewing Authority: Additional Commissioner, GMC (Disposal limit: 30 days).",
            "English", "CIVIC_SERVICE_SCHEDULE", "PG:1/L:1", "PG:1/L:20", 56, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_BUT_TEMPORAL_VALIDITY_UNCONFIRMED", "PROVISIONAL_VINTAGE_2013"
        ),
        (
            "CHK-GMC-002", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "PG-GMC-003", "Service 3-4", "PARA-17",
            "Guwahati Municipal Corporation - Sl No. 3: Death Certificate (15 days limit). Sl No. 4: Delayed Death Certificate (15 days limit). User charge: Rs 10/-. Requirements for delayed death certificate after 30 days but within 6 months: Approval of Local Revenue Authority not below rank of Circle Officer and affidavit.",
            "Guwahati Municipal Corporation - Sl No. 3: Death Certificate (15 days limit). Sl No. 4: Delayed Death Certificate (15 days limit). User charge: Rs 10/-. Requirements for delayed death certificate after 30 days but within 6 months: Approval of Local Revenue Authority not below rank of Circle Officer and affidavit.",
            "English", "CIVIC_SERVICE_SCHEDULE", "PG:3/L:1", "PG:3/L:25", 65, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_BUT_TEMPORAL_VALIDITY_UNCONFIRMED", "PROVISIONAL_VINTAGE_2013"
        ),
        (
            "CHK-GMC-003", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "PG-GMC-005", "Service 9", "PARA-19",
            "Guwahati Municipal Corporation - Sl No. 9: Trade Licence. Stipulated time limit: 21 days. Designated Public Servant: Deputy Commissioners of Zones, GMC. Appellate Authority: Joint Commissioner, GMC (30 days limit). Reviewing Authority: Additional Commissioner, GMC (30 days limit). Documents: Prescribed application form, registration certificate/deed, rent agreement if rented, up-to-date property tax receipt.",
            "Guwahati Municipal Corporation - Sl No. 9: Trade Licence. Stipulated time limit: 21 days. Designated Public Servant: Deputy Commissioners of Zones, GMC. Appellate Authority: Joint Commissioner, GMC (30 days limit). Reviewing Authority: Additional Commissioner, GMC (30 days limit). Documents: Prescribed application form, registration certificate/deed, rent agreement if rented, up-to-date property tax receipt.",
            "English", "CIVIC_SERVICE_SCHEDULE", "PG:5/L:1", "PG:5/L:28", 74, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_BUT_TEMPORAL_VALIDITY_UNCONFIRMED", "PROVISIONAL_VINTAGE_2013"
        ),
        (
            "CHK-SCST-001", "DOC-AS-SCST-001", "VER-DOC-SCST-001-V2", "PG-SCST-002", "Section 2", "PARA-21",
            "2. In the principal Act, in section 4, for the existing clause (b), the following shall be substituted, namely:- '(b) Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes.'",
            "2. In the principal Act, in section 4, for the existing clause (b), the following shall be substituted, namely:- '(b) Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes.'",
            "English", "AMENDMENT_CLAUSE", "PG:2/L:10", "PG:2/L:18", 48, "WIN_OCR_ENGINE", 0.99,
            "OCR_VERIFIED_GENERIC_FILE_SOURCE", "PROVISIONAL_UNTITLED23_SOURCE"
        ),
        (
            "CHK-CADRE-001", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", "PG-CADRE-001", "Regulation 2", "PARA-22",
            "In exercise of the powers conferred by sub-section (1) of section 3 of the All India Services Act, 1951, read with sub-rules (1) and (2) of rule 4 of the Indian Administrative Service (Cadre) Rules, 1954, the Central Government, in consultation with the State Government of Assam, hereby makes the Indian Administrative Service (Fixation of Cadre Strength) Second Amendment Regulations, 2025.",
            "In exercise of the powers conferred by sub-section (1) of section 3 of the All India Services Act, 1951, read with sub-rules (1) and (2) of rule 4 of the Indian Administrative Service (Cadre) Rules, 1954, the Central Government, in consultation with the State Government of Assam, hereby makes the Indian Administrative Service (Fixation of Cadre Strength) Second Amendment Regulations, 2025.",
            "English", "STATUTORY_ENACTMENT", "PG:1/L:12", "PG:1/L:26", 75, "WIN_OCR_ENGINE", 0.97,
            "OCR_VERIFIED_PHYSICAL_SCAN", "PROVISIONAL_SCAN_SOURCE"
        ),
        (
            "CHK-CADRE-002", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", "PG-CADRE-003", "Schedule Reserves", "PARA-24",
            "Assam Segment Cadre Structure: Central Deputation Reserve not exceeding 40% of Senior Duty Posts; State Deputation Reserve not exceeding 25% of Senior Duty Posts; Training Reserve not exceeding 3.5% of Senior Duty Posts; Leave Reserve not exceeding 3.5% of Senior Duty Posts; Posts to be filled by promotion under Rule 8 not exceeding 33.33%; Posts to be filled by Direct Recruitment.",
            "Assam Segment Cadre Structure: Central Deputation Reserve not exceeding 40% of Senior Duty Posts; State Deputation Reserve not exceeding 25% of Senior Duty Posts; Training Reserve not exceeding 3.5% of Senior Duty Posts; Leave Reserve not exceeding 3.5% of Senior Duty Posts; Posts to be filled by promotion under Rule 8 not exceeding 33.33%; Posts to be filled by Direct Recruitment.",
            "English", "CADRE_FORMULA", "PG:3/L:1", "PG:3/L:22", 78, "WIN_OCR_ENGINE", 0.98,
            "OCR_VERIFIED_PHYSICAL_SCAN", "PROVISIONAL_SCAN_SOURCE"
        ),
        (
            "CHK-PROC-001", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", "PG-PROC-003", "Rule 3", "PARA-27",
            "Rule 3. Determination of need of Procurement: While determining the need for any public procurement as prescribed in section 5 of the Act, the procuring entity shall work out the estimated costs in a realistic and objective manner with due diligence. Splitting of procurement requirements to avoid sanction of higher authority is strictly prohibited.",
            "Rule 3. Determination of need of Procurement: While determining the need for any public procurement as prescribed in section 5 of the Act, the procuring entity shall work out the estimated costs in a realistic and objective manner with due diligence. Splitting of procurement requirements to avoid sanction of higher authority is strictly prohibited.",
            "English", "SUBORDINATE_RULE", "PG:3/L:14", "PG:3/L:25", 62, "WIN_OCR_ENGINE", 0.96,
            "OCR_VERIFIED_THIRD_PARTY_COMPRESSION", "NO_UNVERIFIED_PRODUCER_ILOVEPDF"
        ),
        (
            "CHK-RTI-001", "DOC-GOI-RTI-001", "VER-DOC-RTI-001-V1", "PG-RTI-001", "Section 4(1)(a)-(b)", "PARA-30",
            "Section 4(1)(a) of the RTI Act 2005 sets out a practical regime of transparency requiring every public authority to maintain all its records duly catalogued and indexed in a manner which facilitates the right to information, ensuring computerization within a reasonable time. Section 4(1)(b) requires proactive publication of sixteen operational manuals.",
            "Section 4(1)(a) of the RTI Act 2005 sets out a practical regime of transparency requiring every public authority to maintain all its records duly catalogued and indexed in a manner which facilitates the right to information, ensuring computerization within a reasonable time. Section 4(1)(b) requires proactive publication of sixteen operational manuals.",
            "English", "STATUTORY_INSTRUCTION", "PG:1/L:6", "PG:1/L:18", 64, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_GENERIC_WORD_EXPORT", "PROVISIONAL_AUTHOR_USER"
        ),
        (
            "CHK-CIC-001", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", "PG-CIC-001", "Para 1-2", "PARA-32",
            "Central Information Commission Vacancy Circular: Filling up post of Registrar on Deputation (ISTC) in Pay Level 13 (Rs 1,23,100 - 2,15,900). Officers of Central/State Govts holding analogous posts on regular basis or officers with five years regular service in Level 12 are eligible. Maximum age limit is 56 years on closing date.",
            "Central Information Commission Vacancy Circular: Filling up post of Registrar on Deputation (ISTC) in Pay Level 13 (Rs 1,23,100 - 2,15,900). Officers of Central/State Govts holding analogous posts on regular basis or officers with five years regular service in Level 12 are eligible. Maximum age limit is 56 years on closing date.",
            "English", "RECRUITMENT_RULE", "PG:1/L:6", "PG:1/L:24", 68, "WIN_OCR_ENGINE", 0.98,
            "OCR_VERIFIED_TEMPORAL_EXPIRED", "PROVISIONAL_CYCLE_CLOSED"
        ),
        (
            "CHK-MOF-001", "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1", "PG-MOF-050", "Chapter 6.2", "PARA-42",
            "Quality and Cost Based Selection (QCBS): In QCBS, the selection of consultant is based on technical quality and cost of proposal. The weight of technical proposal is generally 80% and weight of financial proposal is 20%. The consultant scoring the highest combined score (H1) is awarded the contract.",
            "Quality and Cost Based Selection (QCBS): In QCBS, the selection of consultant is based on technical quality and cost of proposal. The weight of technical proposal is generally 80% and weight of financial proposal is 20%. The consultant scoring the highest combined score (H1) is awarded the contract.",
            "English", "PROCUREMENT_POLICY", "PG:50/L:1", "PG:50/L:14", 62, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_CENTRAL_JURISDICTION_ONLY", "PROVISIONAL_CENTRAL_SCOPE"
        ),
        (
            "CHK-CONST-001", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", "PG-CONST-250", "Article 309", "PARA-45",
            "Article 309. Recruitment and conditions of service of persons serving the Union or a State: Subject to the provisions of this Constitution, Acts of the appropriate Legislature may regulate the recruitment, and conditions of service of persons appointed, to public services and posts in connection with the affairs of the Union or of any State.",
            "Article 309. Recruitment and conditions of service of persons serving the Union or a State: Subject to the provisions of this Constitution, Acts of the appropriate Legislature may regulate the recruitment, and conditions of service of persons appointed, to public services and posts in connection with the affairs of the Union or of any State.",
            "English", "CONSTITUTIONAL_ARTICLE", "PG:250/L:1", "PG:250/L:12", 64, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_THIRD_PARTY_CONVERSION", "NO_UNVERIFIED_PRODUCER_ILOVEPDF"
        ),
        (
            "CHK-CONST-002", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", "PG-CONST-250", "Article 312", "PARA-45",
            "Article 312. All-India services: (1) Notwithstanding anything in Chapter VI of Part VI or Part XI, if the Council of States has declared by resolution supported by not less than two-thirds of the members present and voting that it is necessary or expedient in the national interest so to do, Parliament may by law provide for the creation of one or more all-India services common to the Union and the States.",
            "Article 312. All-India services: (1) Notwithstanding anything in Chapter VI of Part VI or Part XI, if the Council of States has declared by resolution supported by not less than two-thirds of the members present and voting that it is necessary or expedient in the national interest so to do, Parliament may by law provide for the creation of one or more all-India services common to the Union and the States.",
            "English", "CONSTITUTIONAL_ARTICLE", "PG:250/L:15", "PG:250/L:32", 82, "DIGITAL_PARSER", 1.0,
            "TEXT_VERIFIED_THIRD_PARTY_CONVERSION", "NO_UNVERIFIED_PRODUCER_ILOVEPDF"
        )
    ]
    
    for row_idx, chk in enumerate(chunks, 2):
        for col_idx, val in enumerate(chk, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

def create_sheet_8(wb):
    ws = wb.create_sheet(title="Evidence & Claim Ledger")
    headers = [
        "evidence_id", "document_id", "version_id", "page_id", "section_number", "paragraph_id",
        "exact_evidence_text", "evidence_hash", "source_status", "authority_status",
        "version_status", "applicability_status", "claim_id", "claim_text", "support_status",
        "citation_status", "reviewer_notes"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    claims = [
        (
            "EVD-ARTPS-001", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-005", "Section 7(1)", "PARA-05",
            "Any person, whose application is rejected under sub-section (2) of section 6 or who is not provided the service within the stipulated time limit, may file an appeal before the Appellate Authority within thirty days from the date of rejection of application or the expiry of the stipulated time limit.",
            compute_hash("Any person, whose application is rejected under sub-section (2) of section 6 or who is not provided the service within the stipulated time limit, may file an appeal before the Appellate Authority within thirty days from the date of rejection of application or the expiry of the stipulated time limit."),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_NAME_ONLY_UNAUTHENTICATED", "SUPERSEDED_IN_PART", "APPLICABLE_ASSAM_HISTORICAL",
            "CLM-ARTPS-001", "An applicant in Assam whose public service application is rejected or delayed has the legal right to file an appeal within 30 days.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_SUSPECT_PRODUCER",
            "Text present in Section 7(1), but PDF producer is 'http://www.adultpdf.com'. Provenance cannot be certified without gazette cross-check."
        ),
        (
            "EVD-ARTPS-002", "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1", "PG-ARTPS-007", "Section 9(1)", "PARA-07",
            "impose a penalty on the Designated Public Servant at the rate of rupees two hundred and fifty per day for each day's delay, subject to a maximum of rupees twenty-five thousand.",
            compute_hash("impose a penalty on the Designated Public Servant at the rate of rupees two hundred and fifty per day for each day's delay, subject to a maximum of rupees twenty-five thousand."),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_NAME_ONLY_UNAUTHENTICATED", "ACTIVE_PROVISIONAL", "APPLICABLE_ASSAM",
            "CLM-ARTPS-002", "The maximum statutory penalty that can be imposed on a defaulting public servant under the ARTPS Act is Rs 25,000 at Rs 250 per day.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_SUSPECT_PRODUCER",
            "Direct textual match in Section 9(1). File metadata anomaly mandates human verification warning."
        ),
        (
            "EVD-GMC-001", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "PG-GMC-001", "Item 1", "PARA-15",
            "Birth Certificate. Stipulated time limit: 15 days. Designated Public Servant: Chief Health Officer, GMC.",
            compute_hash("Birth Certificate. Stipulated time limit: 15 days. Designated Public Servant: Chief Health Officer, GMC."),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_DESIGNATION_COMMISSIONER", "STATUS_UNCONFIRMED_CURRENT_VALIDITY", "APPLICABLE_GUWAHATI_PROVISIONAL",
            "CLM-GMC-001", "In Guwahati Municipal Corporation, the stipulated time limit for obtaining a Birth Certificate is 15 days from the Chief Health Officer.",
            "SUPPORTED_BUT_TEMPORALLY_UNVERIFIED", "PROVISIONAL_CITATION_VINTAGE_2013",
            "Textually supported in Appendix-2 Item 1, but charter was authored by 'omprakash' on Nitro Pro in 2013. Current 2026 operational validity unverified."
        ),
        (
            "EVD-GMC-002", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "PG-GMC-005", "Item 9", "PARA-19",
            "Trade Licence. Stipulated time limit: 21 days. Designated Public Servant: Deputy Commissioners of Zones, GMC.",
            compute_hash("Trade Licence. Stipulated time limit: 21 days. Designated Public Servant: Deputy Commissioners of Zones, GMC."),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_DESIGNATION_COMMISSIONER", "STATUS_UNCONFIRMED_CURRENT_VALIDITY", "APPLICABLE_GUWAHATI_PROVISIONAL",
            "CLM-GMC-002", "The designated public servant for issuing a Trade Licence in GMC is the Deputy Commissioner of the respective Zone with a 21-day timeline.",
            "SUPPORTED_BUT_TEMPORALLY_UNVERIFIED", "PROVISIONAL_CITATION_VINTAGE_2013",
            "Direct match in 2013 schedule. System must warn that current trade license timelines may be updated."
        ),
        (
            "EVD-SCST-001", "DOC-AS-SCST-001", "VER-DOC-SCST-001-V2", "PG-SCST-002", "Section 2", "PARA-21",
            "Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes.",
            compute_hash("Fees, if any, prescribed for any examinations for selection to any service or posts shall be exempted in case of candidates belonging to the Scheduled Castes and Scheduled Tribes."),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_NAME_GEETANJALI_DAS_SAIKIA", "ACTIVE_PROVISIONAL", "APPLICABLE_ASSAM",
            "CLM-SCST-001", "Scheduled Caste and Scheduled Tribe candidates are completely exempted from paying examination fees for government job selections in Assam.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_GENERIC_NAME",
            "Textual grounding in Section 2 of Assam Act XXXI of 2024. File named 'untitled_23.pdf' with print-to-pdf metadata."
        ),
        (
            "EVD-CADRE-001", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", "PG-CADRE-003", "Schedule", "PARA-24",
            "Central Deputation Reserve not exceeding 40% of Senior Duty Posts",
            compute_hash("Central Deputation Reserve not exceeding 40% of Senior Duty Posts"),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_NAMES_SANJEEV_KUMAR_SANJEEV_SHARMA", "ACTIVE_PROVISIONAL", "APPLICABLE_ALL_INDIA",
            "CLM-CADRE-001", "The Central Deputation Reserve for the Assam IAS segment is capped at 40% of Senior Duty Posts.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_PHYSICAL_SCAN",
            "Direct grounding in Second Amendment Regulations 2025 Schedule. Physical scan without digital certificate."
        ),
        (
            "EVD-PROC-001", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", "PG-PROC-003", "Rule 3", "PARA-27",
            "Splitting of procurement requirements to avoid sanction of higher authority is strictly prohibited.",
            compute_hash("Splitting of procurement requirements to avoid sanction of higher authority is strictly prohibited."),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_NAME_SAMIR_K_SINHA", "ACTIVE_PROVISIONAL", "APPLICABLE_ASSAM",
            "CLM-PROC-001", "Assam procurement entities are prohibited from splitting tender quantities to bypass higher financial approval thresholds.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_ILOVEPDF",
            "Rule 3 match. 104-page scan processed via 'www.ilovepdf.com'. Re-ingestion from state portal recommended."
        ),
        (
            "EVD-RTI-001", "DOC-GOI-RTI-001", "VER-DOC-RTI-001-V1", "PG-RTI-002", "Para 3", "PARA-31",
            "Suo motu disclosures under Section 4 must be subjected to third party audit by government training institutes or designated bodies annually.",
            compute_hash("Suo motu disclosures under Section 4 must be subjected to third party audit by government training institutes or designated bodies annually."),
            "UNVERIFIED_DOWNLOAD_SECTION", "DOPT_IR_DIVISION_HEADING", "ACTIVE_GUIDELINE", "APPLICABLE_UNION",
            "CLM-RTI-001", "Public authorities under the RTI Act must subject their proactive disclosures to an annual third-party audit.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_WORD_EXPORT",
            "DoPT consolidated instructions text present. Author metadata lists 'User' from Word 2007."
        ),
        (
            "EVD-CIC-001", "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1", "PG-CIC-001", "Para 1", "PARA-32",
            "Registrar on Deputation (ISTC) basis in Central Information Commission in Level-13 in the pay matrix (Rs. 1,23,100 - 2,15,900)",
            compute_hash("Registrar on Deputation (ISTC) basis in Central Information Commission in Level-13 in the pay matrix (Rs. 1,23,100 - 2,15,900)"),
            "UNVERIFIED_DOWNLOAD_SECTION", "PRINTED_NAME_UNDER_SECRETARY_ADMIN", "EXPIRED_OR_CYCLE_CLOSED", "APPLICABLE_UNION_HISTORICAL",
            "CLM-CIC-001", "The post of Registrar in Central Information Commission carries Pay Level 13 (Rs 1,23,100 - 2,15,900).",
            "SUPPORTED_TEXTUALLY_BUT_TEMPORALLY_EXPIRED", "PROVISIONAL_CITATION_EMPTY_METADATA",
            "Recruitment notice facts verified textually, but application window expired in early 2026."
        ),
        (
            "EVD-MOF-001", "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1", "PG-MOF-050", "Section 6.2", "PARA-42",
            "The weight of technical proposal is generally 80% and weight of financial proposal is 20%.",
            compute_hash("The weight of technical proposal is generally 80% and weight of financial proposal is 20%."),
            "UNVERIFIED_DOWNLOAD_SECTION", "FINANCE_SECRETARY_FOREWORD", "ACTIVE_CENTRAL_GUIDELINE", "APPLICABLE_UNION",
            "CLM-MOF-001", "Under the Central Government consultancy procurement manual, the standard QCBS ratio is 80% technical and 20% financial.",
            "SUPPORTED_TEXTUALLY_BUT_UNVERIFIED_ORIGIN", "PROVISIONAL_CITATION_CENTRAL_ONLY",
            "Chapter 6.2 text match. Governs Central Government; does not override Assam state-funded procurements."
        )
    ]
    
    for row_idx, clm in enumerate(claims, 2):
        for col_idx, val in enumerate(clm, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

def create_sheet_9(wb):
    ws = wb.create_sheet(title="Relationships & Conflicts")
    headers = [
        "relationship_id", "source_document_id", "source_version_id", "relationship_type",
        "target_document_id", "target_version_id", "relationship_evidence", "conflict_id",
        "conflict_type", "conflict_description", "resolution_status", "reviewer_id", "resolution_notes"
    ]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = NAVY_HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28
    
    relationships = [
        (
            "REL-001", "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1", "IMPLEMENTS",
            "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1",
            "Rule preamble cites Section 15 of Assam Act No. IX of 2012 as statutory rulemaking power.",
            "NONE", "NO_CONFLICT", "Subordinate rules execute primary Act.",
            "RESOLVED_PROVISIONAL", "REV-LEGAL-01", "Subordinate relationship confirmed in text; both files have adultpdf.com producer flaw."
        ),
        (
            "REL-002", "DOC-AS-GMC-001", "VER-DOC-GMC-001-V1", "OPERATIONALIZES",
            "DOC-AS-ARTPS-002", "VER-DOC-ARTPS-002-V1",
            "Citizen Charter header explicitly invokes '(See Rule 5)' of the ARTPS Rules, 2012.",
            "CONF-002", "TEMPORAL_VINTAGE_CONFLICT",
            "Charter is dated 2013 (authored by omprakash); current 2026 applicability unverified against recent municipal amendments.",
            "UNRESOLVED_REQUIRES_HUMAN_AUDIT", "REV-LEGAL-01", "Officer must verify whether GMC has updated service fee or timeline schedules."
        ),
        (
            "REL-003", "DOC-AS-SCST-001", "VER-DOC-SCST-001-V2", "AMENDS_STATUTE",
            "DOC-AS-SCST-1978", "VER-DOC-SCST-001-V1",
            "Section 2 of Assam Act XXXI of 2024 expressly substitutes Section 4(b) of Assam Act XII of 1979.",
            "NONE", "NO_CONFLICT", "Express legislative substitution; new text prevails.",
            "RESOLVED_PROVISIONAL", "REV-LEGAL-01", "Active amendment verified in text; source is generic 'untitled_23.pdf'."
        ),
        (
            "REL-004", "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2", "AMENDS_REGULATION",
            "DOC-GOI-CADRE-1955", "VER-DOC-CADRE-001-V1",
            "Notification G.S.R. 78(E) amends Schedule item 'Assam' in IAS (Fixation of Cadre Strength) Regulations 1955.",
            "NONE", "NO_CONFLICT", "Central Government statutory amendment in consultation with State Government.",
            "RESOLVED_PROVISIONAL", "REV-LEGAL-01", "Active cadre regulation supersedes prior post counts. Physical scan."
        ),
        (
            "REL-005", "DOC-AS-PROC-001", "VER-DOC-PROC-001-V1", "CO_EXISTS_WITH_OVERRIDE",
            "DOC-GOI-PROC-001", "VER-DOC-MOF-001-V1",
            "Assam Public Procurement Rules 2020 apply to state procurements; Central MoF Manual applies to Central procurements.",
            "CONF-001", "JURISDICTIONAL_THRESHOLD_CONFLICT",
            "State rules permit QCBS for consultancy above state threshold; Central manual mandates GFR 2017 thresholds.",
            "RESOLVED_BY_JURISDICTION", "REV-LEGAL-01",
            "RAG engine must route state-funded procurements to DOC-AS-PROC-001 and central procurements to DOC-GOI-PROC-001."
        ),
        (
            "REL-006", "DOC-GOI-RTI-001", "VER-DOC-RTI-001-V1", "GOVERNS_PROACTIVE_DISCLOSURE",
            "DOC-GOI-CIC-001", "VER-DOC-CIC-001-V1",
            "Section 4(1)(b) proactive disclosure applies to Central Information Commission as a public authority.",
            "NONE", "NO_CONFLICT", "CIC is bound to publish vacancy circulars proactively under Section 4(1)(b).",
            "RESOLVED_PROVISIONAL", "REV-LEGAL-01", "Statutory alignment confirmed; CIC notice temporal validity expired."
        ),
        (
            "REL-007", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", "CONSTITUTIONAL_FOUNDATION",
            "DOC-GOI-CADRE-001", "VER-DOC-CADRE-001-V2",
            "Article 312 empowers Parliament to create All-India Services and regulate recruitment and conditions.",
            "NONE", "NO_CONFLICT", "Constitutional parentage of All India Services Act 1951.",
            "RESOLVED_PROVISIONAL", "REV-LEGAL-01", "Supreme constitutional authority."
        ),
        (
            "REL-008", "DOC-IND-CONST-001", "VER-DOC-CONST-001-V1", "CONSTITUTIONAL_FOUNDATION",
            "DOC-AS-ARTPS-001", "VER-DOC-ARTPS-001-V1",
            "Seventh Schedule, List II (State List), Entry 41 (State public services) provides state legislative competency.",
            "NONE", "NO_CONFLICT", "State legislative competence established.",
            "RESOLVED_PROVISIONAL", "REV-LEGAL-01", "Supreme constitutional authority."
        )
    ]
    
    for row_idx, rel in enumerate(relationships, 2):
        for col_idx, val in enumerate(rel, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)
            
    style_table(ws)

print("Updated data_sheets_6_9 with strict trust boundaries.")
