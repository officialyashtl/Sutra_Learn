"""
SUTRA LEARN - Comprehensive Validated Question Bank (Class 8 Mathematics)
Target: Linear Equations in One Variable and Foundational Prerequisite Progression.
All 30+ questions contain mathematically verified solutions, misconception-tagged distractors,
hints, step-by-step explanations, cognitive demand classifications, and prerequisite dependencies.
"""

from typing import List, Dict
from .models import Question, Option, CognitiveDemand, MisconceptionTag

QUESTIONS_REGISTRY: Dict[str, Question] = {
    # =========================================================================
    # CONCEPT 1: MATH-C01 (Integer Arithmetic)
    # =========================================================================
    "Q-INT-001": Question(
        id="Q-INT-001",
        concept_id="MATH-C01",
        prerequisite_ids=[],
        prompt="Evaluate the following integer subtraction:",
        equation_display="-8 - (-15)",
        options=[
            Option(id="A", text="7", is_correct=True),
            Option(id="B", text="-23", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Treated -(-15) as subtracting 15 instead of adding 15: -8 - 15 = -23."),
            Option(id="C", text="-7", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Assigned negative sign to the larger magnitude instead of positive 15 - 8 = 7."),
            Option(id="D", text="23", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Discarded negative signs entirely: 8 + 15 = 23."),
        ],
        correct_option_id="A",
        hint="Subtracting a negative number is equivalent to adding its positive opposite: a - (-b) = a + b.",
        explanation="Step 1: Rewrite subtraction of negative: -8 - (-15) = -8 + 15.\nStep 2: Since 15 > 8, result is positive: 15 - 8 = 7.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1,
        content_version="1.0.0"
    ),

    "Q-INT-002": Question(
        id="Q-INT-002",
        concept_id="MATH-C01",
        prerequisite_ids=[],
        prompt="Which of the following calculations yields a NEGATIVE result?",
        equation_display="Compare: (-4) * (-6), (-18) / (-3), (-5) * 3, -10 + 14",
        options=[
            Option(id="A", text="(-4) * (-6)", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Multiplying two negative numbers produces a positive product (+24)."),
            Option(id="B", text="(-18) / (-3)", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Dividing a negative by a negative produces a positive quotient (+6)."),
            Option(id="C", text="(-5) * 3", is_correct=True),
            Option(id="D", text="-10 + 14", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Adding 14 to -10 yields positive 4."),
        ],
        correct_option_id="C",
        hint="Multiplying numbers with DIFFERENT signs always yields a negative product.",
        explanation="(-5) * 3 has one negative and one positive factor. Therefore the product is negative: (-5) * 3 = -15.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=1,
        content_version="1.0.0"
    ),

    "Q-INT-003": Question(
        id="Q-INT-003",
        concept_id="MATH-C01",
        prerequisite_ids=[],
        prompt="Simplify the three-term signed expression:",
        equation_display="-12 + (-7) - (-4)",
        options=[
            Option(id="A", text="-15", is_correct=True),
            Option(id="B", text="-23", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Treated -(-4) as -4, calculating -12 - 7 - 4 = -23."),
            Option(id="C", text="-1", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Subtracted magnitudes incorrectly."),
            Option(id="D", text="15", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Reversed the overall sign."),
        ],
        correct_option_id="A",
        hint="Work from left to right: first compute -12 + (-7) = -19, then evaluate -19 - (-4).",
        explanation="Step 1: -12 + (-7) = -19.\nStep 2: -19 - (-4) = -19 + 4 = -15.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-INT-004": Question(
        id="Q-INT-004",
        concept_id="MATH-C01",
        prerequisite_ids=[],
        prompt="Compute the quotient of two signed integers:",
        equation_display="(-42) / (-7)",
        options=[
            Option(id="A", text="6", is_correct=True),
            Option(id="B", text="-6", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Thought dividing two negatives resulted in a negative."),
            Option(id="C", text="-35", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Subtracted 7 instead of dividing."),
            Option(id="D", text="7", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Division arithmetic error: 42 / 7 = 6, not 7."),
        ],
        correct_option_id="A",
        hint="A negative number divided by a negative number yields a POSITIVE quotient.",
        explanation="(-42) / (-7) = +(42 / 7) = 6.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1,
        content_version="1.0.0"
    ),

    "Q-INT-005": Question(
        id="Q-INT-005",
        concept_id="MATH-C01",
        prerequisite_ids=[],
        prompt="Evaluate using correct order of operations (brackets first):",
        equation_display="-3 * (4 - 9)",
        options=[
            Option(id="A", text="15", is_correct=True),
            Option(id="B", text="-15", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Forgot that multiplying -3 by -5 gives positive 15."),
            Option(id="C", text="-39", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Computed -3 * 4 = -12, then -12 - 9 = -21 or -39 without proper signs."),
            Option(id="D", text="3", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Arithmetic error in bracket."),
        ],
        correct_option_id="A",
        hint="Inside brackets: 4 - 9 = -5. Then multiply -3 by -5.",
        explanation="Step 1: Simplify inside brackets: 4 - 9 = -5.\nStep 2: Multiply: (-3) * (-5) = 15.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    # =========================================================================
    # CONCEPT 2: MATH-C02 (Equality and Balance Principle)
    # =========================================================================
    "Q-BAL-001": Question(
        id="Q-BAL-001",
        concept_id="MATH-C02",
        prerequisite_ids=["MATH-C01"],
        prompt="A student has the balanced equation below. To isolate x on the left side, what operation MUST be performed to keep the equation balanced?",
        equation_display="x + 14 = 39",
        options=[
            Option(id="A", text="Subtract 14 from the left side only", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Operating on only one side unbalances the equation."),
            Option(id="B", text="Subtract 14 from BOTH sides", is_correct=True),
            Option(id="C", text="Add 14 to both sides", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Adding 14 increases the left side constant to 28 instead of isolating x."),
            Option(id="D", text="Divide both sides by 14", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="14 is added to x; division does not undo addition."),
        ],
        correct_option_id="B",
        hint="By the Subtraction Property of Equality, whatever you subtract from one side must be subtracted from the other.",
        explanation="To eliminate +14 from the LHS, subtract 14. To maintain the equality balance, subtract 14 from both sides: x = 39 - 14 = 25.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-BAL-002": Question(
        id="Q-BAL-002",
        concept_id="MATH-C02",
        prerequisite_ids=["MATH-C01"],
        prompt="If 2a = b, which of the following operations maintains equality?",
        equation_display="2a = b",
        options=[
            Option(id="A", text="2a + 5 = b + 5", is_correct=True),
            Option(id="B", text="2a + 5 = b", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Added 5 only to the left side."),
            Option(id="C", text="2a * 3 = b + 3", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Multiplied LHS by 3 but added 3 to RHS; different operations destroy balance."),
            Option(id="D", text="2a - 4 = b + 4", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Subtracted on LHS but added on RHS."),
        ],
        correct_option_id="A",
        hint="Both sides must receive the identical mathematical operation with the identical value.",
        explanation="Adding the exact same number (5) to both sides preserves balance: 2a + 5 = b + 5.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-BAL-003": Question(
        id="Q-BAL-003",
        concept_id="MATH-C02",
        prerequisite_ids=["MATH-C01"],
        prompt="Given 4x = 28, which balance step isolates x?",
        equation_display="4x = 28",
        options=[
            Option(id="A", text="Divide both sides by 4", is_correct=True),
            Option(id="B", text="Subtract 4 from both sides", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="4 is multiplied by x; subtraction does not undo multiplication."),
            Option(id="C", text="Divide LHS by 4 and RHS by 7", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Dividing sides by different divisors destroys the equality balance."),
            Option(id="D", text="Multiply both sides by 4", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Multiplying produces 16x on the left instead of isolating x."),
        ],
        correct_option_id="A",
        hint="The variable x is multiplied by 4. To isolate x while maintaining equality, divide BOTH sides by 4.",
        explanation="Dividing both sides by 4 gives (4x)/4 = 28/4, which simplifies to x = 7.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1,
        content_version="1.0.0"
    ),

    "Q-BAL-004": Question(
        id="Q-BAL-004",
        concept_id="MATH-C02",
        prerequisite_ids=["MATH-C01"],
        prompt="A pan balance scale holds 2 equal blocks and a 3 kg weight on the left pan, balancing 11 kg on the right. What represents the state of balance after removing the 3 kg weight?",
        equation_display="2b + 3 = 11",
        options=[
            Option(id="A", text="2b = 8", is_correct=True),
            Option(id="B", text="2b = 11", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Removed 3 kg from the left pan only, tipping the scale."),
            Option(id="C", text="2b = 14", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added 3 to the right side instead of removing 3: 11 + 3 = 14."),
            Option(id="D", text="b = 8", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Removed coefficient 2 prematurely."),
        ],
        correct_option_id="A",
        hint="If you remove 3 kg from the left pan, you must remove 3 kg from the right pan to keep the scale level: 11 - 3.",
        explanation="Subtracting 3 from both pans maintains balance: 2b + 3 - 3 = 11 - 3, yielding 2b = 8.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-BAL-005": Question(
        id="Q-BAL-005",
        concept_id="MATH-C02",
        prerequisite_ids=["MATH-C01"],
        prompt="Which of the following is an INVALID equation transformation that breaks equality?",
        equation_display="Start: 3x - 2 = 10",
        options=[
            Option(id="A", text="3x = 10 - 2", is_correct=True, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Transposed -2 as -2 instead of adding +2 to RHS: 3x should equal 10 + 2 = 12."),
            Option(id="B", text="3x - 2 + 2 = 10 + 2", is_correct=False),
            Option(id="C", text="3x = 12", is_correct=False),
            Option(id="D", text="(3x - 2) * 2 = 10 * 2", is_correct=False),
        ],
        correct_option_id="A",
        hint="Adding 2 to LHS undoes -2. To preserve balance, you must ADD 2 to RHS, not subtract 2.",
        explanation="If you add 2 to both sides, the RHS becomes 10 + 2 = 12. Writing 3x = 10 - 2 = 8 is mathematically invalid.",
        cognitive_demand=CognitiveDemand.TRANSFER,
        difficulty=2,
        content_version="1.0.0"
    ),

    # =========================================================================
    # CONCEPT 3: MATH-C03 (Inverse Operations)
    # =========================================================================
    "Q-INV-001": Question(
        id="Q-INV-001",
        concept_id="MATH-C03",
        prerequisite_ids=["MATH-C01"],
        prompt="In the equation below, what is the FIRST inverse operation to apply to isolate y efficiently?",
        equation_display="3y - 8 = 19",
        options=[
            Option(id="A", text="Add 8 to both sides", is_correct=True),
            Option(id="B", text="Divide both sides by 3", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Dividing first produces fractions (8/3) and introduces unneeded complexity."),
            Option(id="C", text="Subtract 8 from both sides", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="The inverse of subtracting 8 is ADDING 8."),
            Option(id="D", text="Multiply both sides by 3", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="y is already multiplied by 3; multiplying by 3 makes it 9y."),
        ],
        correct_option_id="A",
        hint="Undo addition or subtraction before undoing multiplication or division.",
        explanation="In reverse order of operations, first undo the subtraction of 8 by adding 8 to both sides: 3y = 27.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-INV-002": Question(
        id="Q-INV-002",
        concept_id="MATH-C03",
        prerequisite_ids=["MATH-C01"],
        prompt="Solve for m by applying the correct inverse operation:",
        equation_display="m / (-4) = 7",
        options=[
            Option(id="A", text="m = -28", is_correct=True),
            Option(id="B", text="m = 28", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Lost the negative sign: 7 * (-4) is -28, not +28."),
            Option(id="C", text="m = -11", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Subtracted 4 instead of multiplying by -4."),
            Option(id="D", text="m = 3", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Added -4 instead of multiplying."),
        ],
        correct_option_id="A",
        hint="The variable m is divided by -4. The inverse of dividing by -4 is multiplying both sides by -4.",
        explanation="Multiply both sides by -4: m = 7 * (-4) = -28.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-INV-003": Question(
        id="Q-INV-003",
        concept_id="MATH-C03",
        prerequisite_ids=["MATH-C01"],
        prompt="In 5 + 2x = 17, which sequence of inverse operations isolates x?",
        equation_display="5 + 2x = 17",
        options=[
            Option(id="A", text="First subtract 5, then divide by 2", is_correct=True),
            Option(id="B", text="First divide by 2, then subtract 5", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Dividing first requires dividing 5 by 2 into a fraction 2.5."),
            Option(id="C", text="First add 5, then multiply by 2", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Used same operations instead of their inverses."),
            Option(id="D", text="First subtract 2, then divide by 5", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Confused coefficient 2 with constant 5."),
        ],
        correct_option_id="A",
        hint="Constant 5 is added to 2x. Subtract 5 first (17 - 5 = 12), then divide by coefficient 2.",
        explanation="Step 1: Subtract 5: 2x = 12. Step 2: Divide by 2: x = 6.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-INV-004": Question(
        id="Q-INV-004",
        concept_id="MATH-C03",
        prerequisite_ids=["MATH-C01"],
        prompt="Solve for p where the expression in parentheses is divided by 3:",
        equation_display="(p - 4) / 3 = 5",
        options=[
            Option(id="A", text="p = 19", is_correct=True),
            Option(id="B", text="p = 11", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Subtracted 4 from 15 instead of adding 4: 15 - 4 = 11."),
            Option(id="C", text="p = 9", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Added 4 to 5 first without clearing the denominator 3."),
            Option(id="D", text="p = 15", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Multiplied 3 * 5 = 15 but forgot to add 4."),
        ],
        correct_option_id="A",
        hint="Because the entire (p - 4) is divided by 3, first clear the denominator by multiplying both sides by 3.",
        explanation="Step 1: Multiply both sides by 3: p - 4 = 15.\nStep 2: Add 4 to both sides: p = 15 + 4 = 19.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-INV-005": Question(
        id="Q-INV-005",
        concept_id="MATH-C03",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the inverse operation needed to eliminate -7 when it is multiplied by x in -7x = 35?",
        equation_display="-7x = 35",
        options=[
            Option(id="A", text="Divide both sides by -7", is_correct=True),
            Option(id="B", text="Add 7 to both sides", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="-7 is multiplied by x, not subtracted; addition does not undo multiplication."),
            Option(id="C", text="Divide both sides by +7", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Dividing by +7 leaves -x instead of isolating positive x."),
            Option(id="D", text="Multiply both sides by -7", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Multiplying yields 49x."),
        ],
        correct_option_id="A",
        hint="The coefficient is -7. To isolate +x, divide by the entire coefficient including its sign: -7.",
        explanation="Dividing (-7x) by (-7) isolates x = 35 / (-7) = -5.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    # =========================================================================
    # CONCEPT 4: MATH-C04 (Simplifying Algebraic Expressions)
    # =========================================================================
    "Q-SIMP-001": Question(
        id="Q-SIMP-001",
        concept_id="MATH-C04",
        prerequisite_ids=["MATH-C01"],
        prompt="Simplify the algebraic expression completely:",
        equation_display="4(2x - 3) - 5x + 7",
        options=[
            Option(id="A", text="3x - 5", is_correct=True),
            Option(id="B", text="3x + 5", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Computed -12 + 7 as +5 instead of -5."),
            Option(id="C", text="3x - 19", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added -12 and -7 instead of adding +7 to -12."),
            Option(id="D", text="3x + 4", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Distributed 4 to 2x but failed to distribute 4 to -3: 8x - 3 - 5x + 7 = 3x + 4."),
        ],
        correct_option_id="A",
        hint="First use distributive property: 4 * 2x and 4 * (-3). Then collect like terms.",
        explanation="Step 1: Distribute 4: 8x - 12 - 5x + 7.\nStep 2: Group like terms: (8x - 5x) + (-12 + 7) = 3x - 5.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-SIMP-002": Question(
        id="Q-SIMP-002",
        concept_id="MATH-C04",
        prerequisite_ids=["MATH-C01"],
        prompt="Which of the following demonstrates the COMMON ERROR of combining unlike terms?",
        equation_display="Identify the invalid simplification:",
        options=[
            Option(id="A", text="5x + 3 = 8x", is_correct=True, misconception_tag=MisconceptionTag.LIKE_TERMS_CONFLATION, misconception_explanation="A variable term (5x) cannot be added to a scalar constant (3) to make 8x."),
            Option(id="B", text="5x + 3x = 8x", is_correct=False),
            Option(id="C", text="5(x + 3) = 5x + 15", is_correct=False),
            Option(id="D", text="7x - 4x + 2 = 3x + 2", is_correct=False),
        ],
        correct_option_id="A",
        hint="Terms can only be combined if they share the exact same variable part. Constants and variables cannot merge.",
        explanation="5x and 3 are unlike terms. 5x + 3 cannot be reduced to 8x.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-SIMP-003": Question(
        id="Q-SIMP-003",
        concept_id="MATH-C04",
        prerequisite_ids=["MATH-C01"],
        prompt="Simplify the expression with a negative outside parentheses:",
        equation_display="-(2x - 5) + 3(x - 1)",
        options=[
            Option(id="A", text="x + 2", is_correct=True),
            Option(id="B", text="x - 8", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Computed -(2x - 5) as -2x - 5 instead of -2x + 5."),
            Option(id="C", text="5x + 2", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added 2x and 3x instead of -2x + 3x."),
            Option(id="D", text="x - 2", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Calculation error on constants +5 - 3."),
        ],
        correct_option_id="A",
        hint="Remember: -(2x - 5) = -2x + 5. Watch the double negative on -(-5).",
        explanation="Step 1: Expand: -2x + 5 + 3x - 3.\nStep 2: Combine: (-2x + 3x) + (5 - 3) = x + 2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-SIMP-004": Question(
        id="Q-SIMP-004",
        concept_id="MATH-C04",
        prerequisite_ids=["MATH-C01"],
        prompt="Simplify by distributing -2 carefully:",
        equation_display="7a - 2(3a - 4)",
        options=[
            Option(id="A", text="a + 8", is_correct=True),
            Option(id="B", text="a - 8", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Computed -2 * (-4) as -8 instead of +8."),
            Option(id="C", text="13a - 8", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added 7a + 6a instead of 7a - 6a."),
            Option(id="D", text="a - 4", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Did not multiply -2 by -4."),
        ],
        correct_option_id="A",
        hint="Distribute -2 into (3a - 4): (-2) * (3a) = -6a, and (-2) * (-4) = +8.",
        explanation="Step 1: 7a - 6a + 8.\nStep 2: (7a - 6a) + 8 = a + 8.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-SIMP-005": Question(
        id="Q-SIMP-005",
        concept_id="MATH-C04",
        prerequisite_ids=["MATH-C01"],
        prompt="Find the simplified expression for the perimeter of a rectangle with length (2x + 1) and width (x - 3):",
        equation_display="Perimeter = 2 * (length + width) = 2 * [(2x + 1) + (x - 3)]",
        options=[
            Option(id="A", text="6x - 4", is_correct=True),
            Option(id="B", text="3x - 2", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Added length and width but forgot to multiply by 2 for total perimeter."),
            Option(id="C", text="6x - 2", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Multiplied 3x by 2 to get 6x, but forgot to multiply -2 by 2."),
            Option(id="D", text="6x + 4", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Computed 1 - 3 as +2 instead of -2."),
        ],
        correct_option_id="A",
        hint="First simplify inside brackets: (2x + 1) + (x - 3) = 3x - 2. Then multiply by 2.",
        explanation="Step 1: Inside brackets: 2x + x + 1 - 3 = 3x - 2.\nStep 2: Multiply by 2: 2(3x - 2) = 6x - 4.",
        cognitive_demand=CognitiveDemand.TRANSFER,
        difficulty=3,
        content_version="1.0.0"
    ),

    # =========================================================================
    # CONCEPT 5: MATH-C05 (Solving Simple Linear Equations)
    # =========================================================================
    "Q-LIN-001": Question(
        id="Q-LIN-001",
        concept_id="MATH-C05",
        prerequisite_ids=["MATH-C02", "MATH-C03", "MATH-C04"],
        prompt="Solve the linear equation for x:",
        equation_display="5x - 8 = 2x + 13",
        options=[
            Option(id="A", text="x = 7", is_correct=True),
            Option(id="B", text="x = 5/3", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Subtracted 8 from 13 instead of adding 8: 13 - 8 = 5."),
            Option(id="C", text="x = 3", is_correct=False, misconception_tag=MisconceptionTag.UNBALANCED_OPERATION, misconception_explanation="Added 2x instead of subtracting 2x."),
            Option(id="D", text="x = -7", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Sign reversal during isolation."),
        ],
        correct_option_id="A",
        hint="Collect all terms containing x on one side, and all constants on the other.",
        explanation="Step 1: Subtract 2x: 3x - 8 = 13.\nStep 2: Add 8: 3x = 21.\nStep 3: Divide by 3: x = 7.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-LIN-002": Question(
        id="Q-LIN-002",
        concept_id="MATH-C05",
        prerequisite_ids=["MATH-C02", "MATH-C03", "MATH-C04"],
        prompt="Solve the equation involving parentheses on both sides:",
        equation_display="3(x - 4) = 2(x + 1)",
        options=[
            Option(id="A", text="x = 14", is_correct=True),
            Option(id="B", text="x = 10", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Subtracted 2 from 12 instead of adding 2 to 12: 12 - 2 = 10."),
            Option(id="C", text="x = 6", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Did not multiply inner constants: 3x - 4 = 2x + 1."),
            Option(id="D", text="x = -14", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Transposition sign error."),
        ],
        correct_option_id="A",
        hint="First expand both sides with distributive property, then collect terms.",
        explanation="Step 1: Expand: 3x - 12 = 2x + 2.\nStep 2: Subtract 2x: x - 12 = 2.\nStep 3: Add 12: x = 14.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-LIN-003": Question(
        id="Q-LIN-003",
        concept_id="MATH-C05",
        prerequisite_ids=["MATH-C02", "MATH-C03", "MATH-C04"],
        prompt="Solve the linear equation with negative coefficient:",
        equation_display="-4x + 9 = 29",
        options=[
            Option(id="A", text="x = -5", is_correct=True),
            Option(id="B", text="x = 5", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Divided by +4 instead of -4: 20 / 4 = 5."),
            Option(id="C", text="x = -9.5", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Added 9 to 29 instead of subtracting: 38 / (-4)."),
            Option(id="D", text="x = 8", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Sign and arithmetic confusion."),
        ],
        correct_option_id="A",
        hint="Undo the +9 by subtracting 9, then divide both sides by -4.",
        explanation="Step 1: Subtract 9: -4x = 20.\nStep 2: Divide by -4: x = 20 / (-4) = -5.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-LIN-004": Question(
        id="Q-LIN-004",
        concept_id="MATH-C05",
        prerequisite_ids=["MATH-C02", "MATH-C03", "MATH-C04"],
        prompt="Solve for x in the equation below:",
        equation_display="2(2x + 3) = 18",
        options=[
            Option(id="A", text="x = 3", is_correct=True),
            Option(id="B", text="x = 6", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Divided 18 by 2 to get 9, but forgot to subtract 3 and divide by 2."),
            Option(id="C", text="x = 15/4", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Did not distribute 2 to 3, writing 4x + 3 = 18."),
            Option(id="D", text="x = -3", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Sign error during subtraction."),
        ],
        correct_option_id="A",
        hint="Method 1: Distribute 2 into (2x + 3) to get 4x + 6 = 18. Method 2: Divide both sides by 2 first: 2x + 3 = 9.",
        explanation="Step 1: 4x + 6 = 18.\nStep 2: 4x = 18 - 6 = 12.\nStep 3: x = 12 / 4 = 3.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-LIN-005": Question(
        id="Q-LIN-005",
        concept_id="MATH-C05",
        prerequisite_ids=["MATH-C02", "MATH-C03", "MATH-C04"],
        prompt="Solve the linear equation involving a fraction:",
        equation_display="(3x + 1) / 4 = 4",
        options=[
            Option(id="A", text="x = 5", is_correct=True),
            Option(id="B", text="x = 1", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Subtracted 1 from 4 first without multiplying by denominator 4."),
            Option(id="C", text="x = 17/3", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added 1 to 16 instead of subtracting 1: 16 + 1 = 17."),
            Option(id="D", text="x = 4", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation slip."),
        ],
        correct_option_id="A",
        hint="Multiply both sides by 4 to eliminate the fraction: 3x + 1 = 16.",
        explanation="Step 1: Multiply both sides by 4: 3x + 1 = 16.\nStep 2: Subtract 1: 3x = 15.\nStep 3: Divide by 3: x = 5.",
        cognitive_demand=CognitiveDemand.TRANSFER,
        difficulty=3,
        content_version="1.0.0"
    ),

    # =========================================================================
    # CONCEPT 6: MATH-C06 (Verifying Solutions by Substitution)
    # =========================================================================
    "Q-VER-001": Question(
        id="Q-VER-001",
        concept_id="MATH-C06",
        prerequisite_ids=["MATH-C01", "MATH-C02", "MATH-C05"],
        prompt="Verify whether x = 4 is a correct solution to the equation below:",
        equation_display="3x + 5 = 2x + 9",
        options=[
            Option(id="A", text="Yes, because LHS = 17 and RHS = 17, so LHS = RHS", is_correct=True),
            Option(id="B", text="No, because LHS = 17 and RHS = 19", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error in evaluating 2(4) + 9."),
            Option(id="C", text="No, because LHS = 12 and RHS = 8", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Substituted 4 but forgot to add constants +5 and +9."),
            Option(id="D", text="Yes, but only if x is positive", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Misunderstood algebraic equivalence."),
        ],
        correct_option_id="A",
        hint="Compute LHS: 3(4) + 5. Compute RHS: 2(4) + 9. Check if both values are equal.",
        explanation="LHS: 3(4) + 5 = 12 + 5 = 17.\nRHS: 2(4) + 9 = 8 + 9 = 17.\nSince LHS (17) == RHS (17), x = 4 is verified as the correct solution.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-VER-002": Question(
        id="Q-VER-002",
        concept_id="MATH-C06",
        prerequisite_ids=["MATH-C01", "MATH-C02", "MATH-C05"],
        prompt="A student tests x = -2 in 4x - 6 = -14. Which statement correctly evaluates their check?",
        equation_display="4x - 6 = -14   (Test: x = -2)",
        options=[
            Option(id="A", text="LHS = 4(-2) - 6 = -8 - 6 = -14. Since LHS == RHS, x = -2 is correct.", is_correct=True),
            Option(id="B", text="LHS = 4(-2) - 6 = -8 - 6 = -2. Since LHS != RHS, x = -2 is wrong.", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Calculated -8 - 6 as -2 instead of -14."),
            Option(id="C", text="LHS = 4(-2) - 6 = +8 - 6 = 2. Since LHS != RHS, x = -2 is wrong.", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Multiplied 4 * (-2) as +8 instead of -8."),
            Option(id="D", text="Negative numbers cannot be tested by substitution.", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Negative numbers can always be substituted."),
        ],
        correct_option_id="A",
        hint="Compute 4 * (-2) = -8, then -8 - 6 = -14. Compare with RHS -14.",
        explanation="LHS: 4(-2) - 6 = -8 - 6 = -14. RHS is -14. Since -14 == -14, x = -2 is verified.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=3,
        content_version="1.0.0"
    ),

    "Q-VER-003": Question(
        id="Q-VER-003",
        concept_id="MATH-C06",
        prerequisite_ids=["MATH-C01", "MATH-C02", "MATH-C05"],
        prompt="Is x = 5 a valid solution to 2(x - 1) = 8?",
        equation_display="2(x - 1) = 8   (Check x = 5)",
        options=[
            Option(id="A", text="Yes, because LHS = 2(5 - 1) = 2(4) = 8, which equals RHS", is_correct=True),
            Option(id="B", text="No, because LHS = 2(5) - 1 = 9 != 8", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Did not subtract 1 before multiplying by 2."),
            Option(id="C", text="No, because x must be even", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Solutions to equations can be odd or even."),
            Option(id="D", text="Yes, because 5 - 1 = 4", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Incomplete verification: did not multiply by 2 to compare with RHS."),
        ],
        correct_option_id="A",
        hint="Substitute 5 for x inside parentheses: 5 - 1 = 4. Then multiply 2 * 4.",
        explanation="LHS: 2(5 - 1) = 2(4) = 8. RHS: 8. Since LHS == RHS, x = 5 is correct.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-VER-004": Question(
        id="Q-VER-004",
        concept_id="MATH-C06",
        prerequisite_ids=["MATH-C01", "MATH-C02", "MATH-C05"],
        prompt="Which candidate value from {2, 3, 4} satisfies 5x - 7 = 8?",
        equation_display="5x - 7 = 8",
        options=[
            Option(id="A", text="x = 3, because 5(3) - 7 = 15 - 7 = 8", is_correct=True),
            Option(id="B", text="x = 2, because 5(2) - 7 = 3", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="3 does not equal 8, so x = 2 is not a solution."),
            Option(id="C", text="x = 4, because 5(4) - 7 = 13", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="13 does not equal 8, so x = 4 is not a solution."),
            Option(id="D", text="None of these values satisfy the equation", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="x = 3 satisfies the equation exactly."),
        ],
        correct_option_id="A",
        hint="Test each candidate: For x = 3, compute 5(3) - 7.",
        explanation="Testing x = 3: 5(3) - 7 = 15 - 7 = 8. This matches RHS 8. Therefore x = 3 is the solution.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2,
        content_version="1.0.0"
    ),

    "Q-VER-005": Question(
        id="Q-VER-005",
        concept_id="MATH-C06",
        prerequisite_ids=["MATH-C01", "MATH-C02", "MATH-C05"],
        prompt="A student checks x = 6 in 2x + 4 = 16 and writes: '2(6) + 4 = 12 + 4 = 16, but 16 / 2 = 8, so it is incorrect.' What is the logical flaw in their verification?",
        equation_display="2x + 4 = 16   (Tested x = 6)",
        options=[
            Option(id="A", text="Once LHS evaluates to 16, it matches RHS 16; doing extra operations like dividing by 2 is unnecessary and flawed.", is_correct=True),
            Option(id="B", text="Their arithmetic 12 + 4 = 16 was wrong.", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="12 + 4 is indeed 16."),
            Option(id="C", text="They should have subtracted 4 from 16 first.", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Verification evaluates expressions independently without transposing."),
            Option(id="D", text="x = 6 is not a solution.", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="x = 6 is indeed the exact correct solution."),
        ],
        correct_option_id="A",
        hint="Verification means evaluating the LHS value and comparing it directly to the RHS value. If they are equal, the check is complete.",
        explanation="The student proved LHS = 16. Since RHS = 16, LHS == RHS. The additional division by 2 was completely extraneous and misguided.",
        cognitive_demand=CognitiveDemand.TRANSFER,
        difficulty=3,
        content_version="1.0.0"
    ),

    # =========================================================================
    # CONCEPT 7: MATH-C07 (Properties of Rational Numbers)
    # =========================================================================
    "Q-RAT-001": Question(
        id="Q-RAT-001",
        concept_id="MATH-C07",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the multiplicative inverse (reciprocal) of -13/19?",
        equation_display="(-13/19)^(-1)",
        options=[
            Option(id="A", text="-19/13", is_correct=True),
            Option(id="B", text="13/19", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Changed the sign instead of taking reciprocal (this is the additive inverse)."),
            Option(id="C", text="19/13", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Inverted the fraction but dropped the negative sign."),
            Option(id="D", text="-13/19", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="A number is not its own multiplicative inverse unless it is 1 or -1.")
        ],
        correct_option_id="A",
        hint="The multiplicative inverse of a/b is b/a because (a/b) * (b/a) = 1.",
        explanation="For any non-zero rational number a/b, its reciprocal is b/a. Therefore (-13/19)^(-1) = -19/13.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1
    ),
    "Q-RAT-002": Question(
        id="Q-RAT-002",
        concept_id="MATH-C07",
        prerequisite_ids=["MATH-C01"],
        prompt="Which property is illustrated by the statement: (-4/5) * 1 = 1 * (-4/5) = -4/5?",
        options=[
            Option(id="A", text="1 is the multiplicative identity for rational numbers", is_correct=True),
            Option(id="B", text="Closure property under multiplication", is_correct=False, misconception_tag=MisconceptionTag.NONE),
            Option(id="C", text="Additive identity property", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="0 is the additive identity; 1 is the multiplicative identity."),
            Option(id="D", text="Associative property", is_correct=False, misconception_tag=MisconceptionTag.NONE)
        ],
        correct_option_id="A",
        hint="When any number is multiplied by 1, its value does not change.",
        explanation="1 is the multiplicative identity for integers, whole numbers, and rational numbers.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=1
    ),
    "Q-RAT-003": Question(
        id="Q-RAT-003",
        concept_id="MATH-C07",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the additive inverse of 2/(-9)?",
        options=[
            Option(id="A", text="2/9", is_correct=True),
            Option(id="B", text="-9/2", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Took reciprocal instead of changing sign."),
            Option(id="C", text="-2/9", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="2/(-9) is already equal to -2/9."),
            Option(id="D", text="9/2", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Flipped and changed sign.")
        ],
        correct_option_id="A",
        hint="The additive inverse of -x is +x so that -x + x = 0.",
        explanation="2/(-9) = -2/9. Its additive inverse is -(-2/9) = 2/9.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 8: MATH-C08 (Operations on Rational Numbers)
    # =========================================================================
    "Q-RATOPS-001": Question(
        id="Q-RATOPS-001",
        concept_id="MATH-C08",
        prerequisite_ids=["MATH-C07"],
        prompt="Evaluate the difference between the rational numbers:",
        equation_display="7/24 - 17/36",
        options=[
            Option(id="A", text="-13/72", is_correct=True),
            Option(id="B", text="13/72", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Subtracting larger from smaller yields negative result."),
            Option(id="C", text="-10/12", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Subtracted numerators and denominators directly."),
            Option(id="D", text="-5/36", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="LCM calculation error.")
        ],
        correct_option_id="A",
        hint="LCM of 24 and 36 is 72. Convert both fractions to denominator 72.",
        explanation="7/24 = 21/72, 17/36 = 34/72. Then 21/72 - 34/72 = (21 - 34)/72 = -13/72.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),
    "Q-RATOPS-002": Question(
        id="Q-RATOPS-002",
        concept_id="MATH-C08",
        prerequisite_ids=["MATH-C07"],
        prompt="Evaluate the division of rational numbers:",
        equation_display="(-4/5) / (-2/3)",
        options=[
            Option(id="A", text="6/5", is_correct=True),
            Option(id="B", text="-6/5", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Dividing negative by negative yields positive."),
            Option(id="C", text="8/15", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Multiplied straight across without taking reciprocal of divisor."),
            Option(id="D", text="-8/15", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Multiplied without inverting and kept negative.")
        ],
        correct_option_id="A",
        hint="To divide by a fraction, multiply by its reciprocal: (a/b) / (c/d) = (a/b) * (d/c).",
        explanation="(-4/5) / (-2/3) = (-4/5) * (-3/2) = 12/10 = 6/5.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),
    "Q-RATOPS-003": Question(
        id="Q-RATOPS-003",
        concept_id="MATH-C08",
        prerequisite_ids=["MATH-C07"],
        prompt="Which of the following is a rational number lying between 1/4 and 1/2?",
        options=[
            Option(id="A", text="3/8", is_correct=True),
            Option(id="B", text="1/8", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="1/8 is less than 1/4."),
            Option(id="C", text="5/8", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="5/8 is greater than 1/2."),
            Option(id="D", text="7/8", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="7/8 is greater than 1/2.")
        ],
        correct_option_id="A",
        hint="The mean (a + b) / 2 of two rational numbers always lies strictly between them.",
        explanation="Mean = (1/4 + 1/2)/2 = (3/4)/2 = 3/8. 1/4 = 2/8 < 3/8 < 4/8 = 1/2.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 9: MATH-C09 (Polygons and Angle Sum Property)
    # =========================================================================
    "Q-POLY-001": Question(
        id="Q-POLY-001",
        concept_id="MATH-C09",
        prerequisite_ids=["MATH-C01"],
        prompt="Find the sum of measures of all interior angles of a pentagon (5 sides):",
        equation_display="S = (n - 2) * 180 degrees",
        options=[
            Option(id="A", text="540 degrees", is_correct=True),
            Option(id="B", text="900 degrees", is_correct=False, misconception_tag=MisconceptionTag.QUADRILATERAL_ANGLE_SUM_ERROR, misconception_explanation="Multiplied n * 180 instead of (n - 2) * 180."),
            Option(id="C", text="360 degrees", is_correct=False, misconception_tag=MisconceptionTag.QUADRILATERAL_ANGLE_SUM_ERROR, misconception_explanation="360 degrees is the sum of exterior angles, not interior angles."),
            Option(id="D", text="720 degrees", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="720 degrees is the angle sum of a hexagon (6 sides).")
        ],
        correct_option_id="A",
        hint="Use the polygon interior angle sum formula: S = (n - 2) * 180 where n is the number of sides.",
        explanation="For a pentagon, n = 5. S = (5 - 2) * 180 = 3 * 180 = 540 degrees.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),
    "Q-POLY-002": Question(
        id="Q-POLY-002",
        concept_id="MATH-C09",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the measure of each exterior angle of a regular nonagon (9 sides)?",
        equation_display="Exterior Angle = 360 / n",
        options=[
            Option(id="A", text="40 degrees", is_correct=True),
            Option(id="B", text="45 degrees", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="45 degrees is for an octagon (8 sides)."),
            Option(id="C", text="140 degrees", is_correct=False, misconception_tag=MisconceptionTag.QUADRILATERAL_ANGLE_SUM_ERROR, misconception_explanation="140 degrees is the interior angle, not the exterior angle."),
            Option(id="D", text="30 degrees", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="30 degrees is for a dodecagon (12 sides).")
        ],
        correct_option_id="A",
        hint="The sum of all exterior angles is always 360 degrees. For a regular polygon with n sides, each exterior angle is 360 / n.",
        explanation="Exterior angle = 360 / 9 = 40 degrees.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),
    "Q-POLY-003": Question(
        id="Q-POLY-003",
        concept_id="MATH-C09",
        prerequisite_ids=["MATH-C01"],
        prompt="How many sides does a regular polygon have if each of its exterior angles measures 24 degrees?",
        equation_display="n = 360 / Exterior Angle",
        options=[
            Option(id="A", text="15 sides", is_correct=True),
            Option(id="B", text="12 sides", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="360 / 24 is 15, not 12."),
            Option(id="C", text="16 sides", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="10 sides", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error.")
        ],
        correct_option_id="A",
        hint="Number of sides n = 360 / (measure of each exterior angle).",
        explanation="n = 360 / 24 = 15 sides.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 10: MATH-C10 (Special Quadrilaterals)
    # =========================================================================
    "Q-QUAD-001": Question(
        id="Q-QUAD-001",
        concept_id="MATH-C10",
        prerequisite_ids=["MATH-C09"],
        prompt="Two adjacent angles of a parallelogram are in the ratio 3:2. What is the measure of the smaller angle?",
        equation_display="3x + 2x = 180 degrees",
        options=[
            Option(id="A", text="72 degrees", is_correct=True),
            Option(id="B", text="108 degrees", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="108 degrees is the larger angle."),
            Option(id="C", text="36 degrees", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="36 degrees is the value of x, not the angle 2x."),
            Option(id="D", text="90 degrees", is_correct=False, misconception_tag=MisconceptionTag.QUADRILATERAL_ANGLE_SUM_ERROR, misconception_explanation="Adjacent angles are only equal (90 each) in rectangles/squares.")
        ],
        correct_option_id="A",
        hint="Adjacent angles of a parallelogram are supplementary (their sum is 180 degrees).",
        explanation="3x + 2x = 180 => 5x = 180 => x = 36. Smaller angle = 2x = 2 * 36 = 72 degrees.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),
    "Q-QUAD-002": Question(
        id="Q-QUAD-002",
        concept_id="MATH-C10",
        prerequisite_ids=["MATH-C09"],
        prompt="The diagonals of a rhombus are 6 cm and 8 cm. What is the length of each side of the rhombus?",
        equation_display="side^2 = (d1/2)^2 + (d2/2)^2",
        options=[
            Option(id="A", text="5 cm", is_correct=True),
            Option(id="B", text="7 cm", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="Added half diagonals (3 + 4 = 7) instead of applying Pythagoras theorem."),
            Option(id="C", text="10 cm", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Applied full diagonal lengths 6^2 + 8^2 = 100 => 10."),
            Option(id="D", text="14 cm", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="Added full diagonal lengths.")
        ],
        correct_option_id="A",
        hint="Diagonals of a rhombus bisect each other perpendicularly, creating four right-angled triangles with legs d1/2 and d2/2.",
        explanation="Half diagonals are 3 cm and 4 cm. Side = sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5 cm.",
        cognitive_demand=CognitiveDemand.TRANSFER,
        difficulty=3
    ),

    # =========================================================================
    # CONCEPT 11: MATH-C11 (Organizing Data)
    # =========================================================================
    "Q-DATA-001": Question(
        id="Q-DATA-001",
        concept_id="MATH-C11",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the class mark (midpoint) of the class interval 125 - 150?",
        equation_display="Class Mark = (Lower Limit + Upper Limit) / 2",
        options=[
            Option(id="A", text="137.5", is_correct=True),
            Option(id="B", text="25", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="25 is the class size (width), not the class mark."),
            Option(id="C", text="135", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="275", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Forgot to divide the sum by 2.")
        ],
        correct_option_id="A",
        hint="Class mark is the average of the lower and upper class limits.",
        explanation="Class mark = (125 + 150) / 2 = 275 / 2 = 137.5.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 12: MATH-C12 (Pie Charts and Probability)
    # =========================================================================
    "Q-PIE-001": Question(
        id="Q-PIE-001",
        concept_id="MATH-C12",
        prerequisite_ids=["MATH-C11"],
        prompt="In a pie chart, a sector represents 25% of the total expenditure. What is the central angle of this sector?",
        equation_display="Angle = (Percentage / 100) * 360 degrees",
        options=[
            Option(id="A", text="90 degrees", is_correct=True),
            Option(id="B", text="25 degrees", is_correct=False, misconception_tag=MisconceptionTag.PERCENTAGE_BASE_ERROR, misconception_explanation="Treated percentage directly as angle degrees."),
            Option(id="C", text="45 degrees", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="45 degrees represents 12.5% of a circle."),
            Option(id="D", text="180 degrees", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="180 degrees represents 50%.")
        ],
        correct_option_id="A",
        hint="Total central angle of a circle is 360 degrees. Find 25% of 360.",
        explanation="Central angle = (25/100) * 360 = (1/4) * 360 = 90 degrees.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),
    "Q-PIE-002": Question(
        id="Q-PIE-002",
        concept_id="MATH-C12",
        prerequisite_ids=["MATH-C11"],
        prompt="When a standard 6-sided die is rolled, what is the probability of rolling a prime number?",
        options=[
            Option(id="A", text="1/2", is_correct=True),
            Option(id="B", text="2/3", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Treated 1 or 4 as prime."),
            Option(id="C", text="1/3", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Counted only 2 primes."),
            Option(id="D", text="1/6", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="This is the probability of a single number.")
        ],
        correct_option_id="A",
        hint="The possible outcomes on a die are {1, 2, 3, 4, 5, 6}. Identify which numbers are prime (greater than 1 with no other divisors).",
        explanation="Prime numbers on a die are {2, 3, 5} (3 favorable outcomes). Total outcomes = 6. Probability = 3/6 = 1/2.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 13: MATH-C13 (Square Numbers and Pythagorean Triplets)
    # =========================================================================
    "Q-SQNUM-001": Question(
        id="Q-SQNUM-001",
        concept_id="MATH-C13",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the unit digit of the square of 1053?",
        options=[
            Option(id="A", text="9", is_correct=True),
            Option(id="B", text="3", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Square of unit digit 3 is 9, not 3."),
            Option(id="C", text="6", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Multiplied by 2 (3*2=6) instead of squaring (3*3=9)."),
            Option(id="D", text="1", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Squares ending in 1 come from unit digits 1 or 9.")
        ],
        correct_option_id="A",
        hint="The unit digit of a square depends solely on the square of its own unit digit.",
        explanation="Unit digit is 3. 3^2 = 9. Therefore, 1053^2 ends in 9.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1
    ),
    "Q-SQNUM-002": Question(
        id="Q-SQNUM-002",
        concept_id="MATH-C13",
        prerequisite_ids=["MATH-C01"],
        prompt="Find a Pythagorean triplet whose smallest member is 8:",
        equation_display="(2m, m^2 - 1, m^2 + 1)",
        options=[
            Option(id="A", text="(8, 15, 17)", is_correct=True),
            Option(id="B", text="(8, 10, 12)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="8^2 + 10^2 = 64 + 100 = 164 != 144."),
            Option(id="C", text="(8, 12, 16)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Not a Pythagorean triplet."),
            Option(id="D", text="(8, 63, 65)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="This uses m = 8 instead of 2m = 8.")
        ],
        correct_option_id="A",
        hint="Let 2m = 8 => m = 4. Then compute m^2 - 1 and m^2 + 1.",
        explanation="2m = 8 => m = 4. m^2 - 1 = 4^2 - 1 = 15. m^2 + 1 = 4^2 + 1 = 17. Check: 8^2 + 15^2 = 64 + 225 = 289 = 17^2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 14: MATH-C14 (Finding Square Roots)
    # =========================================================================
    "Q-SQRT-001": Question(
        id="Q-SQRT-001",
        concept_id="MATH-C14",
        prerequisite_ids=["MATH-C13"],
        prompt="Find the square root of 1296 using prime factorisation:",
        equation_display="sqrt(1296)",
        options=[
            Option(id="A", text="36", is_correct=True),
            Option(id="B", text="34", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="34^2 = 1156."),
            Option(id="C", text="648", is_correct=False, misconception_tag=MisconceptionTag.SQUARE_ROOT_HALVING, misconception_explanation="Divided by 2 instead of taking square root."),
            Option(id="D", text="38", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="38^2 = 1444.")
        ],
        correct_option_id="A",
        hint="1296 = 2^4 * 3^4 = (2^2 * 3^2)^2.",
        explanation="1296 = (2 * 2 * 2 * 2) * (3 * 3 * 3 * 3). sqrt(1296) = 2 * 2 * 3 * 3 = 36.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 15: MATH-C15 (Cube Numbers and Patterns)
    # =========================================================================
    "Q-CBNUM-001": Question(
        id="Q-CBNUM-001",
        concept_id="MATH-C15",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the unit digit of the cube of 23?",
        options=[
            Option(id="A", text="7", is_correct=True),
            Option(id="B", text="3", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Numbers ending in 3 have cubes ending in 7."),
            Option(id="C", text="9", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="9 is the square of 3, not the cube."),
            Option(id="D", text="1", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Cubes ending in 1 come from numbers ending in 1.")
        ],
        correct_option_id="A",
        hint="3^3 = 3 * 3 * 3 = 27, which ends in 7.",
        explanation="The unit digit of 23^3 is determined by 3^3 = 27 => 7.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 16: MATH-C16 (Finding Cube Roots)
    # =========================================================================
    "Q-CBRT-001": Question(
        id="Q-CBRT-001",
        concept_id="MATH-C16",
        prerequisite_ids=["MATH-C15"],
        prompt="Find the cube root of 512 using prime factorisation:",
        equation_display="cbrt(512)",
        options=[
            Option(id="A", text="8", is_correct=True),
            Option(id="B", text="16", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="16^3 = 4096."),
            Option(id="C", text="4", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="4^3 = 64."),
            Option(id="D", text="64", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="512 / 8 = 64, not the cube root.")
        ],
        correct_option_id="A",
        hint="512 = 2^9. Group into triplets of equal factors.",
        explanation="512 = (2*2*2) * (2*2*2) * (2*2*2). cbrt(512) = 2 * 2 * 2 = 8.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 17: MATH-C17 (Comparing Quantities - Percentages & Commercial)
    # =========================================================================
    "Q-COMP-001": Question(
        id="Q-COMP-001",
        concept_id="MATH-C17",
        prerequisite_ids=["MATH-C08"],
        prompt="An item marked at Rs 840 is sold for Rs 714. What is the discount percentage?",
        equation_display="Discount % = (Discount / Marked Price) * 100",
        options=[
            Option(id="A", text="15%", is_correct=True),
            Option(id="B", text="17.6%", is_correct=False, misconception_tag=MisconceptionTag.PERCENTAGE_BASE_ERROR, misconception_explanation="Calculated discount on selling price (126/714) instead of marked price (126/840)."),
            Option(id="C", text="12.6%", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="20%", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="20% would be Rs 168 discount.")
        ],
        correct_option_id="A",
        hint="Discount = Marked Price - Sale Price. Discount % is always computed on the Marked Price.",
        explanation="Discount = 840 - 714 = Rs 126. Discount % = (126 / 840) * 100 = 15%.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 18: MATH-C18 (Compound Interest)
    # =========================================================================
    "Q-CI-001": Question(
        id="Q-CI-001",
        concept_id="MATH-C18",
        prerequisite_ids=["MATH-C17"],
        prompt="Calculate the compound interest on Rs 10000 for 2 years at 10% per annum compounded annually:",
        equation_display="A = P * (1 + R/100)^n; CI = A - P",
        options=[
            Option(id="A", text="Rs 2100", is_correct=True),
            Option(id="B", text="Rs 2000", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Rs 2000 is the Simple Interest, not Compound Interest."),
            Option(id="C", text="Rs 12100", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Rs 12100 is the total Amount (A), not the Interest (CI = A - P)."),
            Option(id="D", text="Rs 1100", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Computed interest for only 1 year.")
        ],
        correct_option_id="A",
        hint="Amount A = 10000 * (1 + 10/100)^2 = 10000 * (1.1)^2 = 12100. Then CI = A - P.",
        explanation="A = 10000 * (11/10)^2 = 10000 * 121/100 = Rs 12100. CI = 12100 - 10000 = Rs 2100.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 19: MATH-C19 (Multiplication of Algebraic Expressions)
    # =========================================================================
    "Q-MULT-001": Question(
        id="Q-MULT-001",
        concept_id="MATH-C19",
        prerequisite_ids=["MATH-C04"],
        prompt="Multiply the binomials and simplify:",
        equation_display="(2a + 3b) * (3a - 4b)",
        options=[
            Option(id="A", text="6a^2 + ab - 12b^2", is_correct=True),
            Option(id="B", text="6a^2 - ab - 12b^2", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="-8ab + 9ab = +ab, not -ab."),
            Option(id="C", text="6a^2 - 12b^2", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Forgot the middle terms (-8ab + 9ab)."),
            Option(id="D", text="5a^2 - b^2", is_correct=False, misconception_tag=MisconceptionTag.LIKE_TERMS_CONFLATION, misconception_explanation="Added coefficients instead of multiplying.")
        ],
        correct_option_id="A",
        hint="Use FOIL / Distributive property: 2a(3a - 4b) + 3b(3a - 4b).",
        explanation="2a * 3a = 6a^2; 2a * (-4b) = -8ab; 3b * 3a = 9ab; 3b * (-4b) = -12b^2. Combining: 6a^2 + ab - 12b^2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 20: MATH-C20 (Standard Algebraic Identities)
    # =========================================================================
    "Q-IDENT-001": Question(
        id="Q-IDENT-001",
        concept_id="MATH-C20",
        prerequisite_ids=["MATH-C19"],
        prompt="Using a standard algebraic identity, evaluate:",
        equation_display="105 * 95",
        options=[
            Option(id="A", text="9975", is_correct=True),
            Option(id="B", text="9995", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="10000 - 25 = 9975, not 9995."),
            Option(id="C", text="9950", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="10025", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added 25 instead of subtracting: a^2 - b^2.")
        ],
        correct_option_id="A",
        hint="(100 + 5)(100 - 5) matches the identity (a + b)(a - b) = a^2 - b^2.",
        explanation="105 * 95 = (100 + 5)(100 - 5) = 100^2 - 5^2 = 10000 - 25 = 9975.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 21: MATH-C21 (Area of Trapezium and Polygons)
    # =========================================================================
    "Q-MENS-001": Question(
        id="Q-MENS-001",
        concept_id="MATH-C21",
        prerequisite_ids=["MATH-C10"],
        prompt="Find the area of a trapezium with parallel sides of 12 cm and 20 cm, and height 10 cm:",
        equation_display="Area = (1/2) * (a + b) * h",
        options=[
            Option(id="A", text="160 cm^2", is_correct=True),
            Option(id="B", text="320 cm^2", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="Forgot the factor of 1/2."),
            Option(id="C", text="120 cm^2", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Multiplied only one side by height."),
            Option(id="D", text="42 cm", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="Computed perimeter/units instead of area.")
        ],
        correct_option_id="A",
        hint="Area = (1/2) * (sum of parallel sides) * height.",
        explanation="Area = (1/2) * (12 + 20) * 10 = (1/2) * 32 * 10 = 16 * 10 = 160 cm^2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 22: MATH-C22 (Surface Area and Volume of 3D Solids)
    # =========================================================================
    "Q-VOL-001": Question(
        id="Q-VOL-001",
        concept_id="MATH-C22",
        prerequisite_ids=["MATH-C21"],
        prompt="Find the volume of a right circular cylinder with radius 7 cm and height 10 cm (take pi = 22/7):",
        equation_display="V = pi * r^2 * h",
        options=[
            Option(id="A", text="1540 cm^3", is_correct=True),
            Option(id="B", text="440 cm^2", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="440 is the Curved Surface Area 2*pi*r*h, not the Volume."),
            Option(id="C", text="220 cm^3", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Used r instead of r^2."),
            Option(id="D", text="3080 cm^3", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Multiplied by diameter instead of radius.")
        ],
        correct_option_id="A",
        hint="Volume of a cylinder is Area of base * height = pi * r^2 * h.",
        explanation="V = (22/7) * 7 * 7 * 10 = 22 * 7 * 10 = 1540 cm^3.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 23: MATH-C23 (Powers with Negative Exponents)
    # =========================================================================
    "Q-EXP-001": Question(
        id="Q-EXP-001",
        concept_id="MATH-C23",
        prerequisite_ids=["MATH-C08"],
        prompt="Evaluate the value of the exponential expression:",
        equation_display="(1/2)^(-5)",
        options=[
            Option(id="A", text="32", is_correct=True),
            Option(id="B", text="-32", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Negative exponent indicates reciprocal, not a negative result."),
            Option(id="C", text="1/32", is_correct=False, misconception_tag=MisconceptionTag.EXPONENT_BASE_CONFLATION, misconception_explanation="Evaluated (1/2)^5 instead of (1/2)^(-5)."),
            Option(id="D", text="-10", is_correct=False, misconception_tag=MisconceptionTag.EXPONENT_BASE_CONFLATION, misconception_explanation="Multiplied base by exponent.")
        ],
        correct_option_id="A",
        hint="(a/b)^(-m) = (b/a)^m. Inverting 1/2 gives 2.",
        explanation="(1/2)^(-5) = (2/1)^5 = 2^5 = 32.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 24: MATH-C24 (Laws of Exponents and Scientific Form)
    # =========================================================================
    "Q-EXPLAW-001": Question(
        id="Q-EXPLAW-001",
        concept_id="MATH-C24",
        prerequisite_ids=["MATH-C23"],
        prompt="Express 0.000000000085 in standard scientific form:",
        options=[
            Option(id="A", text="8.5 * 10^(-11)", is_correct=True),
            Option(id="B", text="8.5 * 10^11", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Very small numbers require negative powers of 10."),
            Option(id="C", text="85 * 10^(-12)", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="In standard form, mantissa must be between 1.0 and 10.0 (8.5, not 85)."),
            Option(id="D", text="0.85 * 10^(-10)", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Mantissa must be >= 1.0.")
        ],
        correct_option_id="A",
        hint="Standard scientific form is k * 10^n where 1.0 <= k < 10. Move decimal 11 places to the right.",
        explanation="Moving decimal point 11 places to the right gives 8.5. Therefore, standard form is 8.5 * 10^(-11).",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 25: MATH-C25 (Direct Proportion)
    # =========================================================================
    "Q-DIR-001": Question(
        id="Q-DIR-001",
        concept_id="MATH-C25",
        prerequisite_ids=["MATH-C08"],
        prompt="If 14 metres of cloth costs Rs 1890, what is the cost of 6 metres of the same cloth?",
        equation_display="14 / 1890 = 6 / y",
        options=[
            Option(id="A", text="Rs 810", is_correct=True),
            Option(id="B", text="Rs 750", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="C", text="Rs 900", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="Rs 4410", is_correct=False, misconception_tag=MisconceptionTag.PROPORTION_INVERSION, misconception_explanation="Treated direct proportion as inverse proportion.")
        ],
        correct_option_id="A",
        hint="Cloth length and cost are in direct proportion: x1 / y1 = x2 / y2.",
        explanation="y = (6 * 1890) / 14 = 6 * 135 = Rs 810.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 26: MATH-C26 (Inverse Proportion)
    # =========================================================================
    "Q-INVPROP-001": Question(
        id="Q-INVPROP-001",
        concept_id="MATH-C26",
        prerequisite_ids=["MATH-C25"],
        prompt="A car travelling at 60 km/h takes 2 hours to cover a distance. How long will it take travelling at 80 km/h?",
        equation_display="60 * 2 = 80 * t",
        options=[
            Option(id="A", text="1.5 hours (1 hr 30 mins)", is_correct=True),
            Option(id="B", text="2.67 hours", is_correct=False, misconception_tag=MisconceptionTag.PROPORTION_INVERSION, misconception_explanation="Treated as direct proportion (higher speed takes more time!)."),
            Option(id="C", text="1.2 hours", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="1 hour", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="At 120 km/h it would take 1 hour.")
        ],
        correct_option_id="A",
        hint="Speed and time for a fixed distance are inversely proportional: Speed1 * Time1 = Speed2 * Time2.",
        explanation="60 * 2 = 80 * t => 120 = 80t => t = 120 / 80 = 1.5 hours.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 27: MATH-C27 (Factorisation)
    # =========================================================================
    "Q-FACT-001": Question(
        id="Q-FACT-001",
        concept_id="MATH-C27",
        prerequisite_ids=["MATH-C20"],
        prompt="Factorise the algebraic expression completely:",
        equation_display="49x^2 - 36",
        options=[
            Option(id="A", text="(7x + 6)(7x - 6)", is_correct=True),
            Option(id="B", text="(7x - 6)^2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="(7x - 6)^2 = 49x^2 - 84x + 36, not a difference of squares."),
            Option(id="C", text="(49x + 6)(x - 6)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="49 is 7^2, not 49*1."),
            Option(id="D", text="(7x + 6)^2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="(7x + 6)^2 = 49x^2 + 84x + 36.")
        ],
        correct_option_id="A",
        hint="Apply identity a^2 - b^2 = (a + b)(a - b) with a = 7x and b = 6.",
        explanation="49x^2 - 36 = (7x)^2 - (6)^2 = (7x + 6)(7x - 6).",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 28: MATH-C28 (Division of Algebraic Expressions)
    # =========================================================================
    "Q-DIV-001": Question(
        id="Q-DIV-001",
        concept_id="MATH-C28",
        prerequisite_ids=["MATH-C27"],
        prompt="Divide the polynomial by the binomial:",
        equation_display="(y^2 + 7y + 10) / (y + 5)",
        options=[
            Option(id="A", text="y + 2", is_correct=True),
            Option(id="B", text="y + 5", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="y + 5 was the divisor."),
            Option(id="C", text="y + 7", is_correct=False, misconception_tag=MisconceptionTag.LIKE_TERMS_CONFLATION, misconception_explanation="Subtracted incorrectly."),
            Option(id="D", text="y^2 + 2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Canceled terms across addition illegally.")
        ],
        correct_option_id="A",
        hint="Factorise the numerator y^2 + 7y + 10 into (y + 5)(y + 2).",
        explanation="(y^2 + 7y + 10) / (y + 5) = [(y + 5)(y + 2)] / (y + 5) = y + 2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    # =========================================================================
    # CONCEPT 29: MATH-C29 (Cartesian Plane and Coordinates)
    # =========================================================================
    "Q-GRAPH-001": Question(
        id="Q-GRAPH-001",
        concept_id="MATH-C29",
        prerequisite_ids=["MATH-C01"],
        prompt="In which quadrant of the coordinate plane does the point (-4, 3) lie?",
        options=[
            Option(id="A", text="Quadrant II", is_correct=True),
            Option(id="B", text="Quadrant I", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Quadrant I has (+, +) signs."),
            Option(id="C", text="Quadrant III", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Quadrant III has (-, -) signs."),
            Option(id="D", text="Quadrant IV", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Quadrant IV has (+, -) signs.")
        ],
        correct_option_id="A",
        hint="In (-4, 3), x is negative (left) and y is positive (up).",
        explanation="Negative x and positive y corresponds to Quadrant II.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1
    ),

    # =========================================================================
    # CONCEPT 30: MATH-C30 (Reading and Interpreting Linear Graphs)
    # =========================================================================
    "Q-LINGRAPH-001": Question(
        id="Q-LINGRAPH-001",
        concept_id="MATH-C30",
        prerequisite_ids=["MATH-C29", "MATH-C05"],
        prompt="A car travels at a uniform speed. Its distance-time linear graph passes through (0, 0) and (2, 100). What is its speed?",
        equation_display="Speed = Distance / Time",
        options=[
            Option(id="A", text="50 km/h", is_correct=True),
            Option(id="B", text="100 km/h", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="100 km is total distance in 2 hours, not speed per hour."),
            Option(id="C", text="200 km/h", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Multiplied distance by time instead of dividing."),
            Option(id="D", text="25 km/h", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Divided by 4 instead of 2.")
        ],
        correct_option_id="A",
        hint="Speed is the slope of the distance-time graph: (y2 - y1) / (x2 - x1).",
        explanation="Speed = (100 - 0) / (2 - 0) = 100 / 2 = 50 km/h.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    # =========================================================================
    # SUPPLEMENTAL QUESTIONS FOR 100% ADAPTIVE PATHWAY COVERAGE
    # =========================================================================
    "Q-DATA-002": Question(
        id="Q-DATA-002",
        concept_id="MATH-C11",
        prerequisite_ids=["MATH-C01"],
        prompt="A frequency distribution table groups data into class intervals 20-30, 30-40, 40-50. What is the lower limit of the class interval 30-40?",
        options=[
            Option(id="A", text="30", is_correct=True),
            Option(id="B", text="40", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="40 is the upper class limit, not the lower limit."),
            Option(id="C", text="35", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="35 is the class mark (midpoint), not lower limit."),
            Option(id="D", text="10", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="10 is the class width (40 - 30).")
        ],
        correct_option_id="A",
        hint="In the class interval a-b, 'a' represents the lower limit and 'b' represents the upper limit.",
        explanation="For interval 30-40, the lower limit is 30.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1
    ),

    "Q-SQRT-002": Question(
        id="Q-SQRT-002",
        concept_id="MATH-C14",
        prerequisite_ids=["MATH-C13"],
        prompt="Estimate the square root of 80 to the nearest whole integer:",
        options=[
            Option(id="A", text="9", is_correct=True),
            Option(id="B", text="8", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="8^2 = 64, difference is 16. 9^2 = 81, difference is only 1."),
            Option(id="C", text="40", is_correct=False, misconception_tag=MisconceptionTag.SQUARE_ROOT_HALVING, misconception_explanation="Divided 80 by 2 instead of finding square root!"),
            Option(id="D", text="10", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="10^2 = 100, which is much larger than 80.")
        ],
        correct_option_id="A",
        hint="Compare 80 with consecutive perfect squares: 8^2 = 64 and 9^2 = 81. Which is closer?",
        explanation="Since 80 is very close to 81 (9^2), sqrt(80) is approximately 9.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    "Q-CBNUM-002": Question(
        id="Q-CBNUM-002",
        concept_id="MATH-C15",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the smallest natural number by which 392 must be multiplied so that the product is a perfect cube? (Prime factors: 392 = 2 * 2 * 2 * 7 * 7)",
        options=[
            Option(id="A", text="7", is_correct=True),
            Option(id="B", text="2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="The factor 2 already appears in a triplet of 3."),
            Option(id="C", text="14", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Multiplying by 14 is not the smallest natural number required."),
            Option(id="D", text="49", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Multiplying by 49 would give 7^4, which is not a multiple of 3.")
        ],
        correct_option_id="A",
        hint="In a perfect cube, every prime factor appears in triplets (groups of 3). How many more 7s are needed?",
        explanation="392 = (2 * 2 * 2) * (7 * 7). The factor 7 appears only twice. Multiplying by 7 completes the triplet.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),

    "Q-CBRT-002": Question(
        id="Q-CBRT-002",
        concept_id="MATH-C16",
        prerequisite_ids=["MATH-C15"],
        prompt="Find the cube root of -216:",
        equation_display="cbrt(-216)",
        options=[
            Option(id="A", text="-6", is_correct=True),
            Option(id="B", text="6", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Cube of positive 6 is +216, not -216."),
            Option(id="C", text="-72", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Divided by 3 instead of taking cube root."),
            Option(id="D", text="36", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Squared 6.")
        ],
        correct_option_id="A",
        hint="The cube of a negative number is always negative: (-6) * (-6) * (-6) = -216.",
        explanation="Since (-6)^3 = -216, cbrt(-216) = -6.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=1
    ),

    "Q-COMP-002": Question(
        id="Q-COMP-002",
        concept_id="MATH-C17",
        prerequisite_ids=["MATH-C07"],
        prompt="An item with marked price Rs 800 is sold for Rs 680 after discount. What is the discount percentage?",
        options=[
            Option(id="A", text="15%", is_correct=True),
            Option(id="B", text="12%", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="C", text="17.6%", is_correct=False, misconception_tag=MisconceptionTag.PERCENTAGE_BASE_ERROR, misconception_explanation="Calculated discount on sale price (120/680) instead of Marked Price (120/800)."),
            Option(id="D", text="20%", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Overestimated discount.")
        ],
        correct_option_id="A",
        hint="Discount Amount = MP - SP = 800 - 680 = 120. Discount % = (Discount / MP) * 100.",
        explanation="Discount = 800 - 680 = 120. Discount % = (120 / 800) * 100 = 15%.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-CI-002": Question(
        id="Q-CI-002",
        concept_id="MATH-C18",
        prerequisite_ids=["MATH-C17"],
        prompt="Calculate the compound interest on Rs 5,000 for 1 year at 10% per annum compounded half-yearly:",
        options=[
            Option(id="A", text="Rs 512.50", is_correct=True),
            Option(id="B", text="Rs 500", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="This is simple interest, missing the compounding effect."),
            Option(id="C", text="Rs 1,025", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Used full 10% rate for both half-years instead of 5%."),
            Option(id="D", text="Rs 5,512.50", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="This is the total Amount, not the Interest earned.")
        ],
        correct_option_id="A",
        hint="Compounded half-yearly: Rate = 10/2 = 5% per half year, n = 2 periods. A = P(1 + r/100)^n.",
        explanation="A = 5000 * (1 + 0.05)^2 = 5000 * 1.1025 = Rs 5,512.50. CI = A - P = 512.50.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=3
    ),

    "Q-MULT-002": Question(
        id="Q-MULT-002",
        concept_id="MATH-C19",
        prerequisite_ids=["MATH-C04"],
        prompt="Subtract (2x - 3y) from (5x + 4y):",
        options=[
            Option(id="A", text="3x + 7y", is_correct=True),
            Option(id="B", text="3x + y", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Failed to invert the sign of -3y: 4y - (-3y) = 4y + 3y = 7y, not y."),
            Option(id="C", text="7x + y", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Added expressions instead of subtracting."),
            Option(id="D", text="3x - 7y", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Sign error on y term.")
        ],
        correct_option_id="A",
        hint="Subtracting (2x - 3y) means adding its opposite: (5x + 4y) - (2x - 3y) = 5x + 4y - 2x + 3y.",
        explanation="(5x - 2x) + (4y - (-3y)) = 3x + (4y + 3y) = 3x + 7y.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-IDENT-002": Question(
        id="Q-IDENT-002",
        concept_id="MATH-C20",
        prerequisite_ids=["MATH-C19"],
        prompt="Evaluate 103 * 97 using the algebraic identity (x + a)(x - a) = x^2 - a^2:",
        options=[
            Option(id="A", text="9,991", is_correct=True),
            Option(id="B", text="9,997", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Subtracted 3 instead of 3^2 = 9 from 10,000."),
            Option(id="C", text="10,009", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Added 9 instead of subtracting 9."),
            Option(id="D", text="9,981", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Subtracted 19.")
        ],
        correct_option_id="A",
        hint="Express as (100 + 3)(100 - 3) = 100^2 - 3^2.",
        explanation="100^2 - 3^2 = 10,000 - 9 = 9,991.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-MENS-002": Question(
        id="Q-MENS-002",
        concept_id="MATH-C21",
        prerequisite_ids=["MATH-C01"],
        prompt="The diagonals of a rhombus are 8 cm and 12 cm. Find its area:",
        options=[
            Option(id="A", text="48 cm^2", is_correct=True),
            Option(id="B", text="96 cm^2", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="Forgot the factor of 1/2 for rhombus area: Area = 1/2 * d1 * d2."),
            Option(id="C", text="20 cm^2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Added the diagonals instead of finding area."),
            Option(id="D", text="40 cm^2", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error.")
        ],
        correct_option_id="A",
        hint="Area of a rhombus = 1/2 * d1 * d2.",
        explanation="Area = (1/2) * 8 * 12 = 4 * 12 = 48 cm^2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-VOL-002": Question(
        id="Q-VOL-002",
        concept_id="MATH-C22",
        prerequisite_ids=["MATH-C21"],
        prompt="A cuboidal box has length 10 cm, breadth 6 cm, and height 4 cm. What is its total surface area?",
        options=[
            Option(id="A", text="248 cm^2", is_correct=True),
            Option(id="B", text="240 cm^3", is_correct=False, misconception_tag=MisconceptionTag.AREA_PERIMETER_CONFUSION, misconception_explanation="Calculated Volume (l*b*h = 240) instead of Surface Area!"),
            Option(id="C", text="124 cm^2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Forgot to multiply by 2 (calculated lb + bh + hl)."),
            Option(id="D", text="400 cm^2", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Arbitrary calculation.")
        ],
        correct_option_id="A",
        hint="Total Surface Area = 2 * (lb + bh + hl).",
        explanation="TSA = 2 * (10*6 + 6*4 + 4*10) = 2 * (60 + 24 + 40) = 2 * 124 = 248 cm^2.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-EXP-002": Question(
        id="Q-EXP-002",
        concept_id="MATH-C23",
        prerequisite_ids=["MATH-C01"],
        prompt="Express 3^4 * 3^2 in exponential form using the product law of exponents:",
        options=[
            Option(id="A", text="3^6", is_correct=True),
            Option(id="B", text="3^8", is_correct=False, misconception_tag=MisconceptionTag.EXPONENT_BASE_CONFLATION, misconception_explanation="Multiplied exponents (4 * 2 = 8) instead of adding them!"),
            Option(id="C", text="9^6", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Multiplied bases 3 * 3 = 9; in exponent laws, the base remains unchanged."),
            Option(id="D", text="9^8", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Multiplied both bases and exponents.")
        ],
        correct_option_id="A",
        hint="When bases are equal, add powers: a^m * a^n = a^(m+n).",
        explanation="3^4 * 3^2 = 3^(4 + 2) = 3^6.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=1
    ),

    "Q-EXPLAW-002": Question(
        id="Q-EXPLAW-002",
        concept_id="MATH-C24",
        prerequisite_ids=["MATH-C23"],
        prompt="Simplify and write in positive exponential form: 5^(-3) * 5^7",
        options=[
            Option(id="A", text="5^4", is_correct=True),
            Option(id="B", text="5^(-21)", is_correct=False, misconception_tag=MisconceptionTag.EXPONENT_BASE_CONFLATION, misconception_explanation="Multiplied exponents (-3 * 7 = -21) instead of adding them."),
            Option(id="C", text="1 / 5^4", is_correct=False, misconception_tag=MisconceptionTag.RECIPROCAL_CONFUSION, misconception_explanation="Inverted positive power 5^4 unnecessarily."),
            Option(id="D", text="5^(-10)", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="Subtracted -3 - 7 = -10.")
        ],
        correct_option_id="A",
        hint="Apply law: a^m * a^n = a^(m+n). Here -3 + 7 = 4.",
        explanation="5^(-3) * 5^7 = 5^(-3 + 7) = 5^4.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-DIR-002": Question(
        id="Q-DIR-002",
        concept_id="MATH-C25",
        prerequisite_ids=["MATH-C07"],
        prompt="If the cost of 12 pens is Rs 180, what is the cost of 8 pens of the same type?",
        options=[
            Option(id="A", text="Rs 120", is_correct=True),
            Option(id="B", text="Rs 150", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="C", text="Rs 96", is_correct=False, misconception_tag=MisconceptionTag.PROPORTION_INVERSION, misconception_explanation="Inverted proportion ratio."),
            Option(id="D", text="Rs 100", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Estimate without ratio.")
        ],
        correct_option_id="A",
        hint="In direct proportion, x/y = constant: 180 / 12 = Cost / 8.",
        explanation="Unit cost = 180 / 12 = Rs 15 per pen. Cost of 8 pens = 15 * 8 = Rs 120.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-INVPROP-002": Question(
        id="Q-INVPROP-002",
        concept_id="MATH-C26",
        prerequisite_ids=["MATH-C25"],
        prompt="6 pipes can fill a tank in 80 minutes. How long will 5 pipes of the same type take?",
        options=[
            Option(id="A", text="96 minutes", is_correct=True),
            Option(id="B", text="66.7 minutes", is_correct=False, misconception_tag=MisconceptionTag.PROPORTION_INVERSION, misconception_explanation="Treated as direct proportion (fewer pipes take less time!)."),
            Option(id="C", text="75 minutes", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="D", text="100 minutes", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Rough guess.")
        ],
        correct_option_id="A",
        hint="Inverse proportion: Pipes1 * Time1 = Pipes2 * Time2: 6 * 80 = 5 * t.",
        explanation="480 = 5 * t => t = 480 / 5 = 96 minutes.",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-FACT-002": Question(
        id="Q-FACT-002",
        concept_id="MATH-C27",
        prerequisite_ids=["MATH-C20"],
        prompt="Factorise the quadratic expression: x^2 + 7x + 12",
        options=[
            Option(id="A", text="(x + 3)(x + 4)", is_correct=True),
            Option(id="B", text="(x + 2)(x + 6)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="2 * 6 = 12, but 2 + 6 = 8, not 7."),
            Option(id="C", text="(x + 1)(x + 12)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="1 + 12 = 13, not 7."),
            Option(id="D", text="(x - 3)(x - 4)", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="(-3) + (-4) = -7, not +7.")
        ],
        correct_option_id="A",
        hint="Find two numbers whose product is 12 and sum is 7: 3 and 4.",
        explanation="x^2 + 3x + 4x + 12 = x(x + 3) + 4(x + 3) = (x + 3)(x + 4).",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-DIV-002": Question(
        id="Q-DIV-002",
        concept_id="MATH-C28",
        prerequisite_ids=["MATH-C27"],
        prompt="Divide 12(x^2 - 16) by 4(x + 4):",
        options=[
            Option(id="A", text="3(x - 4)", is_correct=True),
            Option(id="B", text="3(x + 4)", is_correct=False, misconception_tag=MisconceptionTag.SIGN_ERROR, misconception_explanation="(x^2 - 16) = (x + 4)(x - 4). The factor (x + 4) cancels, leaving 3(x - 4)."),
            Option(id="C", text="12(x - 4)", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Forgot to divide 12 by 4."),
            Option(id="D", text="3x - 16", is_correct=False, misconception_tag=MisconceptionTag.DISTRIBUTION_INCOMPLETE, misconception_explanation="Cancelled terms incorrectly.")
        ],
        correct_option_id="A",
        hint="Factorise x^2 - 16 into (x + 4)(x - 4) and simplify constants: 12 / 4 = 3.",
        explanation="[12(x + 4)(x - 4)] / [4(x + 4)] = 3(x - 4).",
        cognitive_demand=CognitiveDemand.PROCEDURAL,
        difficulty=2
    ),

    "Q-GRAPH-002": Question(
        id="Q-GRAPH-002",
        concept_id="MATH-C29",
        prerequisite_ids=["MATH-C01"],
        prompt="What is the y-coordinate (ordinate) of any point lying on the x-axis?",
        options=[
            Option(id="A", text="0", is_correct=True),
            Option(id="B", text="1", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Points with y=1 lie on the line parallel to x-axis, not on it."),
            Option(id="C", text="Undefined", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="The coordinates are well-defined: (x, 0)."),
            Option(id="D", text="-1", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="Points with y=-1 lie 1 unit below the x-axis.")
        ],
        correct_option_id="A",
        hint="On the horizontal x-axis, there is zero vertical displacement from the origin.",
        explanation="Every point on the x-axis has coordinates of the form (x, 0). Thus y = 0.",
        cognitive_demand=CognitiveDemand.RECALL,
        difficulty=1
    ),

    "Q-LINGRAPH-002": Question(
        id="Q-LINGRAPH-002",
        concept_id="MATH-C30",
        prerequisite_ids=["MATH-C29", "MATH-C05"],
        prompt="A temperature graph shows: 6 AM = 15°C and 12 PM = 27°C. What is the average rate of increase per hour?",
        options=[
            Option(id="A", text="2°C per hour", is_correct=True),
            Option(id="B", text="3°C per hour", is_correct=False, misconception_tag=MisconceptionTag.SUBSTITUTION_CALC_ERROR, misconception_explanation="Calculation error."),
            Option(id="C", text="12°C per hour", is_correct=False, misconception_tag=MisconceptionTag.NONE, misconception_explanation="12°C is total temperature change, not the hourly rate."),
            Option(id="D", text="0.5°C per hour", is_correct=False, misconception_tag=MisconceptionTag.INVERSE_OPERATION_CONFUSION, misconception_explanation="Divided time by change instead of change by time.")
        ],
        correct_option_id="A",
        hint="Rate of change = (Change in temperature) / (Time elapsed). Time = 12 - 6 = 6 hours.",
        explanation="Rate = (27 - 15) / (12 - 6) = 12 / 6 = 2°C per hour.",
        cognitive_demand=CognitiveDemand.CONCEPTUAL,
        difficulty=2
    ),
}


def get_question(question_id: str) -> Question:
    if question_id not in QUESTIONS_REGISTRY:
        raise KeyError(f"Question '{question_id}' not found in registry.")
    return QUESTIONS_REGISTRY[question_id]


def get_all_questions() -> List[Question]:
    return list(QUESTIONS_REGISTRY.values())


def get_questions_by_concept(concept_id: str) -> List[Question]:
    return [q for q in QUESTIONS_REGISTRY.values() if q.concept_id == concept_id]
