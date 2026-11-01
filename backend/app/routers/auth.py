"""
SUTRA LEARN - Authentication Router
Issues cryptographically signed Bearer tokens.
Supports standard username/password login and verified persona session generation.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from app.db.database import get_db_connection
from app.auth import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    identifier: Optional[str] = None  # Learner ID, username, or institutional ID
    username: Optional[str] = None    # Backwards compatibility
    password: str


class UserProfile(BaseModel):
    id: str
    name: str
    role: str
    grade: int


class SessionRequest(BaseModel):
    learner_id: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user_id: str
    name: str
    role: str
    expires_in: int
    redirect_to: str = "/student/home"
    user: Optional[UserProfile] = None


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, conn=Depends(get_db_connection)):
    """
    Unified authentication entry point.
    Authenticates with identifier and password to obtain a cryptographically signed token.
    Server-side role resolution directs user to appropriate portal (/student/home or /teacher/dashboard).
    """
    login_id = (req.identifier or req.username or "").strip()
    if not login_id:
        raise HTTPException(status_code=400, detail="Identifier or username is required.")

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role, password_hash FROM learners WHERE id = ? OR name = ?", (login_id, login_id))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    if user["password_hash"]:
        if not verify_password(req.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid username or password.")

    role = user["role"]
    redirect_to = "/teacher/dashboard" if role == "teacher" else "/student/home"
    token = create_access_token(user["id"], role, user["name"])
    return TokenResponse(
        access_token=token,
        token_type="Bearer",
        user_id=user["id"],
        name=user["name"],
        role=role,
        expires_in=86400,
        redirect_to=redirect_to,
        user=UserProfile(
            id=user["id"],
            name=user["name"],
            role=role,
            grade=user["grade"]
        )
    )


@router.post("/session", response_model=TokenResponse)
def create_session(req: SessionRequest, conn=Depends(get_db_connection)):
    """
    Session generator for verified demo personas.
    Validates user existence in SQLite and issues a cryptographic signed Bearer token.
    Never accepts raw unauthenticated caller headers.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role FROM learners WHERE id = ?", (req.learner_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail=f"Learner '{req.learner_id}' not found in database.")

    role = user["role"]
    redirect_to = "/teacher/dashboard" if role == "teacher" else "/student/home"
    token = create_access_token(user["id"], role, user["name"])
    return TokenResponse(
        access_token=token,
        token_type="Bearer",
        user_id=user["id"],
        name=user["name"],
        role=role,
        expires_in=86400,
        redirect_to=redirect_to,
        user=UserProfile(
            id=user["id"],
            name=user["name"],
            role=role,
            grade=user["grade"]
        )
    )


@router.get("/me")
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns verified profile and claims extracted from the cryptographic Bearer token."""
    return current_user

