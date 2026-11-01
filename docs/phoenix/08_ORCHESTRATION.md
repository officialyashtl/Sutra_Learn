# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 08: 12-STATE AI ORCHESTRATION & ROUTING ENGINE
**Version:** 1.0.0  
**Domain 7 (450 pts):** AI Orchestration & Intelligent Routing  

---

### 1. The 12-State Request Lifecycle

Every AI request entering the SUTRA LEARN backend traverses an explicit, non-bypassable 12-state state machine in `AIOrchestrator` (`backend/app/ai/orchestrator.py`):

```
[01. RECEIVED] 
       │ (Assign RFC 4122 v4 Request ID: req_...)
       ▼
[02. VALIDATING] 
       │ (Enforce min/max length: 1 to 8,000 chars; reject injection attacks)
       ▼
[03. AUTHORIZING] 
       │ (Verify JWT bearer token, assert tenant & role boundaries)
       ▼
[04. BUILDING_CONTEXT] 
       │ (Extract NCERT concept definitions, bound history turns <= 8)
       ▼
[05. SELECTING_PROVIDER] 
       │ (Query Provider Registry for eligible models; check circuit breakers)
       ▼
[06. GENERATING] ──► (Timeout / Exception) ──► [09. RETRYING]
       │                                             │
       │ (Raw text received)                         ▼
       ▼                                      [05. SELECTING_PROVIDER]
[07. VALIDATING_OUTPUT]                              │ (Exhausted / Offline)
       │                                             ▼
       ├─► (Valid Math Steps) ──► [08. COMPLETED]   [10. FALLBACK]
       │                                             │
       └─► (Contradiction) ────► [09. RETRYING] ─────┴─► [08. COMPLETED]
                                                           │
                                                           ▼
                                                    [12. AUDITED]
```

---

### 2. State Invariants & Operational Rules

1. **Request Tracking:** Every transaction receives an immutable `request_id` (`req_<hex>`).
2. **Context Bounding:** Conversation history is strictly bounded to `AI_MAX_HISTORY_MESSAGES` ($\le 8$ turns) to prevent prompt bloat and runaway latency.
3. **No Recursive Cascade:** An attempt counter tracks tries. Total attempts cannot exceed `AI_MAX_TOTAL_ATTEMPTS` (default: 4), guaranteeing termination.
4. **Deterministic Exit:** If all remote and local models are unavailable or fail mathematical validation, the request enters state `10. FALLBACK`, which invokes `CurriculumGroundedFallbackProvider` to guarantee sub-5ms response delivery.
5. **Audit Invariant:** State `12. AUDITED` persists the message, latency, provider attribution, model ID, and validation status to SQLite prior to client dispatch.

