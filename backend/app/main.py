from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.config import settings
from app.database import engine, Base, SessionLocal, get_db
from app.services.seed_service import seed_database
from app.services.security_middleware import SovereignSecurityHeadersMiddleware
from app.api.auth import router as auth_router
from app.api.documents import router as doc_router
from app.api.copilot import router as copilot_router
from app.api.evidence import router as evidence_router
from app.api.verification import router as verification_router
from app.api.admin import router as admin_router
from app.api.security import router as security_router
from app.api.veritrace import router as veritrace_router

from app.services.seed_veritrace import seed_sample_veritrace_documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed master government data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        seed_sample_veritrace_documents(db)
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0-SOVEREIGN",
    description="Sovereign Government Knowledge, Rules & Document Security Platform for authorized officials in Assam and Northeast India. Enforces Indian IT Act 2000, Section 70B CERT-In directions, and DPDP Act 2023.",
    lifespan=lifespan
)

# 1. Sovereign Security Headers & Rate-Limiting Defense Middleware
app.add_middleware(SovereignSecurityHeadersMiddleware)

# 2. Hardened CORS configuration (GIGW 3.0 & CERT-In Compliant)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["Retry-After", "X-Govt-Security-Zone", "X-Audit-Compliance"]
)

# 3. Register Domain Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(security_router, prefix=settings.API_V1_STR)
app.include_router(doc_router, prefix=settings.API_V1_STR)
app.include_router(copilot_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(verification_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(veritrace_router, prefix=settings.API_V1_STR)

# Health & Sovereign Security Diagnostic Endpoints
@app.get("/api/v1/health")
def health():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT_NAME,
        "zero_trust_active": settings.STRICT_ZERO_TRUST,
        "cert_in_compliant": True,
        "dpdp_act_compliant": True,
        "trust_gate_active": True
    }

@app.get("/api/v1/health/liveness")
def liveness():
    return {"status": "LIVE", "security_zone": "SOVEREIGN_SECURE"}

@app.get("/api/v1/health/readiness")
def readiness(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute(Base.metadata.tables["documents"].select().limit(1))
        return {
            "status": "READY",
            "database": "CONNECTED",
            "repository_state": "SOVEREIGN_ENCLAVE_ACTIVE",
            "cca_trust_engine": "ACTIVE"
        }
    except Exception as e:
        return {"status": "UNREADY", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
