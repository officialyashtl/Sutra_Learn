# SUTRA LEARN — Mathematics & Misconception Diagnostics
**Document ID:** `docs/04-mathematics-and-diagnostics.md`  
**Execution Standard:** Mathematics Assessment Engineer + Curriculum Specialist  
**Timestamp:** 2026-11-01T17:29:00+05:30  
**Status:** MATHEMATICALLY VERIFIED & GROUNDED IN NCERT  

---

## 1. Curriculum Scope & Domain Rigor

SUTRA LEARN implements the complete foundational and core curriculum for **NCERT Class 8 Mathematics — Chapter 2: Linear Equations in One Variable**:

```
[MATH-C01: Integer Arithmetic] (Prerequisite Foundation)
       │
       ├─────────────────────────────────┐
       ▼                                 ▼
[MATH-C02: Balance Principle]     [MATH-C03: Inverse Operations]
       │                                 │
       └────────────────┬────────────────┘
                        ▼
       [MATH-C04: Simplifying Expressions]
                        │
                        ▼
       [MATH-C05: Solving Linear Equations]
                        │
                        ▼
       [MATH-C06: Verifying Solutions by Substitution]
```

---

## 2. Mathematical Verification of 8 Core Algebraic Equation Cases

All equation solvers and evaluation routines are tested against exact symbolic transformations and substitution checks:

| Case ID | Algebraic Type | Target Equation | Solved Value ($x$) | Verification by Substitution | Diagnostic Test Status |
|---|---|---|---|---|---|
| **Case 1** | Standard Two-Step | $2x + 5 = 15$ | $x = 5.0$ | $\text{LHS} = 2(5) + 5 = 15 = \text{RHS}$ | **PASS** |
| **Case 2** | Subtraction Two-Step | $3x - 7 = 11$ | $x = 6.0$ | $\text{LHS} = 3(6) - 7 = 11 = \text{RHS}$ | **PASS** |
| **Case 3** | Distribution / Brackets | $2(x + 3) = 14$ | $x = 4.0$ | $\text{LHS} = 2(4 + 3) = 14 = \text{RHS}$ | **PASS** |
| **Case 4** | Variables on Both Sides | $5x + 2 = 3x + 10$ | $x = 4.0$ | $\text{LHS} = 22 = \text{RHS} = 22$ | **PASS** |
| **Case 5A**| Negative Coefficient | $-4x + 9 = 29$ | $x = -5.0$ | $\text{LHS} = -4(-5) + 9 = 29 = \text{RHS}$| **PASS** |
| **Case 5B**| Negative Product / Inverse Div | $-7x = 35$ | $x = -5.0$ | $\text{LHS} = -7(-5) = 35 = \text{RHS}$ | **PASS** |
| **Case 6** | Fraction Coefficients | $\frac{x}{3} + \frac{5}{2} = -\frac{3}{2}$ | $x = -12.0$ | $\text{LHS} = -4 + 2.5 = -1.5 = \text{RHS}$| **PASS** |
| **Case 7** | Substitution Verification | $3x + 5 = 2x + 9$ | $x = 4.0$ | $\text{LHS} = 17 = \text{RHS} = 17$ | **PASS** |

---

## 3. Misconception Distractor Tagging in Question Bank

Assessment questions do NOT present arbitrary incorrect options. Distractor options in `backend/app/content/questions.py` are engineered around common cognitive traps identified in educational research:

### Trap 1: Inverse Operation Confusion (`INVERSE_OPERATION_CONFUSION`)
- **Example:** In $2x + 5 = 15$, the student adds $5$ to the RHS instead of subtracting, yielding $2x = 20 \implies x = 10$.
- **Detection:** Diagnosed when distractor option matching $+5$ addition is selected.
- **Pedagogical Action:** Triggers review of `MATH-C02` (Balance Principle) and `MATH-C03` (Inverse Operations).

### Trap 2: Sign Inversion / Dropping Negative (`SIGN_ERROR`)
- **Example:** In $-7x = 35$, dividing by $-7$ results in $+5$ instead of $-5$.
- **Detection:** Diagnosed when positive magnitude is chosen ignoring negative divisor.
- **Pedagogical Action:** Triggers `BRIDGE_BACK` to `MATH-C01` (Integer Arithmetic).

### Trap 3: Incomplete Distribution (`DISTRIBUTION_INCOMPLETE`)
- **Example:** In $7a - 2(3a - 4)$, expanding without distributing negative sign to $-4$, yielding $7a - 6a - 8$ instead of $a + 8$.
- **Detection:** Diagnosed when negative coefficient fails to invert interior sign.
- **Pedagogical Action:** Scaffolds step-by-step bracket expansion in `MATH-C04`.

