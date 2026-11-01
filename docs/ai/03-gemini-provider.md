# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 03: GOOGLE GEMINI CLOUD INFERENCE ADAPTER
**Version:** 1.0.0  
**Adapter Implementation:** `backend/app/ai/gemini_adapter.py`  
**Client SDK:** Official `google.genai` SDK v2.34.0  
**Primary Model Identifier:** `gemini-3.8-flash`  

---

### 1. Adapter Architecture

The `GeminiAdapter` encapsulates remote cloud communication with Google's Generative AI infrastructure.

```
AIRequest --> GeminiAdapter
                  |
                  |--> Build Grounded NCERT Context (curriculum_context.py)
                  |--> Configure System Instruction & Socratic Constraints
                  |--> Call Async Client: client.aio.models.generate_content()
                  |
                  +---> Success: Extract Text & Token Metadata
                  |
                  +---> HTTP 403 (PERMISSION_DENIED):
                  |         Trip Circuit to OPEN immediately (0 retries)
                  |
                  +---> HTTP 404 (NOT_FOUND / DEPRECATED):
                  |         Trip Circuit to OPEN immediately
                  |
                  +---> HTTP 429 (QUOTA_EXCEEDED):
                  |         Increment Failure Count; Trip on Threshold
                  |
                  +---> Timeout / Network Error:
                            Record Failure; Failover to Tier 2 (Qwen)
```

---

### 2. Live Runtime Findings & Error Classification

During verification against the live Google GenAI API endpoint with key ``:
1. **API Key Validity:** Authenticates successfully against `client.models.list()`, confirming valid project credentials.
2. **Model Deprecation Detection:** When querying `gemini-2.5-flash`, the API returns HTTP 404 (`NOT_FOUND. This model is no longer available to new users. Please update your code to use models/gemini-3.8-flash`). The adapter was immediately configured to `gemini-3.8-flash`.
3. **Billing / Quota Classification:** When querying `gemini-3.8-flash`, Google returns HTTP 403 (`PERMISSION_DENIED: The Gemini API free tier is not available for this project. To use the Gemini API, please set up billing...`).
4. **Permanent Failure Handling:** The adapter categorizes this as `ErrorCategory.PERMISSION_DENIED`. Instead of uselessly retrying or blocking the user for 60 seconds, it trips the circuit breaker to `OPEN` immediately and cascades to the local models.

---

### 3. Pedagogical Guardrails

When generating tutor responses, `GeminiAdapter` injects a rigorous system instruction:
- **Identity:** SUTRA LEARN Master Mathematics Tutor (NCERT Class 8).
- **Domain Scope:** Linear Equations in One Variable (`MATH-C01` to `MATH-C06`).
- **Pedagogical Rule:** Never give away direct answers. Use Socratic questioning, identify student misconceptions, and maintain step-by-step equality principles.
- **Mathematical Integrity:** State every transformation step clearly ($ax + b = c \implies ax = c - b \implies x = (c - b)/a$).

