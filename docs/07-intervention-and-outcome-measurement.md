# SUTRA LEARN — Educator Interventions & Outcome Measurement
**Document ID:** `docs/07-intervention-and-outcome-measurement.md`  
**Execution Standard:** Educational Technology Specialist + Database Architect  
**Timestamp:** 2026-11-01T17:27:00+05:30  
**Status:** IMPLEMENTED & VERIFIED  

---

## 1. The Human-in-the-Loop Intervention Lifecycle

SUTRA LEARN enforces a rigorous clinical model where automated algorithms diagnose and recommend, but authoritative pedagogical overrides remain under the certified control of human educators:

```
[Student Friction Detected] ──► [Adaptive Engine Flags TEACHER_REVIEW]
                                               │
                                               ▼
[Teacher Investigates Dossier] ◄── [Cohort Analytics Dashboard]
             │
             ▼
[Teacher Formulates Clinical Rationale]
             │
             ▼
[Authorized Override: POST /api/v1/teacher/override]
             │
             ├─────────────────────────────────────────────────┐
             ▼                                                 ▼
[Immutable Audit Record Created]             [Progress State Updated in SQLite]
Category: PEDAGOGICAL_INTERVENTIONS          `concept_progress.last_recommended_outcome`
Actor: Authenticated Teacher ID
             │
             ▼
[Targeted Remediation & Student Re-assessment]
             │
             ▼
[Effectiveness Measurement: GET /api/v1/teacher/interventions/{id}/effectiveness]
             │
             ▼
[Before vs. After Delta & Retention Verification]
```

---

## 2. Clinical Rationale Requirement & Compliance

Every teacher override requires:
- `learner_id`: Target student identifier.
- `concept_id`: Target concept code (`MATH-C01` through `MATH-C06`).
- `previous_outcome`: State prior to intervention.
- `overridden_outcome`: New prescribed path (`BRIDGE_BACK`, `SCAFFOLD`, `STRETCH`, `CONFIRM`).
- `reason`: Substantive educational justification ($\ge 5$ characters).

**Security Invariant:** Submissions lacking clinical rationale or containing trivial whitespace are rejected with `HTTP 400 Bad Request`.

---

## 3. Measuring Intervention Effectiveness

Intervention outcomes are tracked deterministically using timestamped attempts:
- **Pre-Intervention Baseline:** All attempts on `concept_id` where `server_timestamp < intervention_timestamp`.
- **Post-Intervention Outcome:** All attempts on `concept_id` where `server_timestamp >= intervention_timestamp`.
- **Accuracy Delta:** $\Delta_{\text{acc}} = \text{Accuracy}_{\text{post}} - \text{Accuracy}_{\text{pre}}$.
- **Misconception Resolution Rate:** Count of persistent error signals before vs. after.

### Methodological Rigor & Causality Disclosure
> [!IMPORTANT]
> SUTRA LEARN explicitly distinguishes observed before-and-after improvement from proven counterfactual causality. Observational changes reflect real student performance trajectories following teacher scaffolding, but formal causal claims require controlled baseline comparison groups.

