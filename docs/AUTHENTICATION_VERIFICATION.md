# SUTRA LEARN — AUTHENTICATION, CRYPTOGRAPHY & 401 FORENSIC AUDIT
**Document Version:** 1.0.0-OMEGA  
**Classification:** Cybersecurity Engineering & Cryptographic Assurance  
**Author:** Yash TL (The Oath of Tyr)  
**Verification Suite:** `scripts/test_omega_forensic_suite.py` (Suites 1 & 2)  

---

## 1. Cryptographic Authentication Specification

SUTRA LEARN implements an enterprise-grade authentication subsystem adhering to OWASP and NIST SP 800-63B standards.

### 1.1 Password Hashing Architecture
- **Algorithm:** PBKDF2 with HMAC-SHA256
- **Iteration Count:** 100,000 iterations (OWASP recommended baseline)
- **Salt:** 16 bytes of cryptographically secure random bytes generated via `secrets.token_bytes(16)`
- **Comparison Function:** `hmac.compare_digest()` to eliminate timing attack vectors
- **Format:** `pbkdf2:sha256:100000$<salt_hex>$<hash_hex>`

```python
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"pbkdf2:sha256:100000${salt.hex()}${dk.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    if not stored_hash or not stored_hash.startswith("pbkdf2:sha256:"):
        return False
    parts = stored_hash.split("$")
    salt = bytes.fromhex(parts[1])
    target_hash = bytes.fromhex(parts[2])
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return hmac.compare_digest(derived, target_hash)
```

---

## 2. JWT Cryptographic Token Lifecycle

Tokens are constructed with base64url-encoded header and payload, signed using HMAC-SHA256 with the cluster secret key:

- **Token Format:** `sutra_jwt_<base64_header>.<base64_payload>.<base64_signature>`
- **Token Claims:**
  - `sub`: Unique Subject ID (`student-01`, `teacher-01`)
  - `role`: Role entitlement (`student` | `teacher` | `admin`)
  - `name`: Display name
  - `iat`: Epoch seconds issued at
  - `exp`: Epoch seconds expiration (12-hour sliding window)
  - `jti`: Nonce to prevent replay attacks

---

## 3. Forensic Root Cause Analysis: The 401 Unauthorized Cascade

During the initial emergency audit, several instances of unexpected `401 Unauthorized` responses were analyzed and traced to three distinct architectural root causes.

### Root Cause 1: Multi-Worker Ephemeral Signing Secret
- **Mechanism:** In `backend/app/auth.py`, when `SUTRA_SECRET_KEY` was not explicitly set in `.env`, the module initialized:
  ```python
  SECRET_KEY = os.getenv("SUTRA_SECRET_KEY") or secrets.token_bytes(32)
  ```
- **Consequence:** In production Uvicorn configurations running multiple workers (`--workers 2` or `--workers 4`), each worker process executed this import independently, generating different random keys. A student authenticated by Worker 1 had their subsequent request routed by the OS kernel load balancer to Worker 2, where signature verification failed cryptographically, producing a `401 Unauthorized: Cryptographic token signature verification failed`.
- **Resolution:**
  1. Configured persistent `SUTRA_SECRET_KEY` in root `.env` and `backend/.env`.
  2. Implemented a deterministic host/database cluster fallback so multi-worker clusters remain synchronized even in bare-container environments.

### Root Cause 2: Unmigrated Demo Learner Password Hashes
- **Mechanism:** Early database seed scripts initialized demo learner rows prior to the addition of the `password_hash` column. Consequently, rows in `backend/sutra_learn.db` contained `password_hash = NULL`.
- **Consequence:** In `routers/auth.py`, a `NULL` hash triggered either an unhandled NoneType exception or failed password verification for standard demo logins.
- **Resolution:**
  - Updated `backend/app/db/database.py` in `init_db()` with an automatic migration query:
  ```sql
  UPDATE learners SET password_hash = ? WHERE password_hash IS NULL;
  UPDATE teachers SET password_hash = ? WHERE password_hash IS NULL;
  ```
  - Standardized default credentials (`sutra123` for students, `teacher123` for teachers).

### Root Cause 3: Missing Frontend 401 Session Interceptor
- **Mechanism:** In `frontend/src/App.tsx` and child components, fetch calls used `headers: authToken ? { Authorization: ... } : {}`. When a token expired or was rejected, the server responded with 401, but the client left the stale token in `localStorage`.
- **Consequence:** Every tab switch or background refetch triggered a repetitive wave of 401 errors without redirecting the user or resetting application state.
- **Resolution:**
  - Created `frontend/src/api/client.ts` with a centralized fetch wrapper.
  - On any 401 response, `client.ts` clears `sutra_auth_token` and dispatches `window.dispatchEvent(new CustomEvent("sutra:auth-expired"))`.
  - Added a global event listener in `frontend/src/App.tsx` that catches this event, cleans React auth state, and smoothly transitions to the login screen.

---

## 4. Empirical Test Suite Evidence (`test_omega_forensic_suite.py`)

The automated security test harness verified all cryptographic behaviors:

```text
--- 1. PASSWORD CRYPTOGRAPHY & BYPASS RESISTANCE ---
[PASS] PBKDF2-HMAC-SHA256 constant-time verification verified (100k iterations).

--- 2. CRYPTOGRAPHIC TOKEN LIFECYCLE & TAMPERING TESTS ---
[PASS] Valid token verified: subject=student-01, role=student
[PASS] Expired token correctly rejected: 401: Token has expired.
[PASS] Tampered token signature correctly rejected: 401: Cryptographic token signature verification failed.
[PASS] Invalid token prefix correctly rejected: 401: Invalid token format.

--- 4. CROSS-STUDENT ISOLATION & CONVERSATION OWNERSHIP ---
[PASS] Conversation owned by student-01 successfully retrieved.
[PASS] Cross-student deletion by student-02 correctly rejected: Conversation preserved.
```

---

## 5. Security Summary & Defenses

1. **Zero Password Plaintext:** No plaintexts stored anywhere in memory or disk.
2. **Timing Attack Immune:** Constant-time hash verification.
3. **Tamper Proof:** HMAC-SHA256 signature verification over headers and payloads.
4. **Ownership Gated:** Student cannot read, modify, or delete another student's conversation or progress records (`403 Forbidden`).

