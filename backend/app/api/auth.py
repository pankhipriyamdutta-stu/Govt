from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models.user import User, Role, Department
from app.services.auth_service import authenticate_user, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication & Identity"])

class LoginRequest(BaseModel):
    username: str
    password: str

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    department_name: str
    department_code: str
    role_id: str
    role_name: str
    permitted_action: str
    mfa_enabled: bool

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        # Default to demo officer if unauthenticated for smooth inspection
        user = db.query(User).filter(User.username == "officer_sharma").first()
        if user:
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid signature")
    
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    token = create_access_token({"sub": user.username, "role": user.role.role_id if user.role else "ROL-001"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "department": user.department.name if user.department else "Public Scope",
            "department_code": user.department.code if user.department else "PUB",
            "role_id": user.role.role_id if user.role else "ROL-001",
            "role_name": user.role.role_name if user.role else "Public User",
            "permitted_action": user.role.permitted_action if user.role else "Read Public Charters"
        }
    }

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "department": current_user.department.name if current_user.department else "Public Scope",
        "department_code": current_user.department.code if current_user.department else "PUB",
        "role_id": current_user.role.role_id if current_user.role else "ROL-001",
        "role_name": current_user.role.role_name if current_user.role else "Public User",
        "permitted_action": current_user.role.permitted_action if current_user.role else "Read Public Charters",
        "mfa_enabled": current_user.mfa_enabled
    }

@router.get("/demo-users")
def list_demo_users(db: Session = Depends(get_db)):
    """Returns available demonstration user accounts across all 6 government roles."""
    users = db.query(User).all()
    return [
        {
            "username": u.username,
            "full_name": u.full_name,
            "role_id": u.role.role_id if u.role else "",
            "role_name": u.role.role_name if u.role else "",
            "department": u.department.name if u.department else ""
        }
        for u in users
    ]
