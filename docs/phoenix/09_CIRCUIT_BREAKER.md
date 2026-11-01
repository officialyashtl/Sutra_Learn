# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 09: CIRCUIT BREAKER & ERROR RECOVERY POLICIES
**Version:** 1.0.0  
**Domain 7 (450 pts) & Domain 19 (400 pts):** Resilience & Circuit Breaker Engineering  

---

### 1. Circuit Breaker Specification

Each inference adapter is guarded by its own independent `CircuitBreaker` instance (`backend/app/ai/circuit_breaker.py`).
The circuit isolates cascading failures and maintains three distinct states:
- **`CLOSED`**: Standard operation. Requests flow freely. Consecutive failures increment a counter.
- **`OPEN`**: Tripped. Inference requests are blocked immediately at the boundary. Cooldown timer begins.
- **`HALF_OPEN`**: Cooldown elapsed. A single probe request tests downstream recovery. If successful, resets to `CLOSED`; if failed, resets to `OPEN`.

---

### 2. Categorized Error Handling & Immediate Tripping Rules

Errors are classified using `ErrorCategory`:

```
                +---------------------------------------+
                |           Downstream Error            |
                +---------------------------------------+
                                   │
                   ┌───────────────┴───────────────┐
                   ▼                               ▼
       [Permanent Errors]                 [Transient Errors]
       - PERMISSION_DENIED (403)          - QUOTA_EXCEEDED (429)
       - MODEL_NOT_FOUND (404)            - TIMEOUT
                                          - SERVICE_UNAVAILABLE (503)
                   │                               │
                   ▼                               ▼
       Immediate Trip to OPEN!            Increment Failure Count
       Retries: 0                         Trip to OPEN if count >= 3
       Cascade to Local Models            Cascade to Next Provider
```

---

### 3. Empirical Verification Trace

During Stage 07 execution of `scripts/ai/verify_ai_all.ps1`:
```
Circuit Breaker [gemini]: Permanent error (PERMISSION_DENIED) detected: 403 PERMISSION_DENIED.
Immediately tripping circuit to OPEN.
[req_086ea926f49e] Gemini API failure (PERMISSION_DENIED): 403 PERMISSION_DENIED
[req_086ea926f49e] Cascaded cleanly to Ollama Local Models
```
The circuit breaker immediately isolated the Google API billing failure, protecting user experience from latency spikes.

