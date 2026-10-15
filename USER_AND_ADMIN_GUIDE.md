# USER & ADMINISTRATOR GUIDE
## NESFIC-D-36: Trusted Government Knowledge, Rules & Document Assistant

**Project Identifier:** NESFIC-D-36  
**Challenge:** NESFIC 2026, Challenge Stream 1  
**Target Audience:** Assam Government Officials, Verification Officers, Legal Reviewers, and Department Administrators  

---

### Part 1: Government Official User Guide

#### 1. Navigating the Command Centre
- **Overview:** The Command Centre is your operational homepage. It displays your current department, active state statutes in the pilot repository, trust status health, and pending verification alerts.
- **Quick Rule Query:** Use the central search bar on the homepage or click **"Launch AI Co-Pilot"** to start exploring government rules.

#### 2. Using the AI Co-Pilot
The AI Co-Pilot is designed specifically for statutory inquiry and grounded drafting.

##### Tripartite Response Meaning
Every answer from the Co-Pilot displays a prominent color-coded badge:
- 🟢 **VERIFIED (Green):** The answer is 100% grounded in an active primary statute or gazette. You can legally rely on this provision.
- 🟡 **VERIFICATION REQUIRED (Amber):** Pertinent evidence was located, but temporal validity (e.g. vintage 2013 charter) or third-party file metadata requires human officer confirmation before formal enforcement.
- 🔴 **CANNOT GENERATE VERIFIED ANSWER (Red):** The requested gazette does not exist, the circular is expired, the file is quarantined PII, or the question invites speculation. The system abstains rather than inventing answers.

##### Inspecting Citations & Evidence
- Below every answer, review the **Atomic Claims Grounding Ledger** and **Primary Statutory Citations**.
- Click **"Inspect Evidence in Source Detective"** to inspect the 360-degree forensic lineage of that exact rule.

##### Specialized Decision Support Tools
- **Document Summarisation:** Select any statute to generate a source-constrained legal summary.
- **Statutory Version Comparison:** Compare two enactments (e.g., State Procurement Rules 2020 vs Central GFR 2017) to determine legal precedence.
- **Bilingual Translation (English ↔ Assamese):** Translate legal excerpts into Assamese with preserved rule numbers and statutory caveats.
- **Grounded Drafting:** Generate departmental Office Notes or Form-2 acknowledgements grounded strictly in verified evidence.

---

### Part 2: Verification Officer Guide (`reviewer_baruah` / `ROL-003`)

#### 1. Accessing the Verification Queue
1. Log in or select **Dr. Mridul Baruah, Verification Officer** from the top right role switcher.
2. Navigate to **Admin & Control** -> **Verification Queue**.
3. View pending documents flagged during automated ingestion (e.g., files with `adultpdf.com` or `ilovepdf.com` converter metadata).

#### 2. Auditing & Recording a Decision
1. Click **"Audit & Decide"** on any queue item.
2. Review the document title, issuing authority, and cryptographic anomaly notes.
3. Select your authoritative decision:
   - `APPROVE AS TRUSTED PRIMARY STATUTE`
   - `REJECT (UNTRUSTED THIRD-PARTY TOOL)`
   - `FLAG FOR SECONDARY LEGAL REVIEW`
4. Enter your mandatory **Authoritative Rationale** (e.g. *"Text verified against Assam Gazette Extraordinary No. 194"*).
5. Click **"Commit Official Decision"**. The decision is logged immutably into the audit chain.

---

### Part 3: System Security Auditor Guide (`auditor_das` / `ROL-006`)

#### 1. Inspecting the Tamper-Evident Audit Ledger
1. Select **Himanta Das, System Security Auditor** from the role switcher.
2. Navigate to **Trust & Security Centre**.
3. Check the **Audit Chain Cryptographic Status**:
   - `MATHEMATICALLY INTACT`: Verifies that every query audit log's `previous_hash` matches the preceding block's SHA-256 tamper hash.
4. Review the chronological audit log entries showing exact query text, response status, model used, and latency.

#### 2. Reviewing Red-Team Incident Alerts
- Inspect blocked adversarial attacks under **Active Security Incident Alerts**:
  - Prompt injection overrides
  - Quarantined PII extraction attempts
  - Oral WhatsApp order spoofing
  - Cross-jurisdiction procurement poisoning attempts.
