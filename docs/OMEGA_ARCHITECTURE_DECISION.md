# SUTRA LEARN — OMEGA ∞
## DOCUMENT 03: ARCHITECTURE DECISION RECORD (ADR-008)
### Multi-Tier Provider Cascade & Authoritative Learning Engine Decoupling

**Status:** APPROVED & IMPLEMENTED  
**Date:** November 4, 2026  
**Deciders:** Principal Software Architect, AI/ML Integration Lead, SRE Lead  
**Supersedes:** ADR-007 (Single Model Ollama / Preview Gemini Architecture)  

---

### 1. CONTEXT & PROBLEM STATEMENT

SUTRA LEARN serves students and teachers across diverse network and hardware conditions—from well-connected urban schools to low-bandwidth rural classrooms and completely air-gapped lab environments.

The integration of the Google GenAI Developer API key (`AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]`) introduces an ultra-fast, highly accurate cloud reasoning model (`gemini-flash-lite-latest` and `gemini-3.5-flash-lite`).

However, an educational platform cannot rely exclusively on a cloud API:
1. **Network Volatility:** School connections experience frequent drops.
2. **Provider Availability:** Remote models periodically encounter 503 high-demand spikes or quota exhaustion (429).
3. **Truthfulness Requirement:** Pedagogical feedback must never hallucinate mathematical steps.
4. **Offline Mandate:** Core practice and mastery evaluation must function when entirely disconnected from the internet.

---

### 2. EVALUATED ARCHITECTURAL OPTIONS

#### Option A: Monolithic Cloud Provider (Gemini Only)
- *Pros:* Simpler backend architecture, zero local model memory footprint.
- *Cons:* Complete system paralysis during network outages or quota limits. Violates the core offline-first requirement.
- *Verdict:* **REJECTED.**

#### Option B: Local-Only Inference (Ollama Qwen/Gemma Only)
- *Pros:* Fully self-contained, high data sovereignty.
- *Cons:* Requires high-end client/server GPUs (minimum 8GB VRAM) which typical low-cost school hardware lacks. Slower inference latency (15–30s on CPU).
- *Verdict:* **REJECTED.**

#### Option C: Pure Deterministic Rule Engine Only
- *Pros:* 100% mathematically verifiable, microsecond latency, zero runtime cost.
- *Cons:* Cannot interpret arbitrary natural language queries, conversational slang, or nuanced emotional frustration from students.
- *Verdict:* **REJECTED as sole provider; RETAINED as authoritative ground truth.**

#### Option D: Multi-Tier Failover Cascade with Grounded Deterministic Fallback (SELECTED)
- **Tier 1 (Cloud):** Google Gemini Developer API (`gemini-flash-lite-latest` $\to$ `gemini-3.5-flash-lite` $\to$ `gemini-3.1-flash-lite`).
- **Tier 2 (Local Server):** Ollama Local Models (`qwen3.5:4b` $\to$ `gemma4:e2b`).
- **Tier 3 (Authoritative Deterministic):** NCERT Class 8 Curriculum Rule Engine & SymPy Validator.
- *Pros:* Delivers the best available experience under all network conditions. 100% resilient.
- *Verdict:* **APPROVED & ADOPTED.**

---

### 3. ARCHITECTURAL TOPOLOGY & PIPELINE

```
                                 [ Student Request ]
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │    FastAPI Auth Layer   │ (JWT Validation & Rate Limiting)
                             └────────────┬────────────┘
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │ NCERT Context Grounding │ (Loads Concept, Objectives, Hints)
                             └────────────┬────────────┘
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │ Multi-Model Orchestrator│
                             └────────────┬────────────┘
                                          │
           ┌──────────────────────────────┼──────────────────────────────┐
           │ (Circuit Closed & Online)    │ (Cloud Unavailable/Offline)   │ (All Remote Failed)
           ▼                              ▼                              ▼
┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐
│ Google Gemini Cloud │        │ Ollama Local Models │        │ SUTRA Deterministic │
│ (Flash-Lite Latest) │        │ (Qwen 3.5 / Gemma)  │        │ Curriculum Engine   │
└──────────┬──────────┘        └──────────┬──────────┘        └──────────┬──────────┘
           │                              │                              │
           └──────────────────────────────┼──────────────────────────────┘
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │ SymPy / AST Validator   │ (Mathematical Truth Verification)
                             └────────────┬────────────┘
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │ Conversation Persistence│ (SQLite WAL Mode + Attribution)
                             └────────────┬────────────┘
                                          │
                                          ▼
                             [ Frontend Client Display ]
```

---

### 4. KEY DECISIONS & INVARIANTS

1. **Decoupled Provider Factory:** `backend/app/routers/tutor.py` accesses AI capabilities strictly through `get_ai_provider()`. Routers never instantiate concrete adapters directly.
2. **Deterministic Fallback is Transparent:** Responses generated by the deterministic engine or local fallback are explicitly tagged (`is_fallback: true`, `provider: "NCERT Curriculum Engine"`). The platform never claims Google Gemini generated a fallback answer.
3. **Mathematical Validation Gate:** AI-generated equations are passed through `backend/app/ai/math_validator.py` (using SymPy and Python AST) to verify balance operations before output delivery.
4. **Separation of Mastery and AI:** The AI Tutor provides instructional support, explanations, and hints. Authoritative student mastery (Bayesian Knowledge Tracing) is updated solely by formal question evaluations in `backend/app/engine/adaptive.py`. An AI tutor conversation never modifies student mastery scores directly.
5. **Circuit Breakers with Cooldown:** Consecutive failures (5 consecutive HTTP errors or timeouts) trip the circuit breaker to `OPEN` for 60 seconds, bypassing doomed network calls and routing immediately to Tier 2/3.

