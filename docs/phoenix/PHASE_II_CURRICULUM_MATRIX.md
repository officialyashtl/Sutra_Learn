# SUTRA LEARN — PHASE II CURRICULUM TRACEABILITY MATRIX
## NCERT Class 8 Mathematics (Complete Chapters 1 to 13 · 30 Concepts · 81 Diagnostic Questions)

| Chapter | Chapter Title | Concept ID | Code | Concept Title | Prerequisites | Question Count | Primary Misconception Trap |
|:---|:---|:---|:---|:---|:---|:---:|:---|
| **Ch 1** | Rational Numbers | `MATH-C07` | `RAT_NUM` | Rational Numbers & Properties | `MATH-C01` | 3 | `reciprocal_confusion` |
| **Ch 1** | Rational Numbers | `MATH-C08` | `RAT_OPS` | Operations on Rational Numbers | `MATH-C07` | 3 | `reciprocal_confusion`, `sign_error` |
| **Ch 2** | Linear Equations in One Variable | `MATH-C01` | `INT_ARITH` | Integer Arithmetic | None (Root) | 5 | `sign_error` |
| **Ch 2** | Linear Equations in One Variable | `MATH-C02` | `EQ_BAL` | The Balance Principle | `MATH-C01` | 5 | `unbalanced_operation` |
| **Ch 2** | Linear Equations in One Variable | `MATH-C03` | `INV_OPS` | Inverse Operations | `MATH-C01` | 5 | `inverse_conf`, `sign_error` |
| **Ch 2** | Linear Equations in One Variable | `MATH-C04` | `ALG_SIMP` | Simplifying Algebraic Expressions | `MATH-C01` | 5 | `distrib_incomplete`, `like_terms` |
| **Ch 2** | Linear Equations in One Variable | `MATH-C05` | `LIN_EQ` | Solving Linear Equations | `MATH-C02`, `MATH-C03`, `MATH-C04` | 5 | `sign_error`, `inverse_conf` |
| **Ch 2** | Linear Equations in One Variable | `MATH-C06` | `VER_SUB` | Verification by Substitution | `MATH-C05` | 5 | `sub_calc_error` |
| **Ch 3** | Understanding Quadrilaterals | `MATH-C09` | `POLY_PROPS` | Polygons & Classification | `MATH-C01` | 3 | `quadrilateral_angle_sum_error` |
| **Ch 3** | Understanding Quadrilaterals | `MATH-C10` | `QUAD_ANGLES` | Angle Sum & Quadrilaterals | `MATH-C09` | 2 | `quadrilateral_angle_sum_error` |
| **Ch 4** | Data Handling | `MATH-C11` | `DATA_ORG` | Organizing Data & Grouping | `MATH-C01` | 2 | `sub_calc_error` |
| **Ch 4** | Data Handling | `MATH-C12` | `PIE_CHART` | Circle Graphs / Pie Charts | `MATH-C11` | 2 | `sub_calc_error` |
| **Ch 5** | Squares and Square Roots | `MATH-C13` | `SQUARE_NUM` | Properties of Square Numbers | `MATH-C01` | 2 | `square_root_halving` |
| **Ch 5** | Squares and Square Roots | `MATH-C14` | `SQUARE_ROOT` | Square Roots & Estimation | `MATH-C13` | 2 | `square_root_halving` |
| **Ch 6** | Cubes and Cube Roots | `MATH-C15` | `CUBE_NUM` | Cubes and Perfect Cubes | `MATH-C01` | 2 | `sub_calc_error` |
| **Ch 6** | Cubes and Cube Roots | `MATH-C16` | `CUBE_ROOT` | Cube Roots by Prime Factorisation | `MATH-C15` | 2 | `sign_error` |
| **Ch 7** | Comparing Quantities | `MATH-C17` | `PERCENT_RAT` | Ratios, Percentages & Discounts | `MATH-C07` | 2 | `percentage_base_error` |
| **Ch 7** | Comparing Quantities | `MATH-C18` | `COMP_INT` | Compound Interest Formulation | `MATH-C17` | 2 | `percentage_base_error` |
| **Ch 8** | Algebraic Expressions & Identities | `MATH-C19` | `ALG_TERMS` | Algebraic Expressions Operations | `MATH-C04` | 2 | `distrib_incomplete`, `sign_error` |
| **Ch 8** | Algebraic Expressions & Identities | `MATH-C20` | `ALG_IDENT` | Standard Algebraic Identities | `MATH-C19` | 2 | `sign_error`, `sub_calc_error` |
| **Ch 9** | Mensuration | `MATH-C21` | `TRAP_AREA` | Area of Trapezium & Polygons | `MATH-C01` | 2 | `area_perimeter_confusion` |
| **Ch 9** | Mensuration | `MATH-C22` | `SURF_VOL` | Surface Area and Volume | `MATH-C21` | 2 | `area_perimeter_confusion` |
| **Ch 10** | Exponents and Powers | `MATH-C23` | `EXP_POS` | Powers with Positive Exponents | `MATH-C01` | 2 | `exponent_base_conflation` |
| **Ch 10** | Exponents and Powers | `MATH-C24` | `EXP_LAWS` | Negative Exponents & Power Laws | `MATH-C23` | 2 | `exponent_base_conflation` |
| **Ch 11** | Direct and Inverse Proportions | `MATH-C25` | `DIR_PROP` | Direct Proportion | `MATH-C07` | 2 | `proportion_inversion` |
| **Ch 11** | Direct and Inverse Proportions | `MATH-C26` | `INV_PROP` | Inverse Proportion | `MATH-C25` | 2 | `proportion_inversion` |
| **Ch 12** | Factorisation | `MATH-C27` | `FACT_ALG` | Factorisation using Identities | `MATH-C20` | 2 | `distrib_incomplete` |
| **Ch 12** | Factorisation | `MATH-C28` | `DIV_ALG` | Division of Algebraic Polynomials | `MATH-C27` | 2 | `like_terms`, `sign_error` |
| **Ch 13** | Introduction to Graphs | `MATH-C29` | `CART_PLANE` | Cartesian Plane & Coordinates | `MATH-C01` | 2 | `sign_error` |
| **Ch 13** | Introduction to Graphs | `MATH-C30` | `LIN_GRAPH` | Reading & Interpreting Linear Graphs | `MATH-C29`, `MATH-C05` | 2 | `sub_calc_error`, `inverse_conf` |

---

## Pedagogical Validation
1. **Total Registered Concepts:** 30 Concepts across 13 Official Chapters.
2. **Total Diagnostic Items:** 81 Validated Questions with distractor-misconception tagging.
3. **Directed Acyclic Graph (DAG) Invariant:** Formally verified acyclic through DFS topological traversal (`backend/tests/test_content.py::test_prerequisite_graph_acyclic`).
4. **Adaptive Remediation Mappings:** Every misconception tag maps directly to its upstream foundational concept in `MISCONCEPTION_TO_PREREQUISITE_MAP`.

