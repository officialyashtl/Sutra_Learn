# SUTRA LEARN — OMEGA ∞
## DOCUMENT 04: AI SUBSYSTEM IMPLEMENTATION & RESILIENCE REPORT

**System:** SUTRA LEARN AI Subsystem  
**Integration Scope:** Google GenAI Gemini Developer API + Multi-Tier Failover Cascade  
**Files Modified / Verified:**
- `backend/app/ai/config.py`
- `backend/app/ai/gemini_adapter.py`
- `backend/app/ai/circuit_breaker.py`
- `backend/app/ai/orchestrator.py`
- `backend/app/ai/provider.py`
- `backend/app/ai/registry.py`
- `backend/app/routers/tutor.py`
- `backend/app/routers/educator_assistant.py`
**Date:** November 4, 2026  
**Status:** FULLY IMPLEMENTED & INTEGRATED  

---

### 1. PROVIDER IMPLEMENTATION ARCHITECTURE

The integration implements the official `google-genai` SDK with full async support via `client.aio.models.generate_content`.

```python
# Initialization snippet from backend/app/ai/gemini_adapter.py
if self.api_key and not self.api_key.startswith("mock") and not self.api_key.startswith("your_"):
    try:
        from google import genai
        self._client = genai.Client(api_key=self.api_key)
    except Exception as e:
        logger.error(f"Failed to initialize Google GenAI client: {e}")
        self._client = None
```

#### Key Implementation Characteristics:
1. **Model Cascade Mechanism:** When calling `generate_content`, the adapter attempts the primary model (`gemini-flash-lite-latest`). If Google returns an HTTP 503 (demand spike) or HTTP 404 (model retirement), it automatically cascades to secondary verified candidates (`gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.8-flash`) within the same request lifecycle.
2. **Asynchronous Execution:** Generation is performed asynchronously without blocking the FastAPI event loop.
3. **Usage & Attribution Metadata:** Every response captures exact latency in milliseconds, token counts from `response.usage_metadata`, and the exact model identifier that fulfilled the request.

---

### 2. RESILIENCE ENGINE & CIRCUIT BREAKER SPECIFICATION

To prevent cascading failures and retry storms, `backend/app/ai/circuit_breaker.py` manages a strict finite-state machine for each provider:

```
          ┌────────────────────────────────────────────────────────┐
          │                                                        │
          ▼                                                        │
    ┌───────────┐      Failure Threshold Exceeded (5)      ┌───────┴──────┐
    │  CLOSED   │ ───────────────────────────────────────> │     OPEN     │
    │ (Normal)  │                                          │ (Fast-Fail)  │
    └───────────┘                                          └───────┬──────┘
          ▲                                                        │
          │                   Success Recovery                     │ Cooldown Elapsed (60s)
          └──────────────────────────────────────────────┐         │
                                                         │         ▼
                                                   ┌───────────────┴┐
                                                   │   HALF-OPEN    │
                                                   │ (Trial Probe)  │
                                                   └────────────────┘
```

#### Circuit Breaker Parameters:
- **Failure Threshold:** 5 consecutive failed requests.
- **Cooldown Window:** 60 seconds before transitioning from `OPEN` to `HALF-OPEN`.
- **Success Threshold:** 2 consecutive successful responses in `HALF-OPEN` resets the circuit to `CLOSED`.
- **Fast Failover:** When the circuit is `OPEN`, requests bypass the network call entirely and immediately route to the Tier 2 local Ollama runtime or Tier 3 NCERT deterministic engine.

---

### 3. SUTRA LEARN PEDAGOGICAL MODES IMPLEMENTATION

The AI subsystem supports 6 distinct teaching modes, each configured with pedagogical instructions grounded in NCERT Class 8 Mathematics:

| Teaching Mode | Router Parameter | Pedagogical Objective | Response Format |
|---|---|---|---|
| **Guided Learning** | `guided_learning` | Socratic questioning; prompts student for the next algebraic step | Step-by-step questions with 2 progressive hints |
| **Worked Example** | `worked_example` | Complete demonstration of balance operations ($$ax + b = cx + d$$) | Formatted LaTeX equations with step explanations |
| **Practice Question** | `practice` | Generates a calibrated practice problem at the student's current tier | Question statement with hints |
| **Check My Work** | `check_my_work` | Diagnoses student's proposed algebraic solution and highlights errors | Misconception code diagnosis & correction |
| **Quick Revision** | `quick_revision` | Synthesizes core concept rules and balance axioms | Bulleted review summary |
| **Prerequisites** | `prerequisite_support` | Identifies and bridges foundational gaps (integers, fractions) | Diagnostic bridging problem |

---

### 4. DATA ISOLATION & CONVERSATION PERSISTENCE

All conversational data is persisted in SQLite with relational foreign keys and learner ownership constraints:

```sql
-- Conversations Table
CREATE TABLE IF NOT EXISTS ai_conversations (
    id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    owner_role TEXT NOT NULL,
    title TEXT NOT NULL,
    conversation_type TEXT NOT NULL,
    concept_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner_id) REFERENCES learners(id)
);

-- Messages Table
CREATE TABLE IF NOT EXISTS ai_messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    sender_role TEXT NOT NULL,
    content TEXT NOT NULL,
    response_type TEXT NOT NULL,
    hints TEXT,
    concept_id TEXT,
    requires_follow_up BOOLEAN DEFAULT 0,
    provider_metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE
);
```

#### Enforcement of Security Invariants:
1. **Server-Side Authentication:** In `backend/app/routers/tutor.py`, the user ID is resolved exclusively via `Depends(get_current_user)`. Frontend request parameters cannot spoof or override `owner_id`.
2. **Access Control:** `GET /api/v1/tutor/conversations/{id}` explicitly checks `conv["owner_id"] == current_user["id"]`. Attempts to access another student's conversation trigger `HTTP 403 Forbidden`.
3. **Transactional Safety:** Database connections use `PRAGMA busy_timeout = 10000;` and execute within isolated transactions to guarantee message ordering and prevent deadlocks.

