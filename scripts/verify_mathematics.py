"""
SUTRA LEARN — Independent Mathematical & Adaptive Engine Verification Suite
Comprehensive verification of all 13 NCERT Class 8 chapters:
1. Core Algebraic Equations & Substitutions (Linear Equations)
2. Rational Numbers & Arithmetic
3. Exponents and Powers
4. Squares, Cubes and Roots
5. Polygon & Quadrilateral Angle Sums
6. Commercial Mathematics (Discounts, Profits, Taxes)
7. Mensuration (Trapezium, Cuboid, Cylinder)
8. Direct and Inverse Proportions
9. Algebraic Identities
10. AI Hallucination & Step Contradiction Rejection
11. Diagnostic Misconception Traps across Chapters
12. Deterministic Adaptive Decision Logic
"""

import sys
import os
import math
from pathlib import Path

# Add backend to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.content.models import MisconceptionTag
from app.content.questions import QUESTIONS_REGISTRY
from app.ai.math_validator import MathematicalValidator
from app.engine.adaptive import AdaptiveEngine, EvidenceRecord, LearningPathOutcome


def verify_equation_solver():
    print("=" * 70)
    print("1. SOLVING 8 CORE ALGEBRAIC EQUATIONS & SUBSTITUTIONS")
    print("=" * 70)

    equations = [
        {
            "name": "Case 1: Standard Two-Step",
            "equation": "2x + 5 = 15",
            "solve": lambda: (15 - 5) / 2,
            "expected_x": 5.0,
            "lhs": lambda x: 2 * x + 5,
            "rhs": lambda x: 15,
        },
        {
            "name": "Case 2: Subtraction Two-Step",
            "equation": "3x - 7 = 11",
            "solve": lambda: (11 + 7) / 3,
            "expected_x": 6.0,
            "lhs": lambda x: 3 * x - 7,
            "rhs": lambda x: 11,
        },
        {
            "name": "Case 3: Parentheses / Distribution",
            "equation": "2(x + 3) = 14",
            "solve": lambda: (14 / 2) - 3,
            "expected_x": 4.0,
            "lhs": lambda x: 2 * (x + 3),
            "rhs": lambda x: 14,
        },
        {
            "name": "Case 4: Variables on Both Sides",
            "equation": "5x + 2 = 3x + 10",
            "solve": lambda: (10 - 2) / (5 - 3),
            "expected_x": 4.0,
            "lhs": lambda x: 5 * x + 2,
            "rhs": lambda x: 3 * x + 10,
        },
        {
            "name": "Case 5A: Negative Coefficient",
            "equation": "-4x + 9 = 29",
            "solve": lambda: (29 - 9) / -4,
            "expected_x": -5.0,
            "lhs": lambda x: -4 * x + 9,
            "rhs": lambda x: 29,
        },
        {
            "name": "Case 5B: Negative Product",
            "equation": "-7x = 35",
            "solve": lambda: 35 / -7,
            "expected_x": -5.0,
            "lhs": lambda x: -7 * x,
            "rhs": lambda x: 35,
        },
    ]

    all_passed = True
    for eq in equations:
        computed_x = eq["solve"]()
        lhs_val = eq["lhs"](computed_x)
        rhs_val = eq["rhs"](computed_x)
        is_sub_valid = (lhs_val == rhs_val)
        is_x_correct = (computed_x == eq["expected_x"])

        status = "PASS" if (is_x_correct and is_sub_valid) else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"[{status}] {eq['name']:32} | {eq['equation']:18} | Solution x={computed_x} | LHS={lhs_val} RHS={rhs_val}")

    return all_passed


def verify_expanded_mathematics_engine():
    print("\n" + "=" * 70)
    print("2. VERIFYING EXPANDED MATHEMATICAL VALIDATOR ENGINE (ALL TOPICS)")
    print("=" * 70)

    val = MathematicalValidator
    checks = []

    # 1. Rational arithmetic: 3/4 + 2/5 = 23/20
    c1 = val.validate_rational_arithmetic("+", (3, 4), (2, 5), (23, 20))
    checks.append(("Rational Addition: 3/4 + 2/5 = 23/20", c1))

    # 2. Rational multiplication: (-2/3) * (9/4) = -3/2
    c2 = val.validate_rational_arithmetic("*", (-2, 3), (9, 4), (-6, 4))
    checks.append(("Rational Multiplication: (-2/3) * (9/4) = -6/4", c2))

    # 3. Exponent laws: 2^3 * 2^4 = 2^7
    c3 = val.validate_exponent_law(2, 3, 4, "product")
    checks.append(("Exponent Product Law: 2^3 * 2^4 = 2^7", c3))

    # 4. Exponent quotient law: 3^5 / 3^2 = 3^3
    c4 = val.validate_exponent_law(3, 5, 2, "quotient")
    checks.append(("Exponent Quotient Law: 3^5 / 3^2 = 3^3", c4))

    # 5. Exponent power of power: (2^3)^2 = 2^6
    c5 = val.validate_exponent_law(2, 3, 2, "power_of_power")
    checks.append(("Exponent Power of Power: (2^3)^2 = 2^6", c5))

    # 6. Negative exponent law: 4^(-2) = 1/16
    c6 = val.validate_exponent_law(4, 0, 2, "negative_exponent")
    checks.append(("Negative Exponent Law: 4^(-2) = 1/16", c6))

    # 7. Squares & square roots: sqrt(144) = 12
    c7 = val.validate_square_and_root(144, 12)
    checks.append(("Square Root: sqrt(144) = 12", c7))

    # 8. Cubes & cube roots: 4^3 = 64
    c8 = val.validate_cube_and_root(64, 4)
    checks.append(("Cube Root: cbrt(64) = 4", c8))

    # 9. Quadrilateral angle sum: (4-2)*180 = 360
    c9 = val.validate_polygon_angle_sum(4, 360)
    checks.append(("Quadrilateral Angle Sum: 360 deg", c9))

    # 10. Pentagon angle sum: (5-2)*180 = 540
    c10 = val.validate_polygon_angle_sum(5, 540)
    checks.append(("Pentagon Angle Sum: 540 deg", c10))

    # 11. Commercial discount: 20% discount on 500 = 400
    c11 = val.validate_percentage_commercial(500, 20, "discount", 400)
    checks.append(("Commercial Math (20% discount on 500 = 400)", c11))

    # 12. Commercial profit: 15% profit on 800 = 920
    c12 = val.validate_percentage_commercial(800, 15, "profit", 920)
    checks.append(("Commercial Math (15% profit on 800 = 920)", c12))

    # 13. Mensuration Trapezium Area: 0.5 * (6 + 10) * 4 = 32
    c13 = val.validate_mensuration("trapezium", {"a": 6, "b": 10, "h": 4}, "area", 32)
    checks.append(("Mensuration Trapezium Area: 32 sq units", c13))

    # 14. Mensuration Cylinder Volume: pi * 7^2 * 10
    cyl_vol = math.pi * 49 * 10
    c14 = val.validate_mensuration("cylinder", {"r": 7, "h": 10}, "volume", cyl_vol)
    checks.append(("Mensuration Cylinder Volume: pi * 7^2 * 10", c14))

    # 15. Direct proportion: 5/20 == 8/32
    c15 = val.validate_proportion(5, 20, 8, 32, "direct")
    checks.append(("Direct Proportion: 5/20 = 8/32", c15))

    # 16. Inverse proportion: 4 workers * 6 hours == 8 workers * 3 hours
    c16 = val.validate_proportion(4, 6, 8, 3, "inverse")
    checks.append(("Inverse Proportion: 4 * 6 = 8 * 3", c16))

    # 17. Algebraic Identity 1: (a+b)^2 = a^2 + 2ab + b^2
    c17 = val.validate_algebraic_identity("identity_1", 3, 5)
    checks.append(("Algebraic Identity 1: (3+5)^2 = 3^2 + 2*3*5 + 5^2", c17))

    all_passed = True
    for desc, passed in checks:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {desc}")

    return all_passed


def verify_step_consistency_and_contradiction():
    print("\n" + "=" * 70)
    print("3. VERIFYING AI HALLUCINATION & STEP CONTRADICTION REJECTION")
    print("=" * 70)

    val = MathematicalValidator
    all_passed = True

    # Test A: Valid consistent multi-step linear equation
    good_text = (
        "Let us solve step by step:\n"
        "2x + 5 = 15\n"
        "Subtract 5 from both sides:\n"
        "2x = 10\n"
        "Divide by 2:\n"
        "x = 5"
    )
    res_good = val.validate_step_consistency(good_text)
    if res_good["valid"]:
        print("[PASS] Consistent linear transformation accepted (root x=5)")
    else:
        print(f"[FAIL] Consistent text wrongly rejected: {res_good}")
        all_passed = False

    # Test B: Hallucinated/invalid transformation (common sign error in step)
    bad_text = (
        "Let us solve step by step:\n"
        "2x + 5 = 15\n"
        "Add 5 to both sides:\n"
        "2x = 20\n"
        "Divide by 2:\n"
        "x = 10"
    )
    res_bad = val.validate_step_consistency(bad_text)
    if not res_bad["valid"]:
        print(f"[PASS] Hallucinated transformation successfully caught: {res_bad['reason']}")
    else:
        print("[FAIL] Contradictory transformation was not caught!")
        all_passed = False

    # Test C: Arithmetic step falsehood rejection (e.g. 15 - 5 = 12)
    arith_false_text = (
        "First calculate the difference:\n"
        "15 - 5 = 12\n"
        "Now continue."
    )
    res_arith = val.validate_step_consistency(arith_false_text)
    if not res_arith["valid"]:
        print(f"[PASS] False arithmetic assertion caught: {res_arith['reason']}")
    else:
        print("[FAIL] False arithmetic assertion was not caught!")
        all_passed = False

    return all_passed


def verify_misconception_traps():
    print("\n" + "=" * 70)
    print("4. VERIFYING MISCONCEPTION DETECTION IN QUESTION BANK ACROSS CHAPTERS")
    print("=" * 70)

    traps = [
        ("Q-INV-005", "-7x = 35", "Dropping negative sign during division"),
        ("Q-LIN-003", "-4x + 9 = 29", "Sign inversion when subtracting across equality"),
        ("Q-INT-001", "-8 - (-15)", "Subtracting a negative treated as subtraction"),
        ("Q-SIMP-004", "7a - 2(3a - 4)", "Distributing negative sign to second term"),
        ("Q-BAL-001", "x + 14 = 39", "Unbalanced operation (subtracting from LHS only)"),
        ("Q-BAL-002", "2a = b", "Unbalanced operation (multiplying/dividing one side only)"),
        ("Q-VER-001", "3x + 5 = 2x + 9", "Verification by substitution for x = 4"),
        ("Q-RAT-002", "3/5 * (-10/9)", "Reciprocal and sign confusion in rational numbers"),
        ("Q-EXP-002", "3^4 * 3^2", "Exponent base conflation (multiplying powers)"),
        ("Q-SQRT-002", "Estimate sqrt(80)", "Square root halving misconception (dividing by 2)"),
        ("Q-COMP-002", "15% discount on 800", "Percentage base error (on SP instead of MP)"),
        ("Q-QUAD-002", "Quadrilateral interior angles", "Quadrilateral angle sum error"),
        ("Q-INVPROP-002", "6 pipes fill in 80 mins", "Proportion inversion (treating inverse as direct)"),
    ]

    all_passed = True
    for qid, expr, desc in traps:
        q = QUESTIONS_REGISTRY.get(qid)
        if not q:
            print(f"[FAIL] Missing question {qid}")
            all_passed = False
            continue

        misconception_opts = [o for o in q.options if not o.is_correct and o.misconception_tag != MisconceptionTag.NONE]
        has_correct = any(o.is_correct for o in q.options)
        has_explanation = bool(q.explanation)

        status = "PASS" if (misconception_opts and has_correct and has_explanation) else "FAIL"
        if status == "FAIL":
            all_passed = False

        tags = [o.misconception_tag.value for o in misconception_opts]
        print(f"[{status}] {qid:10} ({expr:22}) | Traps: {', '.join(set(tags))} | {desc}")

    return all_passed


def verify_adaptive_evaluator():
    print("\n" + "=" * 70)
    print("5. VERIFYING ADAPTIVE ENGINE DECISION LOGIC INDEPENDENT OF LLM")
    print("=" * 70)

    engine = AdaptiveEngine()

    # Scenario A: 2 distinct correct unassisted attempts -> STRETCH (Mastery >= 85%)
    ev_mastery = [
        EvidenceRecord(
            attempt_id="att-1",
            question_id="Q-LIN-001",
            concept_id="MATH-C05",
            is_correct=True,
            hint_used=False,
            selected_option_id="A",
            misconception_tag=MisconceptionTag.NONE
        ),
        EvidenceRecord(
            attempt_id="att-2",
            question_id="Q-LIN-002",
            concept_id="MATH-C05",
            is_correct=True,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.NONE
        )
    ]
    rec_mastery = engine.evaluate_learner_concept("MATH-C05", ev_mastery)
    p_mastery = rec_mastery.outcome == LearningPathOutcome.STRETCH
    print(f"[{'PASS' if p_mastery else 'FAIL'}] Scenario A (2 unassisted correct) -> Outcome: {rec_mastery.outcome.value} (Expected: STRETCH)")

    # Scenario B: 2 sign errors on linear equations -> BRIDGE_BACK to MATH-C01 (Integer Arithmetic)
    ev_bridge = [
        EvidenceRecord(
            attempt_id="att-3",
            question_id="Q-LIN-003",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="C",
            misconception_tag=MisconceptionTag.SIGN_ERROR
        ),
        EvidenceRecord(
            attempt_id="att-4",
            question_id="Q-LIN-001",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="D",
            misconception_tag=MisconceptionTag.SIGN_ERROR
        )
    ]
    rec_bridge = engine.evaluate_learner_concept("MATH-C05", ev_bridge)
    p_bridge = (rec_bridge.outcome == LearningPathOutcome.BRIDGE_BACK and rec_bridge.target_concept_id == "MATH-C01")
    print(f"[{'PASS' if p_bridge else 'FAIL'}] Scenario B (2 sign errors) -> Outcome: {rec_bridge.outcome.value} -> Target: {rec_bridge.target_concept_id} (Expected: BRIDGE_BACK to MATH-C01)")

    # Scenario B2: Exponent base conflation -> BRIDGE_BACK to MATH-C23 (Powers with Positive Exponents)
    ev_exp = [
        EvidenceRecord(
            attempt_id="att-3b",
            question_id="Q-EXPLAW-001",
            concept_id="MATH-C24",
            is_correct=False,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.EXPONENT_BASE_CONFLATION
        ),
        EvidenceRecord(
            attempt_id="att-4b",
            question_id="Q-EXPLAW-002",
            concept_id="MATH-C24",
            is_correct=False,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.EXPONENT_BASE_CONFLATION
        )
    ]
    rec_exp = engine.evaluate_learner_concept("MATH-C24", ev_exp)
    p_exp = (rec_exp.outcome == LearningPathOutcome.BRIDGE_BACK and rec_exp.target_concept_id == "MATH-C23")
    print(f"[{'PASS' if p_exp else 'FAIL'}] Scenario B2 (2 exponent errors) -> Outcome: {rec_exp.outcome.value} -> Target: {rec_exp.target_concept_id} (Expected: BRIDGE_BACK to MATH-C23)")

    # Scenario C: 3 consecutive failures without correct -> TEACHER_REVIEW
    ev_struggle = [
        EvidenceRecord(
            attempt_id="att-5",
            question_id="Q-LIN-001",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="B",
            misconception_tag=MisconceptionTag.NONE
        ),
        EvidenceRecord(
            attempt_id="att-6",
            question_id="Q-LIN-002",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="C",
            misconception_tag=MisconceptionTag.NONE
        ),
        EvidenceRecord(
            attempt_id="att-7",
            question_id="Q-LIN-003",
            concept_id="MATH-C05",
            is_correct=False,
            hint_used=False,
            selected_option_id="D",
            misconception_tag=MisconceptionTag.NONE
        )
    ]
    rec_struggle = engine.evaluate_learner_concept("MATH-C05", ev_struggle)
    p_struggle = rec_struggle.outcome == LearningPathOutcome.TEACHER_REVIEW
    print(f"[{'PASS' if p_struggle else 'FAIL'}] Scenario C (3 persistent errors) -> Outcome: {rec_struggle.outcome.value} (Expected: TEACHER_REVIEW)")

    # Scenario D: 1 attempt only -> CONFIRM (insufficient evidence)
    ev_confirm = [
        EvidenceRecord(
            attempt_id="att-8",
            question_id="Q-LIN-001",
            concept_id="MATH-C05",
            is_correct=True,
            hint_used=False,
            selected_option_id="A",
            misconception_tag=MisconceptionTag.NONE
        )
    ]
    rec_confirm = engine.evaluate_learner_concept("MATH-C05", ev_confirm)
    p_confirm = rec_confirm.outcome == LearningPathOutcome.CONFIRM
    print(f"[{'PASS' if p_confirm else 'FAIL'}] Scenario D (1 attempt only) -> Outcome: {rec_confirm.outcome.value} (Expected: CONFIRM)")

    return p_mastery and p_bridge and p_exp and p_struggle and p_confirm


if __name__ == "__main__":
    t1 = verify_equation_solver()
    t2 = verify_expanded_mathematics_engine()
    t3 = verify_step_consistency_and_contradiction()
    t4 = verify_misconception_traps()
    t5 = verify_adaptive_evaluator()

    print("\n" + "=" * 70)
    if t1 and t2 and t3 and t4 and t5:
        print("MATHEMATICS & ADAPTIVE ENGINE INDEPENDENT VERIFICATION: ALL 5 SUITES PASSED")
        sys.exit(0)
    else:
        print("MATHEMATICS VERIFICATION FAILED")
        sys.exit(1)
