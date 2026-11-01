# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 10: NCERT CURRICULUM COVERAGE & ADAPTIVE PEDAGOGY
**Version:** 1.0.0  
**Domain 9 (650 pts) & Domain 10 (650 pts):** Curriculum Coverage & Adaptive Learning Engine  

---

### 1. NCERT Class 8 Mathematics Syllabus Scope

SUTRA LEARN implements the complete curriculum for NCERT Class 8 Mathematics — Chapter 2: Linear Equations in One Variable, spanning 6 interconnected concepts:

| Concept ID | Concept Title | Prerequisite Concepts | Core Pedagogical Objective | Misconception Trap IDs |
| :--- | :--- | :--- | :--- | :--- |
| **`MATH-C01`** | Integer Operations with Negative Numbers | None (Foundation) | Master $+$, $-$, $\times$, $\div$ with negative integers. | `sign_error`, `sub_neg_error` |
| **`MATH-C02`** | Balance Concept of Equations | `MATH-C01` | Conceptualize equality as a balanced scale requiring symmetric operations. | `unbalanced_operation` |
| **`MATH-C03`** | Inverse Operations | `MATH-C01`, `MATH-C02` | Apply inverse operations systematically to isolate variables. | `inverse_conf` |
| **`MATH-C04`** | Simplifying Expressions | `MATH-C01` | Combine like terms and apply the distributive property ($a(b+c) = ab+ac$). | `distrib_incomplete`, `like_terms_error` |
| **`MATH-C05`** | Solving Linear Equations | `MATH-C01` to `MATH-C04` | Execute multi-step algebraic solution sequences with complete accuracy. | `sign_error`, `inverse_conf` |
| **`MATH-C06`** | Verifying Solutions | `MATH-C05` | Substitute root back into original equation to prove $\text{LHS} = \text{RHS}$. | `sub_calc_error` |

---

### 2. Directed Acyclic Graph (DAG) Invariant

The prerequisite graph is strictly acyclic, verified by `backend/tests/test_content.py::test_prerequisite_graph_acyclic`:
```
MATH-C01 (Negative Integers)
   │
   ├───────────────┐
   ▼               ▼
MATH-C02        MATH-C04 (Simplification)
(Balance Scale)    │
   │               │
   ▼               │
MATH-C03 (Inverse) │
   │               │
   └───────┬───────┘
           ▼
        MATH-C05 (Linear Equations)
           │
           ▼
        MATH-C06 (Verification by Substitution)
```

---

### 3. The 5 Deterministic Adaptive Engine Outcomes

The adaptive learning engine (`backend/app/engine/adaptive.py`) evaluates student attempts deterministically using 5 pedagogically validated outcomes:

1. **`CONFIRM`:** Student has 1 attempt with insufficient evidence to determine mastery. Assigns an unattempted question on the same concept.
2. **`STRETCH`:** Student achieves 2 unassisted correct answers in a row ($\ge 85\%$ confidence). Advances the student to the next concept in the DAG.
3. **`SCAFFOLD`:** Student relied on hints or took extended time. Provides a guided, hint-scaffolded question on the same concept.
4. **`BRIDGE_BACK`:** Student commits 2 consecutive misconception errors rooted in a prerequisite concept (e.g. sign error in linear equations). Automatically bridges the student back to prerequisite `MATH-C01`.
5. **`TEACHER_REVIEW`:** Student fails 3 consecutive attempts on a concept. Automatically flags the student's dossier for clinical educator intervention.

*Zero LLM non-determinism is permitted to modify mastery scores or learning pathways.*

