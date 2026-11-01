# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 10: CURRICULUM CONTEXT & GROUNDING SPECIFICATION
**Version:** 1.0.0  
**Implementation:** `backend/app/ai/curriculum_context.py`  
**Curriculum Scope:** NCERT Class 8 Mathematics — Chapter 2: Linear Equations in One Variable  

---

### 1. Curriculum Knowledge Hierarchy

SUTRA LEARN anchors all AI inference to verified NCERT Class 8 Mathematics learning objectives across six interconnected concepts:

| Concept ID | Concept Title | Prerequisite Concepts | Core Pedagogical Objective | Common Student Misconceptions |
| :--- | :--- | :--- | :--- | :--- |
| `MATH-C01` | Integer Operations with Negative Numbers | None (Foundational Prerequisite) | Master addition, subtraction, multiplication, and division with negative integers. | Treats subtracting a negative as subtraction (e.g. $-8 - (-15) = -23$ instead of $+7$). |
| `MATH-C02` | Balance Concept of Equations | `MATH-C01` | Understand an equation as a balanced scale where identical operations preserve equality. | Unbalanced operation: modifies LHS without modifying RHS. |
| `MATH-C03` | Inverse Operations | `MATH-C01`, `MATH-C02` | Apply inverse operations systematically to isolate variables. | Inverts operation incorrectly; confusion between additive and multiplicative inverses. |
| `MATH-C04` | Simplifying Algebraic Expressions | `MATH-C01` | Combine like terms and apply the distributive property correctly. | Distributive property incomplete: $2(x+3)$ expanded as $2x+3$. |
| `MATH-C05` | Solving Linear Equations | `MATH-C01`, `MATH-C02`, `MATH-C03`, `MATH-C04` | Execute multi-step algebraic solution sequences with complete accuracy. | Drops negative signs when dividing by negative coefficients ($-4x = 20 \implies x = 5$). |
| `MATH-C06` | Verifying Solutions by Substitution | `MATH-C05` | Substitute root back into original equation to prove $\text{LHS} = \text{RHS}$. | Substitutes into a modified step rather than the original equation. |

---

### 2. Directed Acyclic Graph (DAG) Invariant

The prerequisite graph is strictly acyclic, proven by automated unit testing in `backend/tests/test_content.py::test_prerequisite_graph_acyclic`:
```
MATH-C01 (Negative Integers)
   |
   +---> MATH-C02 (Balance Scale)
   |        |
   |        +---> MATH-C03 (Inverse Operations)
   |                 |
   +---> MATH-C04 (Simplification)
            |
            +---> MATH-C05 (Linear Equations)
                     |
                     +---> MATH-C06 (Verification by Substitution)
```

---

### 3. Context Injection Mechanism

When an AI adapter builds a prompt, `get_grounded_concept_context(concept_id)` extracts:
1. Concept title, description, and mastery objectives.
2. Direct worked examples showing the step-by-step arithmetic.
3. Explicit list of common misconceptions and distractor rationales.
4. Prerequisite chain for potential remediation bridging.

This grounding guarantees that whether Gemini, Qwen, Gemma, or Fallback responds, the mathematical terminology and problem representations remain uniform.

