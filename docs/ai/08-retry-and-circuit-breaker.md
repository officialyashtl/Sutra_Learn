# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 08: RETRY & CIRCUIT BREAKER ENGINE
**Version:** 1.0.0  
**Implementation:** `backend/app/ai/circuit_breaker.py` (`CircuitBreaker`)  
**Pattern:** Resilience4j-style Provider Circuit Breaker with Categorized Error Handling  

---

### 1. Circuit Breaker Specification

Each inference adapter (Gemini, Qwen, Gemma) is isolated by its own `CircuitBreaker` instance. The circuit maintains three states:
- **`CLOSED`**: Healthy. Normal requests pass through to the provider adapter.
- **`OPEN`**: Tripped. Failures exceeded threshold or permanent error encountered. Requests are immediately rejected without attempting inference.
- **`HALF_OPEN`**: Cooldown elapsed. A single probe request is permitted to test provider recovery.

```
       [Normal Operations]
       +-----------------+
       |     CLOSED      |<---------------+
       +-----------------+                |
         |                                |
         | consecutive failures >= 3      | single probe succeeds
         | OR Permanent Error (403/404)   |
         v                                |
       +-----------------+        +-----------------+
       |      OPEN       |------->|    HALF_OPEN    |
       +-----------------+        +-----------------+
              cooldown >= 60s             |
                                          | probe fails
                                          v
                                  (return to OPEN)
```

---

### 2. Error Categorization & Immediate Tripping Rules

Errors are classified into five explicit categories (`ErrorCategory`):

| Error Category | HTTP Code / Trigger | Immediate Circuit Action | Retry Allowed? | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| `PERMISSION_DENIED` | HTTP 403 (Invalid Key / No Billing) | **Immediate Trip to `OPEN`** | **No** (0 retries) | Retrying with an unpaid or invalid key wastes latency. Immediately falls back to local models. |
| `MODEL_NOT_FOUND` | HTTP 404 (Deprecated Model Tag) | **Immediate Trip to `OPEN`** | **No** (0 retries) | Model does not exist on endpoint. Retrying will not resolve it. |
| `QUOTA_EXCEEDED` | HTTP 429 (Rate Limit Breached) | Increment failure count | **Yes** (Up to retry limit) | Transient rate limit. Tripped if failure count reaches threshold. |
| `TIMEOUT` | Request latency > SLA limit | Increment failure count | **Yes** (Cascade to next tier) | Downstream server is overloaded or hung. |
| `SERVICE_UNAVAILABLE` | HTTP 503 / Socket Connection Refused | Increment failure count | **Yes** | Server daemon offline or restarted. |
| `UNKNOWN` | Unhandled runtime exception | Increment failure count | **No** | Defensive catch to prevent orchestrator crash. |

---

### 3. Verification & Live Trace

During automated testing of `scripts/ai/verify_ai_backend.ps1`:
```
Circuit Breaker [gemini]: Permanent error (PERMISSION_DENIED) detected: 403 PERMISSION_DENIED.
Immediately tripping circuit to OPEN.
[req_ea717fdb9841] Gemini API failure (PERMISSION_DENIED): 403 PERMISSION_DENIED
```
The circuit breaker immediately shifted state to `OPEN`, preventing subsequent student queries from blocking on Google API calls.

