# DEPLOYMENT GUIDE & OPERATIONAL RUNBOOK
## NESFIC-D-36: Trusted Government Knowledge, Rules & Document Assistant

**Project Identifier:** NESFIC-D-36  
**Challenge:** NESFIC 2026, Challenge Stream 1  
**Classification:** Restricted / Government Decision-Support Platform  

---

### 1. System Requirements & Runtime Prerequisites

- **Python Runtime:** Python 3.11+
- **Node.js Runtime:** Node.js v20+ / v24+ with npm
- **Database:** PostgreSQL 15+ (Production) or SQLite 3.38+ (Local Development & Self-Contained Pilot)
- **Containerization (Optional):** Docker 24+ & Docker Compose v2+
- **Memory & Storage:** 4 GB RAM minimum (8 GB recommended for OCR workloads), 10 GB disk space for document vault and gazette archives.

---

### 2. Local Development Setup (Windows / Linux / macOS)

#### A. Backend Setup
1. Navigate to the repository root:
   ```bash
   cd /path/to/Govt
   ```
2. Verify Python 3.11 is available:
   ```bash
   python --version
   ```
3. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Initialize database and seed the 19 master government CSV sheets:
   ```bash
   python backend/test_init.py
   ```
5. Run the automated test suite (Unit, Integration, Crypto, and Red-Team):
   ```bash
   pytest backend/tests -v
   ```
6. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
   ```

#### B. Frontend Setup
1. In a separate terminal, navigate to `frontend/`:
   ```bash
   cd frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Run production build test:
   ```bash
   npm run build
   ```
4. Start the Vite development server:
   ```bash
   npm run dev -- --host 127.0.0.1 --port 5173
   ```
5. Open your browser at `http://127.0.0.1:5173`.

---

### 3. Docker Compose Deployment (Single-Command Production Stack)

To run the complete production containerized stack:

```bash
docker-compose up --build -d
```

- **Frontend:** Accessible at `http://localhost:5173`
- **Backend API:** Accessible at `http://localhost:8000/api/v1`
- **Interactive OpenAPI Documentation:** `http://localhost:8000/docs`

To inspect container health:
```bash
docker-compose ps
docker-compose logs -f backend
```

---

### 4. Database Backup & Disaster Recovery Procedures

#### A. Backup
For SQLite (Pilot / Air-Gapped Mode):
```bash
# Atomic snapshot using sqlite3 backup API or copy with lock
sqlite3 backend_gov.db ".backup 'backups/backend_gov_backup_$(date +%Y%m%d_%H%M%S).db'"
```

For PostgreSQL (Enterprise Deployment):
```bash
pg_dump -h localhost -U nesfic_admin -d nesfic_db -F c -b -v -f "backups/nesfic_pg_$(date +%Y%m%d_%H%M%S).dump"
```

#### B. Restoration
```bash
# SQLite Restoration:
cp backups/backend_gov_backup_TIMESTAMP.db backend_gov.db

# PostgreSQL Restoration:
pg_restore -h localhost -U nesfic_admin -d nesfic_db -v "backups/nesfic_pg_TIMESTAMP.dump"
```

---

### 5. RBAC Default Demonstration Accounts

The system is pre-seeded with 6 role-based government identities. Use the role switcher in the top navigation bar or authenticate with:
- **Default Demonstration Password:** `GovtSecure@2026`

| Username | Role Identifier | Role Title | Department Jurisdiction | Permitted Operations |
| :--- | :--- | :--- | :--- | :--- |
| `citizen_user` | `ROL-001` | Citizen / Public User | Public Portal Scope | Query public citizen charters, timelines, fee rules. |
| `officer_sharma` | `ROL-002` | Department Official (DPS) | Finance Department | Departmental rule lookup, draft Form-2 acknowledgements. |
| `reviewer_baruah`| `ROL-003` | Verification Officer | Legislative Department | Audit scanned gazettes, inspect signatures, approve/reject. |
| `legal_gogoi` | `ROL-004` | Legal & Appellate Reviewer | Legislative Department | Map amendment lineages, statutory conflict resolution. |
| `admin_kalita` | `ROL-005` | Department Administrator | Administrative Reforms | Ingest circulars, update charter schedules, view metrics. |
| `auditor_das` | `ROL-006` | System Security Auditor | Audit & Vigilance | Inspect tamper-evident audit logs, review red-team alerts. |

---

### 6. Operational Verification Runbook

1. **Ingesting a New Document:**
   - Authorized officials submit PDFs via `Document Repository` -> `Ingest New Document`.
   - The file is automatically SHA-256 hashed and routed to `/quarantine`.
   - Status is set to `PENDING_VERIFICATION`. It does **NOT** enter search retrieval.
2. **Verification Officer Certification:**
   - Verification Officer (`reviewer_baruah`) navigates to `Admin & Control` -> `Verification Queue`.
   - Inspects metadata anomalies (e.g., third-party web converter flags).
   - Enters mandatory legal rationale and selects `APPROVE AS TRUSTED` or `REJECT`.
3. **Auditing AI Answers in Source Detective:**
   - Any official or citizen can click `Inspect Evidence in Source Detective` on any Co-Pilot answer.
   - Inspect the verbatim statute text, Section locator, printed page number, file SHA-256 hash, and signer institutional authority.
