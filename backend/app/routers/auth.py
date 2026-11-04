"""
SUTRA LEARN - Authentication Router
Issues cryptographically signed Bearer tokens.
Supports standard username/password login and verified persona session generation.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.database import get_db_connection
from app.auth import verify_password, create_access_token, get_current_user
from app.auth_rate_limit import login_rate_limiter, get_client_ip
from app.services.audit import record_audit_event, AuditCategory

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
    learner_id: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    demo_mode: Optional[bool] = True


DEMO_PERSONAS = {"student-01", "student-02", "student-03", "teacher-01"}


class TokenResponse(BaseModel):
    access_token: str
    token: Optional[str] = None  # Backwards compatibility alias
    token_type: str = "Bearer"
    user_id: str
    name: str
    role: str
    expires_in: int
    redirect_to: str = "/student/home"
    user: Optional[UserProfile] = None


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, request: Request, conn=Depends(get_db_connection)):
    """
    Unified authentication entry point.
    Authenticates with identifier and password to obtain a cryptographically signed token.
    Server-side role resolution directs user to appropriate portal (/student/home or /teacher/dashboard).
    Protected by in-memory sliding window rate limiter against brute-force attacks.
    """
    ip = get_client_ip(request)
    login_rate_limiter.check_rate_limit(f"login_{ip}")

    login_id = (req.identifier or req.username or "").strip()
    if not login_id:
        raise HTTPException(status_code=400, detail="Identifier or username is required.")

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role, password_hash FROM learners WHERE id = ? OR name = ?", (login_id, login_id))
    user = cursor.fetchone()

    corr_id = getattr(request.state, "correlation_id", None) if hasattr(request, "state") else None

    if not user:
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.SECURITY,
            actor_id=login_id,
            outcome="REJECTED",
            rationale="User not found during login",
            correlation_id=corr_id,
            details={"ip": ip, "login_id": login_id}
        )
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    if not user["password_hash"]:
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.SECURITY,
            actor_id=user["id"],
            outcome="REJECTED",
            rationale="Unconfigured password hash rejected",
            correlation_id=corr_id,
            details={"ip": ip}
        )
        raise HTTPException(status_code=401, detail="Authentication failed: Account has no password configured.")

    if not verify_password(req.password, user["password_hash"]):
        record_audit_event(
            conn=conn,
            event_category=AuditCategory.SECURITY,
            actor_id=user["id"],
            outcome="REJECTED",
            rationale="Invalid password attempt",
            correlation_id=corr_id,
            details={"ip": ip}
        )
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    role = user["role"]
    redirect_to = "/teacher/dashboard" if role == "teacher" else "/student/home"
    token = create_access_token(user["id"], role, user["name"])

    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=user["id"],
        actor_role=role,
        learner_id=user["id"],
        outcome="RECORDED",
        rationale="Successful password authentication",
        correlation_id=corr_id,
        details={"ip": ip, "role": role}
    )

    return TokenResponse(
        access_token=token,
        token=token,
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
    Hardened session generator restricted exclusively to verified demo personas.
    Rejects arbitrary or unverified learner accounts to prevent identity spoofing.
    Validates password when supplied, and logs all issuances to system_audit_logs.
    """
    clean_id = (req.learner_id or req.user_id or "").strip()
    if not clean_id:
        raise HTTPException(status_code=400, detail="learner_id or user_id is required.")

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role, password_hash FROM learners WHERE id = ?", (clean_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail=f"Demo learner '{clean_id}' not found in database.")

    if clean_id not in DEMO_PERSONAS:
        raise HTTPException(
            status_code=403,
            detail=f"Persona '{clean_id}' is not an authorized demo persona. Use POST /api/v1/auth/login with verified credentials."
        )

    # If a password was provided, verify it strictly
    if req.password:
        if user["password_hash"] and not verify_password(req.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid password for demo persona.")

    # Record security audit log entry
    try:
        import uuid
        cursor.execute(
            """
            INSERT INTO system_audit_logs (
                id, event_category, actor_id, actor_role, learner_id,
                outcome, rationale, details
            ) VALUES (?, 'SUCCESSFUL_AUTHORIZED_ACTIONS', ?, ?, ?, 'RECORDED', 'Demo session token issued', 'Audited demo fast-access')
            """,
            (f"log_{uuid.uuid4().hex[:12]}", clean_id, user["role"], clean_id)
        )
        conn.commit()
    except Exception:
        pass

    role = user["role"]
    redirect_to = "/teacher/dashboard" if role == "teacher" else "/student/home"
    token = create_access_token(user["id"], role, user["name"])
    return TokenResponse(
        access_token=token,
        token=token,
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


@router.post("/logout")
def logout(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    conn=Depends(get_db_connection)
):
    """
    Terminates client session and records an audited logout event.
    """
    corr_id = getattr(request.state, "correlation_id", None) if hasattr(request, "state") else None
    record_audit_event(
        conn=conn,
        event_category=AuditCategory.AUTHORIZED,
        actor_id=current_user["id"],
        actor_role=current_user.get("role"),
        learner_id=current_user["id"],
        outcome="RECORDED",
        rationale="User initiated session logout",
        correlation_id=corr_id,
        details={"name": current_user.get("name")}
    )
    return {"status": "success", "message": "Successfully logged out."}

