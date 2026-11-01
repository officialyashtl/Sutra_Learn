# SUTRA LEARN — Deterministic Adaptive Engine Verification
**Document ID:** `docs/03-adaptive-engine-verification.md`  
**Execution Standard:** Adaptive Learning Systems Engineer + Principal Software Architect  
**Timestamp:** 2026-11-01T17:29:00+05:30  
**Status:** DETERMINISTICALLY VERIFIED (100% REPRODUCIBLE)  

---

## 1. Adaptive Engine Architecture: `adaptive.py` & `policy.py`

SUTRA LEARN does NOT rely on opaque black-box neural networks for learning path recommendations. The adaptive engine is a deterministic, evidence-weighted policy engine implemented in `backend/app/engine/adaptive.py` with thresholds specified in `backend/app/engine/policy.py`.

### Authoritative Policy Thresholds
- **Mastery Threshold:** $\ge 0.85$ ($85\%$) weighted accuracy.
- **Minimum Independent Items for Mastery:** $\ge 2$ distinct unassisted correct submissions.
- **Scaffold Threshold:** $< 0.50$ ($50\%$) weighted accuracy or hint utilization.
- **Persistent Struggle Threshold:** $\ge 3$ consecutive errors on a concept triggers `TEACHER_REVIEW`.
- **Prerequisite Gap Rule:** Failure on complex equations caused by foundational sign confusion triggers `BRIDGE_BACK` to root concepts (`MATH-C01`).

---

## 2. The Four Student Outcomes & Teacher Review

```
                             [Assessment Attempt]
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  [Correct Answer]          [Incorrect Answer]
                         │                         │
            ┌────────────┴────────────┐            │
            ▼                         ▼            ▼
     [Unassisted]                [Assisted]  [Misconception Trapped?]
     Weight: 1.0                 Weight: 0.5       │
            │                         │       ┌────┴────┐
            │                         │       ▼         ▼
            ▼                         │  [Prereq Gap]  [Persistent Failures]
  Distinct Items >= 2?                │   (Sign Error) (>= 3 consecutive)
       ┌────┴────┐                    │       │         │
       ▼         ▼                    │       ▼         ▼
 [Accuracy]  [CONFIRM]                │  [BRIDGE_BACK] [TEACHER_REVIEW]
 >= 85%?    (Need more evidence)      │  (to MATH-C01) (Human Intervention)
   ┌───┴───┐                          │
   ▼       ▼                          ▼
[STRETCH] [CONFIRM]              [SCAFFOLD]
(Extend)  (Borderline)           (Stepwise Hints & Examples)
```

1. **`CONFIRM`:** Student has submitted only 1 question or evidence is insufficient to distinguish competence from chance guessing. Requests further unassisted validation.
2. **`SCAFFOLD`:** Student is struggling or requested hints; serves stepped explanations, worked examples, and reduces cognitive load.
3. **`BRIDGE_BACK`:** Student exhibited a specific prerequisite misconception (e.g. integer arithmetic error during multi-step linear equation solving); routes back to foundational module (`MATH-C01`).
4. **`STRETCH`:** Student demonstrated proven independent mastery ($\ge 85\%$ accuracy, $\ge 2$ unassisted distinct questions); unlocks next curriculum node.
5. **`TEACHER_REVIEW`:** Student experienced persistent struggle ($\ge 3$ errors); alerts educator for clinical human-in-the-loop intervention.

---

## 3. Empirical Verification Suite (Boundary Test Matrix)

Verified via automated test scripts `scripts/verify_mathematics.py` and `backend/tests/test_engine.py`:

| Test Scenario | Input Evidence Sequence | Calculated Score | Distinct Unassisted Items | Recommended Outcome | Deterministic Result |
|---|---|---|---|---|---|
| **Scenario A** | 2 correct, 0 hints, distinct Qs | $1.00$ ($100\%$) | 2 | **`STRETCH`** | **PASS** |
| **Scenario B** | 2 incorrect with `SIGN_ERROR` | $0.00$ ($0\%$) | 0 | **`BRIDGE_BACK`** (`MATH-C01`) | **PASS** |
| **Scenario C** | 3 consecutive failures | $0.00$ ($0\%$) | 0 | **`TEACHER_REVIEW`** | **PASS** |
| **Scenario D** | 1 unassisted correct attempt | $1.00$ ($100\%$) | 1 | **`CONFIRM`** | **PASS** |
| **Scenario E** | 2 correct with hint used | $0.50$ ($50\%$) | 0 | **`SCAFFOLD`** | **PASS** |
| **Scenario F** | Duplicate attempt on same Q | $1.00$ ($100\%$) | 1 (de-duplicated) | **`CONFIRM`** | **PASS** |

