from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.config import settings
from app.database import engine, Base, SessionLocal, get_db
from app.services.seed_service import seed_database
from app.api.auth import router as auth_router
from app.api.documents import router as doc_router
from app.api.copilot import router as copilot_router
from app.api.evidence import router as evidence_router
from app.api.verification import router as verification_router
from app.api.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed master government data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="NESFIC-D-36: Trusted Government Knowledge, Rules & Document Assistant for authorized officials in Assam and Northeast India.",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Domain Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(doc_router, prefix=settings.API_V1_STR)
app.include_router(copilot_router, prefix=settings.API_V1_STR)
app.include_router(evidence_router, prefix=settings.API_V1_STR)
app.include_router(verification_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

# Health & Diagnostic Endpoints
@app.get("/api/v1/health")
def health():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT_NAME,
        "demo_mode": settings.DEMO_MODE,
        "trust_gate_active": True
    }

@app.get("/api/v1/health/liveness")
def liveness():
    return {"status": "LIVE"}

@app.get("/api/v1/health/readiness")
def readiness(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute(Base.metadata.tables["documents"].select().limit(1))
        return {
            "status": "READY",
            "database": "CONNECTED",
            "repository_state": "ACTIVE_PILOT"
        }
    except Exception as e:
        return {"status": "UNREADY", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
