# SUTRA LEARN — Offline Persistence & Synchronization Verification
**Document ID:** `docs/09-offline-sync-verification.md`  
**Execution Standard:** Senior Full-Stack Engineer + Data Integrity Engineer  
**Timestamp:** 2026-11-01T17:28:00+05:30  
**Status:** IMPLEMENTED & VERIFIED  

---

## 1. Offline-First Architecture

SUTRA LEARN ensures that learners in low-connectivity or intermittent network environments never experience data loss:

```
[Student in Lesson / Assessment]
               │
      [Network Probing]
     ┌─────────┴─────────┐
     ▼                   ▼
[Online Path]      [Offline Path]
     │                   │
[Direct POST]      [Store in IndexedDB: `pending_attempts`]
     │                   │
     ▼                   ▼
[200 OK Recorded]  [Client UI: Queued Locally]
                         │
                   [Connectivity Restored]
                         │
                         ▼
                   [syncPendingAttempts Loop]
                         │
                         ▼
                   [POST /api/v1/attempts (with client UUID)]
                         │
                   ┌─────┴─────┐
                   ▼           ▼
             [Fresh Attempt] [Duplicate Retry]
             Recorded (200)  Idempotent Acknowledge (200)
                   │           │
                   └─────┬─────┘
                         ▼
             [deletePendingAttempt from IndexedDB]
                         │
                         ▼
             [Canonical Metrics Updated]
```

---

## 2. Sync State Transition Machine

The offline synchronization engine maintains explicit discrete states:

| State | Indicator | Trigger & Operational Meaning |
|---|---|---|
| **`ONLINE`** | Green | Network available; requests route synchronously to backend. |
| **`OFFLINE`** | Amber | Network disconnected; lessons served from cache, attempts queued locally. |
| **`PENDING_SYNC`** | Blue | Unsynced attempts residing in IndexedDB `pending_attempts` object store. |
| **`SYNCING`** | Spinner | Active batch synchronization executing against `/api/v1/attempts`. |
| **`SYNCED`** | Checkmark | All queued attempts acknowledged and committed to SQLite backend. |
| **`SYNC_FAILED`** | Red Alert | Server returned non-200 error; attempts retained in IndexedDB for retry. |
| **`CONFLICT_REQUIRES_REVIEW`** | Purple Alert | Cryptographic token mismatch or learner mismatch flagged for review. |

---

## 3. Idempotency & Duplicate Prevention Verification

### Mechanism
Every attempt generates a client-side RFC 4122 v4 UUID (`attempt_id`). When submitted to `POST /api/v1/attempts`:
1. SQLite checks `SELECT id FROM attempts WHERE id = ?`.
2. If absent: inserts attempt and returns `is_duplicate: False`.
3. If present: returns existing record with `is_duplicate: True` and HTTP 200.
4. Client acknowledges and safely evicts record from IndexedDB.

### Automated Test Verification
Verified in `backend/tests/test_api.py::test_idempotent_attempt_submission` and `scripts/verify_e2e.py` Stage 05:
- First submission: `HTTP 200 OK`, `is_duplicate=False`.
- Immediate identical retry: `HTTP 200 OK`, `is_duplicate=True`.
- Total database rows for that attempt: exactly **1**. Zero evidence inflation.

