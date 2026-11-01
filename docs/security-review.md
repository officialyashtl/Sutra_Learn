# SUTRA LEARN — Application Security & Threat Model Review

## 1. Threat Modeling Overview

SUTRA LEARN handles educational performance data for Class 8 students and pedagogical control systems for teachers. The threat model is governed by three core principles:
1. **Confidentiality**: A student's performance, misconceptions, and learning trajectory must be private to that student and authorized educators.
2. **Integrity**: Knowledge mastery probabilities ($P(L)$), assessment attempts, and teacher overrides must be tamper-evident and immune to spoofing.
3. **Accountability**: Every consequential instructional override must be traceable to an authenticated teacher with an unalterable audit log.

---

## 2. Identified Vulnerabilities & Verified Hardening

### 2.1 Vulnerability SUTRA-SEC-001: Header-Based Identity Spoofing
- **Severity**: Critical (CVSS 9.1)
- **Attack Vector**: Attacker sends `x-teacher-id: teacher-01` in an HTTP request to `/api/v1/teacher/cohort` or `/api/v1/teacher/interventions`.
- **Pre-Fix Vulnerability**: The server trusted the header and returned complete cohort performance data or allowed creating instructional overrides without authentication.
- **Fix Implemented**:
  1. Deprecated all trust in `x-user-id` and `x-teacher-id` headers.
  2. Implemented stateless HMAC-SHA256 bearer tokens issued exclusively via `/api/v1/auth/session` or `/api/v1/auth/login`.
  3. Created `get_current_user` and `require_teacher` dependencies that cryptographically verify the signature, role, and expiration timestamp.
- **Verification Evidence**:
  - Unauthenticated request with `x-teacher-id: teacher-01` -> **`401 Unauthorized`**.
  - Student token attempting educator endpoint -> **`403 Forbidden`**.

### 2.2 Vulnerability SUTRA-SEC-002: Cross-Student IDOR (Insecure Direct Object Reference)
- **Severity**: High (CVSS 7.5)
- **Attack Vector**: Student `student-01` obtains a valid student bearer token and requests `/api/v1/learners/student-02/progress` or attempts to submit an assessment attempt under another student's ID.
- **Fix Implemented**:
  - Enforced ownership verification in `backend/app/auth.py`:
    ```python
    def verify_learner_access(target_learner_id: str, current_user: AuthUser):
        if current_user.role == "teacher":
            return True
        if current_user.role == "student" and current_user.user_id == target_learner_id:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Cannot access or modify other learners' records."
        )
    ```
- **Verification Evidence**:
  - Request by `student-01` for `student-02` progress -> **`403 Forbidden`** (Tested in `backend/tests/test_api.py` and `scripts/verify_e2e.py` Stage 12).

### 2.3 Vulnerability SUTRA-SEC-003: Substantive Rationale Bypass in Teacher Overrides
- **Severity**: Medium (CVSS 5.3)
- **Attack Vector**: Teacher submits an override with an empty or trivial reason (`""` or `"ok"`), undermining instructional accountability.
- **Fix Implemented**:
  - Implemented strict validation requiring `reason` to contain at least 5 meaningful characters:
    ```python
    if not payload.reason or len(payload.reason.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Pedagogical rationale required: A clinical reason of at least 5 characters must be provided for audit compliance."
        )
    ```
- **Verification Evidence**:
  - Override attempt with reason `"ok"` -> **`400 Bad Request`** (Tested in `scripts/verify_e2e.py` Stage 10).
  - Override attempt with reason `"Demonstrated oral mastery during one-on-one session"` -> **`200 OK`**.

### 2.4 Vulnerability SUTRA-SEC-004: Tamper-Evident Audit Trail Integrity
- **Severity**: Medium (CVSS 4.8)
- **Attack Vector**: Direct database tampering or spoofed audit log injection.
- **Fix Implemented**:
  - Every intervention record generates a SHA-256 state hash over the immutable tuple:
    $$\text{hash} = \text{SHA256}(\text{id} \parallel \text{learner\_id} \parallel \text{teacher\_id} \parallel \text{concept\_id} \parallel \text{override\_status} \parallel \text{timestamp})$$
  - Any subsequent alteration breaks hash verification during audit inspections.

---

## 3. Cryptographic Token Specification

```
Format: sutra.<base64url_payload>.<hex_hmac_sha256>

Payload JSON:
{
  "user_id": "student-01",
  "role": "student",
  "name": "Aarav Sharma",
  "iat": 1730419200,
  "exp": 1730505600
}

Signature:
HMAC_SHA256(key=SUTRA_SECRET_KEY, message="sutra.<base64url_payload>")
```

---

## 4. Verification Attack Matrix

| Test ID | Attack Scenario | Expected Response | Verified Response | Status |
| :--- | :--- | :--- | :--- | :--- |
| SEC-01 | Unauthenticated GET `/api/v1/teacher/cohort` | 401 Unauthorized | 401 Unauthorized | **PASS** |
| SEC-02 | Attacker with `x-teacher-id: teacher-01` header | 401 Unauthorized | 401 Unauthorized | **PASS** |
| SEC-03 | Student token accessing `/api/v1/teacher/cohort` | 403 Forbidden | 403 Forbidden | **PASS** |
| SEC-04 | Student token accessing another student's progress | 403 Forbidden | 403 Forbidden | **PASS** |
| SEC-05 | Forged bearer token signature | 401 Unauthorized | 401 Unauthorized | **PASS** |
| SEC-06 | Expired bearer token | 401 Unauthorized | 401 Unauthorized | **PASS** |
| SEC-07 | Teacher override with empty rationale | 400 Bad Request | 400 Bad Request | **PASS** |
| SEC-08 | Student deleting another student's tutor conversation | 403 Forbidden | 403 Forbidden | **PASS** |

