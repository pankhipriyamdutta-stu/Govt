# UNRESOLVED ISSUES & HUMAN INTERVENTION REPORT — NESFIC-D-36
**Project:** NESFIC-D-36 — Trusted Government Knowledge, Rules & Document Assistant  
**Challenge:** NESFIC 2026, Challenge Stream 1  
**Author:** Antigravity AI Pair Programmer & Domain Engineering Team  
**Date of Audit:** 2026-10-14  

---

## 1. Purpose & Human-in-the-Loop Protocol

In compliance with Section 4 and Section 7 of the Master Prompt ("Never Invent or Silently Alter Data" and "AI and RAG Readiness"), whenever evidence is incomplete, ambiguous, pending legislative notification, or involves cross-jurisdictional interpretation, the AI assistant **MUST ABSTAIN** or label the result **`VERIFICATION_REQUIRED`** rather than inferring facts.

This report catalogs all genuine evidentiary ambiguities, pending notifications, and required officer actions identified during the ingestion of the supplied government corpus.

---

## 2. Unresolved Issues Requiring Administrative Action

### Case 1: Post-2024 Amendments to the Assam Right to Public Services Framework
- **Evidentiary State:** The ingested corpus contains `DOC-AS-ARTPS-001` (Assam Act IX of 2012) and `DOC-AS-ARTPS-002` (ARTPS Rules, 2012). During 2024, the Assam Legislative Assembly passed the Assam Right to Public Services (Amendment) Act, 2024 (creating a state commission for public services).
- **Ambiguity / Gap:** The exact subordinate procedural rules under the 2024 commission structure are not present in the local downloads folder.
- **Current System Status:** `VERIFICATION_REQUIRED` for queries regarding appeals directly to the State Commission.
- **Required Human Action:** The Department Nodal Officer (AR&T Department) must confirm and ingest the subsequent Gazette notification notifying the date of commencement and appellate regulations under the 2024 amendment.

### Case 2: General / OBC Category Examination Fee Schedules in Assam
- **Evidentiary State:** `DOC-AS-SCST-001` (Assam Act No. XXXI of 2024) substitutes Section 4(b) of Assam Act XII of 1979 to mandate that examination fees are completely exempted for SC and ST candidates.
- **Ambiguity / Gap:** The statute does not prescribe the fee amounts payable by General, OBC, or MOBC candidates. These fee schedules are determined by individual departmental service rules and recruitment advertisements.
- **Current System Status:** `VERIFICATION_REQUIRED` for queries requesting General category application fee amounts.
- **Required Human Action:** Recruitment officers must attach specific departmental advertisement schedules when evaluating General candidate queries. The AI is strictly barred from guessing fee figures.

### Case 3: Jurisdictional Procurement Threshold Conflict (Assam State vs Central MoF)
- **Evidentiary State:** The dataset contains both `DOC-AS-PROC-001` (Assam Public Procurement Rules, 2020) and `DOC-GOI-PROC-001` (Central MoF Manual for Procurement of Consultancy Services, Updated June 2022).
- **Ambiguity / Gap:** In centrally sponsored schemes (CSS) implemented by Assam state departments, procurement officers often query whether Central GFR thresholds or State Public Procurement Rules apply.
- **Current System Status:** `VERIFICATION_REQUIRED_JURISDICTION`.
- **Required Human Action:** Legal and finance officers must examine the specific grant sanction order to ascertain whether the funding agreement mandates adherence to Central GFR or permits execution under Assam State Public Procurement Rules 2020.

### Case 4: Proportionate Penalty Apportionment Under ARTPS Section 9(3)
- **Evidentiary State:** Section 9(3) of the ARTPS Act 2012 provides that penalties may be deducted from the Designated Public Servant, Appellate Authority, and subordinate staff in proportion to their fault.
- **Ambiguity / Gap:** The exact mathematical formula for apportioning liability between supervisory officers and clerical staff is not defined by statute, but left to quasi-judicial enquiry.
- **Current System Status:** `HUMAN_REVIEW_MANDATORY`.
- **Required Human Action:** Departmental disciplinary authorities must conduct formal enquiry hearings. The AI system will display the maximum penalty (Rs 25,000 / Rs 250 per day) but will abstain from deciding employee liability.

### Case 5: 2026 IAS Cadre Revision Notification Ingestion
- **Evidentiary State:** The latest cadre regulation in the repository is `DOC-GOI-CADRE-001` (Second Amendment Regulations, 2025, published 27th January 2025).
- **Ambiguity / Gap:** Users querying 2026 cadre allocations cannot receive an answer because no 2026 notification has been issued by DoPT.
- **Current System Status:** `CANNOT_GENERATE` (Non-existent future enactment).
- **Required Human Action:** System administrator must set up periodic ingestion from `dopt.gov.in` to capture subsequent cadre amendment regulations when published in the Gazette of India.

---

## 3. Quarantined Artifacts & Data Retention Protocol

| Identifier | Source Filename | Current Disposition | Administrative Recommendation |
| :--- | :--- | :--- | :--- |
| **`EXC-ID-001`** | `Identity Card.pdf` | Quarantined (`EXCLUDED_PII`) | Permanently purge from shared workstation; confirm no citizen PII is indexed. |
| **`EXC-DOC-001`** | `19,20,23,24.docx` | Quarantined (`EXCLUDED_SCRATCH`) | Delete zero-byte scratch file. |
| **`EXC-DOC-002`** | `Doc5.docx` | Quarantined (`EXCLUDED_SCRATCH`) | Delete layout scratch file. |
| **`EXC-DOC-003`** | `Doc8.docx` | Quarantined (`EXCLUDED_SCRATCH`) | Delete layout scratch file. |

---

## 4. Summary

All 5 unresolved issues represent legitimate legal boundaries and temporal constraints. By explicitly registering these limitations in Sheet 12 (`Abstention and Human Verification`) and Sheet 16 (`Data Quality Log`), the dataset guarantees that the AI assistant acts with strict legal integrity, avoiding false answers and prioritizing official human review.
