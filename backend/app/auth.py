"""
SUTRA LEARN - Server-Validated Authentication & Cryptographic Token Verification
Uses PBKDF2-HMAC-SHA256 for password hashing and HMAC-SHA256 signed tokens.
Zero reliance on external paid APIs; timing-attack safe comparison.
"""

import os
import hmac
import hashlib
import json
import base64
import time
import secrets
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, Depends
from app.db.database import get_db_connection

# Secret key for token signing (override via environment in production)
SECRET_KEY = os.environ.get(
    "SUTRA_SECRET_KEY",
    "sutra-dev-secret-do-not-use-in-production-b48c9e01f27a3d"
).encode("utf-8")

TOKEN_EXPIRY_SECONDS = 86400  # 24 hours


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with 100,000 iterations."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    )
    return f"{salt}:{key.hex()}"


def verify_password(plain_password: str, hashed: str) -> bool:
    """Verifies a plain password against a stored salt:hash string."""
    try:
        salt, key_hex = hashed.split(":", 1)
        expected = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        )
        return hmac.compare_digest(expected.hex(), key_hex)
    except Exception:
        return False


def create_access_token(user_id: str, role: str, name: str, expires_in: int = TOKEN_EXPIRY_SECONDS) -> str:
    """
    Creates a signed HMAC-SHA256 bearer token.
    Payload includes subject, role, name, issued-at, and expiration.
    """
    now = int(time.time())
    payload = {
        "sub": user_id,
        "role": role,
        "name": name,
        "iat": now,
        "exp": now + expires_in
    }
    payload_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode("utf-8").rstrip("=")

    signature = hmac.new(SECRET_KEY, payload_b64.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    return f"sutra.{payload_b64}.{sig_b64}"


def verify_access_token(token: str) -> Dict[str, Any]:
    """
    Verifies token structure, cryptographic signature, and expiration.
    Uses timing-safe comparison to prevent timing attacks.
    """
    if not token or not token.startswith("sutra."):
        raise HTTPException(status_code=401, detail="Invalid token format.")

    parts = token.split(".")
    if len(parts) != 3:
        raise HTTPException(status_code=401, detail="Malformed token structure.")

    prefix, payload_b64, sig_b64 = parts

    # Recompute signature
    expected_sig = hmac.new(SECRET_KEY, payload_b64.encode("utf-8"), hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode("utf-8").rstrip("=")

    if not hmac.compare_digest(sig_b64, expected_sig_b64):
        raise HTTPException(status_code=401, detail="Cryptographic token signature verification failed.")

    # Decode payload
    try:
        padding = "=" * (4 - (len(payload_b64) % 4)) if len(payload_b64) % 4 != 0 else ""
        payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token payload.")

    # Verify expiration
    now = int(time.time())
    if payload.get("exp", 0) < now:
        raise HTTPException(status_code=401, detail="Token has expired.")

    return payload


def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    conn=Depends(get_db_connection)
) -> Dict[str, Any]:
    """
    FastAPI dependency that validates Bearer token and checks user exists in SQLite.
    Never trusts raw client ID headers.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required: Provide a valid 'Authorization: Bearer <token>' header."
        )

    raw_token = authorization.split(" ", 1)[1].strip()
    payload = verify_access_token(raw_token)

    user_id = payload.get("sub")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role FROM learners WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail=f"Authenticated user '{user_id}' no longer exists.")

    return dict(user)


def require_teacher(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Dependency that strictly enforces teacher role on the authenticated token."""
    if current_user.get("role") != "teacher":
        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: User '{current_user.get('name')}' ({current_user.get('id')}) does not hold teacher privileges."
        )
    return current_user

