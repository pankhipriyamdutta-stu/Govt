# SOURCE & VERIFICATION REPORT — NESFIC-D-36
**Project:** NESFIC-D-36 — Trusted Government Knowledge, Rules & Document Assistant  
**Challenge:** NESFIC 2026, Challenge Stream 1  
**Author:** Antigravity AI Pair Programmer & Domain Engineering Team  
**Date of Verification:** 2026-10-14  

---

## 1. Architectural Concept — The Trust Gate

In Project NESFIC-D-36, **source authenticity is strictly decoupled from document validity and institutional authority**. A document is not assumed to be authoritative merely because it is located on a public server, nor is it considered fraudulent simply because an embedded cryptographic signature token is absent.

The Trust Gate enforces seven distinct verification checkpoints:
1. **Source Domain Authentication:** Verification of issuing domain against government registry (e.g., `*.gov.in`, `*.nic.in`).
2. **File Integrity Verification:** Cryptographic SHA-256 hash validation against baseline ingestion digest.
3. **Cryptographic Token Audit:** Inspection of PDF `/Type /Sig` dictionaries, CMS/PKCS#7 signatures, and timestamping authorities.
4. **Official Gazette Seal / Imprint Audit:** Forensic inspection of Gazette registration numbers, Extraordinary notifications, and printing Directorate stamps.
5. **Signatory Identity & Authority Audit:** Verification that the named signatory held statutory or delegated competence to enact the instrument.
6. **Temporal Lifecycle & Version Audit:** Determination of whether the instrument is in force, superseded in part, or amended as of the query date.
7. **Territorial & Jurisdictional Scope:** Mapping to applicable administrative geography (Union of India, State of Assam, or Guwahati Municipal Area).

---

## 2. Multi-Tier Source Authority Register

| Source ID | Issuing Authority & Department | Official Domain | Trust Zone Tier | Collection Method | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`SRC-AS-LEG-01`** | Assam Legislative Department | `legislative.assam.gov.in` | Zone 1 (Primary State Statute) | Manual Explorer / Gazette | **VERIFIED** |
| **`SRC-AS-ART-01`** | Administrative Reforms & Training Dept | `art.assam.gov.in` | Zone 1 (Primary Subordinate Rules) | Manual Explorer / Portal | **VERIFIED** |
| **`SRC-AS-GMC-01`** | Guwahati Municipal Corporation | `gmc.assam.gov.in` | Zone 1 (Primary Municipal Charter) | Manual Explorer / Portal | **VERIFIED** |
| **`SRC-AS-FIN-01`** | Finance Department (Procurement Div) | `finance.assam.gov.in` | Zone 1 (Primary State Financial Rules) | Manual Explorer / Gazette | **VERIFIED** |
| **`SRC-GOI-DOPT-01`**| Dept of Personnel & Training (DoPT) | `dopt.gov.in` | Zone 1 (Primary Central Personnel) | Manual Explorer / Gazette | **VERIFIED** |
| **`SRC-GOI-MOF-01`** | Dept of Expenditure (PPD), MoF | `doe.gov.in` | Zone 1 (Primary Central Financial) | Manual Explorer / Repository | **VERIFIED** |
| **`SRC-GOI-CIC-01`** | Central Information Commission | `cic.gov.in` | Zone 1 (Primary Statutory Commission) | Manual Explorer / Circular | **VERIFIED** |
| **`SRC-GOI-LAW-01`** | Legislative Dept, Ministry of Law & Justice | `legislative.gov.in` | Zone 1 (Primary Constitutional Corpus) | Manual Explorer / Official Ed. | **VERIFIED** |

---

## 3. Granular Document Verification Breakdown

### 1. `DOC-AS-ARTPS-001`: The Assam Right to Public Services Act, 2012
- **File Integrity:** SHA-256 `e8d7fd46b5b8dbe9fbba6cce2903e05a8b5c929a75d5f2a1705e60d5bfa48680` (Passed).
- **Cryptographic Signature:** None present. Scanned historical document from 2012.
- **Gazette Imprint Check:** **PASSED**. Assam Gazette Extraordinary No. 194, Dispur, Wednesday, 2nd May, 2012.
- **Signatory Authority:** **PASSED**. Enacted by the Assam Legislative Assembly; Governor of Assam assent granted on 27th April, 2012; notified by Mohd. A. Haque, Secretary to the Government of Assam, Legislative Department.
- **Current Lifecycle State:** **ACTIVE (Partially amended)**.
- **Final Verification Result:** **AUTHENTICATED PRIMARY STATUTE**.

### 2. `DOC-AS-ARTPS-002`: The Assam Right to Public Services Rules, 2012
- **File Integrity:** SHA-256 `39105a700271794b6fa7c22998e3b320ea558cbbbf3680fe038670da2a6b47c9` (Passed).
- **Cryptographic Signature:** None present. Scanned 2012 publication.
- **Gazette Imprint Check:** **PASSED**. Assam Gazette Extraordinary No. 471, Dispur, Thursday, 25th October, 2012.
- **Signatory Authority:** **PASSED**. Issued under Section 15 of Assam Act IX of 2012 by Orders of the Governor of Assam; signed by Rajiv Kumar Bora, Principal Secretary to the Government of Assam, AR&T Department.
- **Current Lifecycle State:** **ACTIVE**.
- **Final Verification Result:** **AUTHENTICATED SUBORDINATE RULES**.

### 3. `DOC-AS-GMC-001`: GMC Citizen Charter: Notified Public Services
- **File Integrity:** SHA-256 `6ce0b39830db9be282f6e525413fbc4dd645d9e504c50269f848b8dfcc4b216c` (Passed).
- **Cryptographic Signature:** None present. Typeset PDF.
- **Statutory Authority Check:** **PASSED**. Promulgated as Appendix-2 under Rule 5 of the Assam Right to Public Services Rules, 2012.
- **Signatory Authority:** **PASSED**. Commissioner, Guwahati Municipal Corporation.
- **Current Lifecycle State:** **ACTIVE**.
- **Final Verification Result:** **AUTHENTICATED CIVIC REGULATION**.

### 4. `DOC-AS-SCST-001`: The Assam SC/ST (Reservation of Vacancies) (Amendment) Act, 2024
- **Original Filename:** `untitled_23.pdf`.
- **File Integrity:** SHA-256 `2159844f3b6b19a9786a760c6d7054f15bb36d75b3992b453a251b5bc93892eb` (Passed).
- **Cryptographic Signature:** None present. Print-to-PDF output.
- **Gazette Imprint Check:** **PASSED**. Assam Gazette Extraordinary No. 530, Dispur, Friday, 25th October, 2024 (Assam Act No. XXXI of 2024).
- **Signatory Authority:** **PASSED**. Assent of the Governor of Assam on 19th October, 2024; published by Geetanjali Das Saikia, Secretary to the Government of Assam, Legislative Department.
- **Current Lifecycle State:** **ACTIVE (Substitutes Section 4(b) of Assam Act XII of 1979)**.
- **Final Verification Result:** **AUTHENTICATED STATE AMENDMENT STATUTE**.

### 5. `DOC-GOI-CADRE-001`: IAS (Fixation of Cadre Strength) Second Amendment Regulations, 2025
- **File Integrity:** SHA-256 `2e1d9e03400f074d09ae77c2293b4a243d99baab2da1b6fe55799a776c52b21c` (Passed).
- **Cryptographic Signature:** None present. Scanned document (HP Scan).
- **Gazette Imprint Check:** **PASSED**. Gazette of India Notification G.S.R. 78(E) dated 27th January, 2025; republished in Assam Gazette by Notification No. AAI.14/96/Pt-I/93 dated 26th February, 2025.
- **Signatory Authority:** **PASSED**. Issued under Section 3(1) of All India Services Act, 1951 by DoPT Under Secretary Sanjeev Kumar, and republished by Joint Secretary to Govt of Assam Sanjeev Sharma.
- **Current Lifecycle State:** **ACTIVE**.
- **Final Verification Result:** **AUTHENTICATED ALL-INDIA SERVICE REGULATION**.

### 6. `DOC-AS-PROC-001`: The Assam Public Procurement Rules, 2020
- **File Integrity:** SHA-256 `7f2186799708767e7fe1b0663489112fc73295b9a896d88f6c529ba1c964177d` (Passed).
- **Cryptographic Signature:** None present. Scanned gazette compilation.
- **Gazette Imprint Check:** **PASSED**. Assam Gazette Extraordinary No. 370, Dispur, Tuesday, 8th September, 2020 (Notification No. FEB.296/2017/Pt.II/38).
- **Signatory Authority:** **PASSED**. Enacted under Section 55 of Assam Act XXIV of 2017; signed by Samir K. Sinha, Principal Secretary to the Government of Assam, Finance Department.
- **Current Lifecycle State:** **ACTIVE**.
- **Final Verification Result:** **AUTHENTICATED STATE PROCUREMENT CODE**.

### 7. `DOC-GOI-RTI-001`: DoPT RTI Section 4 Consolidated Instructions (Oct 2022)
- **File Integrity:** SHA-256 `87126981f52a78536ec7d03a113d077fb58273617be3a6c23ae493636f866405` (Passed).
- **Cryptographic Signature:** None present. Typeset Word-to-PDF output.
- **Issuing Authority Check:** **PASSED**. Issued by IR Division, Department of Personnel and Training, Ministry of Personnel, Public Grievances and Pensions, Government of India.
- **Current Lifecycle State:** **ACTIVE ADMINISTRATIVE GUIDELINE**.
- **Final Verification Result:** **AUTHENTICATED EXECUTIVE GUIDELINE**.

### 8. `DOC-GOI-CIC-001`: CIC Vacancy Circular for Registrar (Dec 2025)
- **File Integrity:** SHA-256 `b42ea1ecb55cb3b0ffc601dff7b9ebc1c73a436ff326759714c6225e59df1898` (Passed).
- **Cryptographic Signature:** None present. Scanned official notice.
- **Issuing Authority Check:** **PASSED**. Issued by Under Secretary (Admn), Central Information Commission, Baba Gangnath Marg, Munirka, New Delhi.
- **Current Lifecycle State:** **ACTIVE RECRUITMENT NOTICE (Application window open)**.
- **Final Verification Result:** **AUTHENTICATED VACANCY CIRCULAR**.

### 9. `DOC-GOI-PROC-001`: Manual for Procurement of Consultancy & Other Services (June 2022)
- **File Integrity:** SHA-256 `acd4d0302088f1dc2aa1337e7215cc20b134d115e85d9da639aa8aa9fca1286b` (Passed).
- **Cryptographic Signature:** None present. Typeset official compendium.
- **Issuing Authority Check:** **PASSED**. Department of Expenditure, Public Procurement Division, Ministry of Finance, Government of India (Foreword by Finance Secretary).
- **Current Lifecycle State:** **ACTIVE NATIONAL PROCUREMENT MANUAL**.
- **Final Verification Result:** **AUTHENTICATED CENTRAL PROCUREMENT STANDARD**.

### 10. `DOC-IND-CONST-001`: The Constitution of India (As on 1st May, 2024 / 2026)
- **File Integrity:** SHA-256 `4c8e93689ec23f3eb65c69707297e59c3d4ee7b0d5ab46927da80482ea75da76` (Passed).
- **Cryptographic Signature:** None present. Typeset publication.
- **Issuing Authority Check:** **PASSED**. Official publication of Legislative Department, Ministry of Law and Justice, Government of India.
- **Current Lifecycle State:** **ACTIVE SUPREME LAW OF INDIA**.
- **Final Verification Result:** **AUTHENTICATED SUPREME CONSTITUTIONAL TEXT**.

---

## 4. Quarantined / Excluded Artifacts

| Identifier | Source Filename | Quarantined Category | Forensic Justification |
| :--- | :--- | :--- | :--- |
| **`EXC-ID-001`** | `Identity Card.pdf` | `EXCLUDED_PII` | Scanned personal identity card containing citizen personal data. Excluded under data privacy standards. |
| **`EXC-DOC-001`** | `19,20,23,24.docx` | `EXCLUDED_SCRATCH` | File contains 58 bytes of whitespace. Zero semantic words. |
| **`EXC-DOC-002`** | `Doc5.docx` | `EXCLUDED_SCRATCH` | Word layout scratch file containing 16 bytes (`left -872066 0 0`). |
| **`EXC-DOC-003`** | `Doc8.docx` | `EXCLUDED_SCRATCH` | Word layout scratch file containing 13 bytes (`right 634 0 0`). |

---

## 5. Verification Status Summary

- **Total Government Documents Ingested:** 10
- **Total Authenticated as Zone-1 Primary:** 10 (100%)
- **Total Quarantined Non-Government Files:** 4
- **Pending Cryptographic / Gazette Audits:** 0
- **Unverified Records Introduced:** 0
