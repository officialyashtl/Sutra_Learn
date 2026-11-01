# SUTRA LEARN — Multi-Provider AI Architecture
**Document ID:** `docs/05-ai-provider-architecture.md`  
**Execution Standard:** AI Systems Architect + Application Security Engineer  
**Timestamp:** 2026-11-01T17:26:00+05:30  
**Status:** IMPLEMENTED & VERIFIED  

---

## 1. Architectural Model Stack & Priority

SUTRA LEARN integrates a resilient, multi-tiered AI provider orchestrator designed to operate under diverse deployment constraints (cloud, local offline, edge school servers):

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AI ROUTER (get_ai_provider)                     │
│         Evaluates mode: 'gemini' | 'ollama' | 'auto' | 'deterministic' │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│  Tier 1 (Cloud)  │       │  Tier 2 (Local)  │       │ Tier 3 (Fallback)│
│  Google Gemini   │       │   Ollama Local   │       │ SUTRA Curriculum │
│ gemini-2.5-flash │       │ Qwen 3.5 4B /    │       │ Grounded Engine  │
│                  │       │ Gemma 4 E2B      │       │ (Deterministic)  │
└────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
         │                          │                          │
         │ Failover (missing key /  │ Failover (unreachable /  │
         │ network / quota)         │ timeout)                 │
         └─────────────────────────►└─────────────────────────►│
```

### Authoritative Provider Hierarchy
1. **Primary Cloud AI:** Google Gemini API (`gemini-2.5-flash`) via `https://generativelanguage.googleapis.com/v1beta`.
2. **Primary Local/Offline AI:** Ollama with `Qwen 3.5 4B` (`qwen:3.5-4b`).
3. **Lightweight Local Fallback:** Ollama with `Gemma 4 E2B` (`gemma4:e2b`, verified operational).
4. **Deterministic Curriculum Fallback:** SUTRA Grounded Curriculum Fallback Engine (`CurriculumGroundedFallbackProvider`).

---

## 2. Strict AI Safety & Learning Authority Boundary

Under SUTRA LEARN architectural invariants, external AI models (Gemini, Qwen, Gemma) are strictly restricted to advisory and pedagogical duties:
- **PERMITTED:** Socratic questioning, conversational explanations, worked examples, stepped hints, concept reframing, and pedagogical diagnostic analysis.
- **ABSOLUTELY FORBIDDEN:**
  1. AI models NEVER directly update, compute, or write student mastery scores (`concept_progress.mastery_percentage`).
  2. AI models NEVER grade formal assessment attempts or determine `is_correct`.
  3. AI models NEVER unlock curriculum nodes in the prerequisite DAG.
  4. AI models NEVER execute student interventions without explicit teacher authorization.

All mastery determinations and curriculum progression policies are exclusively governed by the deterministic rules in `app.engine.adaptive` and `app.engine.policy`.

---

## 3. Provider Implementation Details

### Provider Interface: `BaseAIProvider`
Located in `backend/app/ai/provider.py`:
- `generate_tutor_response(message, concept_id, mode, conversation_history, learner_context) -> Dict[str, Any]`
- `generate_educator_insight(query, cohort_summary, concept_analytics, specific_learner_id) -> Dict[str, Any]`

### Standardized Attribution Metadata
Every response produced across any tier returns structured provenance:
```json
{
  "provider": "Ollama" | "GoogleGemini" | "SutraCurriculumGroundedFallback",
  "model": "gemma4:e2b" | "gemini-2.5-flash" | "ncert-class8-deterministic",
  "is_fallback": true | false,
  "fallback_reason": "string description if failover occurred",
  "requires_follow_up": true | false
}
```

---

## 4. Health Check & Observability Endpoint

Live runtime inspection is exposed at:
`GET /api/v1/ai/health`

Returns real-time reachability of the Ollama socket (`http://127.0.0.1:11434`), installed models, Gemini configuration status, and deterministic fallback availability.

