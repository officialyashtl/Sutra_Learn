# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 01: SYSTEM ARCHITECTURE SPECIFICATION
**Version:** 1.0.0  
**Classification:** Core Infrastructure Architectural Contract  
**System Baseline:** SUTRA LEARN Release Candidate (FastAPI + React/TS/Vite + SQLite)  
**Target Score:** 1,000 / 1,000  

---

### 1. Executive Architecture Overview

SUTRA LEARN implements a four-tiered, multi-model adaptive AI infrastructure engineered specifically for mathematics pedagogy (NCERT Class 8 Mathematics: Linear Equations in One Variable). The platform bridges remote frontier cloud inference, local edge open-weight reasoning models, and deterministic curriculum validation engines into a coherent, fault-tolerant system.

```mermaid
flowchart TD
    subgraph Client ["Client Presentation Tier (React 18 + TS + Earthbound Editorial)"]
        UI_Tutor["Student Tutor Interface (/tutor)"]
        UI_Teacher["Educator Assistant (/teacher/analytics)"]
        Pill["Live Infrastructure Status Pill"]
        Badge["Per-Message Provider & Model Badge"]
    end

    subgraph Gateway ["FastAPI Application Gateway"]
        AuthMid["JWT Authentication & RBAC Guard"]
        AIRouter["AI Infrastructure Router (/api/v1/ai)"]
    end

    subgraph Core ["SUTRA Orchestration Core"]
        Config["Centralized AISettings (pydantic-settings)"]
        Orchestrator["12-State AIOrchestrator"]
        Registry["Provider Registry & Circuit Breaker Fleet"]
        MathVal["Deterministic Mathematical Validator"]
    end

    subgraph Providers ["Multi-Model Inference Providers"]
        T1["Tier 1: Google Gemini API (gemini-3.8-flash)"]
        T2["Tier 2: Qwen 3.5 4B (Local Ollama)"]
        T3["Tier 3: Gemma 4 E2B (Local Ollama)"]
        T4["Tier 4: Deterministic NCERT Curriculum Engine"]
    end

    subgraph Persistence ["Persistence Layer (SQLite DB)"]
        DBCred["Learners & Teachers"]
        DBConv["AI Conversations"]
        DBMsg["AI Messages & Telemetry"]
    end

    UI_Tutor -->|Bearer Token + AIRequest| AuthMid
    UI_Teacher -->|Bearer Token + AIRequest| AuthMid
    AuthMid --> AIRouter
    AIRouter --> Orchestrator

    Orchestrator --> Config
    Orchestrator --> Registry
    Registry --> T1
    Registry --> T2
    Registry --> T3
    Orchestrator --> MathVal
    Orchestrator --> T4

    AIRouter --> Persistence
    Pill -.->|GET /api/v1/ai/health| AIRouter
    Badge -.->|AIResponse Metadata| UI_Tutor
```

---

### 2. Tiered Inference Hierarchy & SLA Definitions

| Tier | Provider / Model | Runtime Environment | SLA Target | Failure Classification | Fallback Trigger |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Cloud)** | Google Gemini API (`gemini-3.8-flash`) | Google GenAI REST Endpoint | $< 3,000$ ms | 403 Forbidden, 429 Quota, 404 Deprecated, ConnectTimeout | Immediate Circuit Trip on 403/404; Failover on 429/Timeout |
| **Tier 2 (Local)** | Qwen 3.5 4B (`qwen3.5:4b`) | Ollama Socket (`127.0.0.1:11434`) | $< 45,000$ ms (CPU) / $< 4,000$ ms (GPU) | 503 Engine Offline, Timeout, OOM, Empty Content | Failover on Socket Unreachable or Inference Timeout |
| **Tier 3 (Local)** | Gemma 4 E2B (`gemma4:e2b`) | Ollama Socket (`127.0.0.1:11434`) | $< 12,000$ ms (CPU) / $< 1,500$ ms (GPU) | 503 Engine Offline, Timeout, OOM | Failover on Socket Unreachable or Inference Timeout |
| **Tier 4 (Final)** | Deterministic Curriculum Engine | In-Memory NCERT Knowledge Base | $< 5$ ms | None (Guaranteed Deterministic Return) | Terminal Safe Fallback; $100\%$ Uptime Guarantee |

---

### 3. Key Architectural Invariants

1. **Deterministic Guarantees:** When operating in `offline` mode or during network/runtime partitioning, the system guarantees $100\%$ curriculum coverage for all 6 core linear equations concepts (`MATH-C01` through `MATH-C06`).
2. **Pedagogical Invariance:** Under no circumstances does the system provide direct, unearned homework answers to students. Every response provides scaffolded hints, Socratic questioning, or worked steps.
3. **Mathematical Step Integrity:** Outputs containing linear equation transformation chains must pass algebraic step consistency checks against the underlying root $x^*$. Contradictory steps trip internal validation and trigger fallback.
4. **Zero Secret Leakage:** Authentication keys (e.g., `GEMINI_API_KEY`) are loaded via typed environment settings, never emitted into client responses, logs, or error traces.
5. **Traceability:** Every AI interaction generates an RFC 4122 v4 Request ID (`req_...`) persisted with latency, provider, model, tokens, and validation status in SQLite.

