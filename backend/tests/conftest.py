import sys
import os
import pytest

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import SessionLocal, Base, engine
from app.services.seed_service import seed_database

@pytest.fixture(scope="session")
def db_session():
    # Make sure db is seeded
    db = SessionLocal()
    seed_database(db)
    yield db
    db.close()
