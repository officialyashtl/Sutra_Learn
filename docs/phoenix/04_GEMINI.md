# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 04: GOOGLE GEMINI ADAPTER & ERROR CLASSIFICATION
**Version:** 1.0.0  
**Domain 6 (650 pts):** AI Provider Infrastructure (Tier 1 Cloud)  

---

### 1. Adapter Implementation Overview

The Google Gemini integration in SUTRA LEARN (`backend/app/ai/gemini_adapter.py`) uses the official `google-genai` SDK v2.34.0.
It encapsulates asynchronous client calls (`client.aio.models.generate_content`), structured system instructions grounded in the NCERT syllabus, and strict error classification.

```mermaid
flowchart TD
    Req["Incoming AIRequest"] --> Prep["Assemble Grounded NCERT Context"]
    Prep --> Call["client.aio.models.generate_content()"]
    
    Call -->|200 OK Response| Success["Extract Text & Token Usage --> Return Clean Dict"]
    
    Call -->|HTTP 403 PERMISSION_DENIED| Err403["ErrorCategory.PERMISSION_DENIED"]
    Call -->|HTTP 404 NOT_FOUND| Err404["ErrorCategory.MODEL_NOT_FOUND"]
    Call -->|HTTP 429 RESOURCE_EXHAUSTED| Err429["ErrorCategory.QUOTA_EXCEEDED"]
    Call -->|Connect / Read Timeout| ErrTime["ErrorCategory.TIMEOUT"]
    
    Err403 --> TripInstant["Trip Circuit Breaker to OPEN Immediately (0 Retries)"]
    Err404 --> TripInstant
    Err429 --> IncrFailure["Increment Failure Count; Trip on Threshold"]
    ErrTime --> IncrFailure
    
    TripInstant --> Cascade["Cascade to Tier 2 (Qwen 3.5 4B)"]
    IncrFailure --> Cascade
```

---

### 2. Empirical Verification & Google Cloud Account Findings

During automated diagnostics with key `AQ.Ab8RN6Kax...`:
1. **Endpoint Reachability & Auth:** Confirmed valid against Google GenAI REST endpoint. Successfully discovered 46 active models.
2. **Model Identifier:** `gemini-3.8-flash` is configured. (Previous model `gemini-2.5-flash` was rejected by Google with HTTP 404 deprecation notice).
3. **Generation Response:** Google returns HTTP 403 `PERMISSION_DENIED`:
   `{'error': {'code': 403, 'message': 'The Gemini API free tier is not available for this project. To use the Gemini API, please set up billing to upgrade to the paid tier at https://aistudio.google.com/billing...', 'status': 'PERMISSION_DENIED'}}`
4. **Resilience Action:** The system correctly:
   - Does NOT hang the student request.
   - Does NOT leak the secret into logs or errors.
   - Trips the circuit breaker to `OPEN` immediately.
   - Seamlessly cascades to Tier 2 (Qwen) and Tier 3 (Gemma).

---

### 3. Pedagogical Constraints

The Gemini prompt includes strict Socratic constraints:
- Identity: SUTRA LEARN Master Mathematics Tutor (NCERT Class 8).
- Constraint: Never provide final arithmetic answers unprompted. Guide students using inverse operations and balance scale principles.
- Safety: Explicit rejection of out-of-scope non-educational requests.

