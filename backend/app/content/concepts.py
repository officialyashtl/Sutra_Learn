"""
SUTRA LEARN - Concept Definitions and Prerequisite Graph
Domain: Class 8 Mathematics - Linear Equations in One Variable and Foundational Prerequisites.
"""

from typing import Dict, List
from .models import Concept, Lesson, WorkedStep

CONCEPTS_REGISTRY: Dict[str, Concept] = {
    "MATH-C01": Concept(
        id="MATH-C01",
        code="INT_ARITH",
        title="Integer Arithmetic",
        grade=8,
        subject="Mathematics",
        description="Mastery of addition, subtraction, multiplication, and division with positive and negative integers.",
        prerequisites=[],
        order_index=1,
        lesson=Lesson(
            concept_id="MATH-C01",
            title="Mastering Signed Numbers & Integer Operations",
            objective="Perform arithmetic operations with positive and negative integers confidently and without sign confusion.",
            key_principles=[
                "Subtracting a number is identical to adding its opposite: a - b = a + (-b).",
                "Two negatives make an addition when subtracting: a - (-b) = a + b.",
                "Multiplication/division with same signs yields positive; opposite signs yield negative.",
                "Always track sign separate from absolute value before combining."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Identify operation and signs",
                    expression="Compute: -12 - (-7)",
                    reasoning="We are subtracting negative 7 from negative 12."
                ),
                WorkedStep(
                    step_number=2,
                    action="Transform subtraction of negative into addition",
                    expression="-12 + 7",
                    reasoning="Subtracting a negative is the same as adding the positive counterpart."
                ),
                WorkedStep(
                    step_number=3,
                    action="Combine numbers with opposite signs",
                    expression="-5",
                    reasoning="Since |-12| > |7|, the result takes the negative sign: -(12 - 7) = -5."
                )
            ],
            common_pitfalls=[
                "Confusing -4 - 3 as +7 because 'two minuses make a plus' (that rule only applies to multiplication/division or double negatives!).",
                "Losing the negative sign when multiplying a bracket by a negative factor."
            ],
            interactive_prompt="What is -15 + (-8) - (-10)?"
        )
    ),
    "MATH-C02": Concept(
        id="MATH-C02",
        code="EQ_BALANCE",
        title="Equality and The Balance Principle",
        grade=8,
        subject="Mathematics",
        description="Understanding an equation as a balanced scale where equal operations must be applied to both sides to maintain truth.",
        prerequisites=["MATH-C01"],
        order_index=2,
        lesson=Lesson(
            concept_id="MATH-C02",
            title="The Golden Rule of Equations: Balance",
            objective="Conceptualize an equation as a level balance beam where identical operations preserve equality.",
            key_principles=[
                "An equation states that the Left Hand Side (LHS) and Right Hand Side (RHS) have identical numerical value.",
                "Addition/Subtraction Property: Adding or subtracting the same quantity to both sides keeps the scale balanced.",
                "Multiplication/Division Property: Multiplying or dividing both sides by the same non-zero quantity maintains equality.",
                "Any operation performed on one side must be performed on the entirety of the other side."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Observe the balanced relation",
                    expression="x + 9 = 24",
                    reasoning="The quantity (x + 9) balances with 24."
                ),
                WorkedStep(
                    step_number=2,
                    action="Apply identical balance operation to both sides",
                    expression="(x + 9) - 9 = 24 - 9",
                    reasoning="Subtracting 9 from both sides preserves the balance and removes 9 from LHS."
                ),
                WorkedStep(
                    step_number=3,
                    action="Simplify both sides",
                    expression="x = 15",
                    reasoning="Both sides are simplified; variable x is isolated while balance is maintained."
                )
            ],
            common_pitfalls=[
                "Performing an operation on the LHS but forgetting to do it to the RHS.",
                "Treating '=' as just a button to get an answer rather than a relational statement of equivalence."
            ],
            interactive_prompt="If 3p = 21, what operation must be applied to both sides to preserve balance?"
        )
    ),
    "MATH-C03": Concept(
        id="MATH-C03",
        code="INV_OPS",
        title="Inverse Operations",
        grade=8,
        subject="Mathematics",
        description="Identifying and applying inverse mathematical operations to isolate unknown variables systematically.",
        prerequisites=["MATH-C01"],
        order_index=3,
        lesson=Lesson(
            concept_id="MATH-C03",
            title="Undoing Operations: The Power of Inverses",
            objective="Use inverse operations in reverse order of operations (SADMEP) to cleanly isolate variables.",
            key_principles=[
                "Addition and Subtraction are inverse operations: (x + k) - k = x.",
                "Multiplication and Division are inverse operations: (k * x) / k = x (for k != 0).",
                "When solving equations, undo operations in reverse order: undo addition/subtraction before multiplication/division."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Identify operations acting on variable x",
                    expression="4x - 7 = 13",
                    reasoning="x is multiplied by 4, then 7 is subtracted."
                ),
                WorkedStep(
                    step_number=2,
                    action="Undo subtraction first using addition",
                    expression="4x - 7 + 7 = 13 + 7  ==>  4x = 20",
                    reasoning="The inverse of -7 is +7 applied to both sides."
                ),
                WorkedStep(
                    step_number=3,
                    action="Undo multiplication using division",
                    expression="(4x) / 4 = 20 / 4  ==>  x = 5",
                    reasoning="The inverse of multiplying by 4 is dividing by 4."
                )
            ],
            common_pitfalls=[
                "Trying to divide before undoing addition/subtraction, leading to messy fractions.",
                "Dividing only one term when dividing an entire side."
            ],
            interactive_prompt="In 2y + 5 = 17, which operation should you undo first?"
        )
    ),
    "MATH-C04": Concept(
        id="MATH-C04",
        code="SIMP_EXPR",
        title="Simplifying Algebraic Expressions",
        grade=8,
        subject="Mathematics",
        description="Combining like terms and applying the distributive property to simplify expressions before solving.",
        prerequisites=["MATH-C01"],
        order_index=4,
        lesson=Lesson(
            concept_id="MATH-C04",
            title="Simplifying Algebraic Expressions & Distributive Law",
            objective="Combine like terms and expand brackets correctly to prepare equations for solving.",
            key_principles=[
                "Like terms have the exact same variable and exponent: 3x and 5x can combine, but 3x and 5 cannot.",
                "Distributive Property: a(b + c) = ab + ac.",
                "Watch out for negative signs outside brackets: -(x - 4) = -x + 4.",
                "Simplify each side independently before moving terms across the equals sign."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Expand bracket using distributive property",
                    expression="3(2x - 5) + 4x",
                    reasoning="Multiply 3 by 2x and 3 by -5."
                ),
                WorkedStep(
                    step_number=2,
                    action="Write expanded form",
                    expression="6x - 15 + 4x",
                    reasoning="3 * 2x = 6x and 3 * (-5) = -15."
                ),
                WorkedStep(
                    step_number=3,
                    action="Group and combine like terms",
                    expression="(6x + 4x) - 15 = 10x - 15",
                    reasoning="Add coefficients of x: 6 + 4 = 10."
                )
            ],
            common_pitfalls=[
                "Adding variable terms and constants together, e.g., claiming 4x + 3 = 7x.",
                "Multiplying only the first term inside brackets: 2(x + 3) becoming 2x + 3 instead of 2x + 6."
            ],
            interactive_prompt="Simplify: 5(x - 2) - 2x + 7"
        )
    ),
    "MATH-C05": Concept(
        id="MATH-C05",
        code="SOLV_LIN_EQ",
        title="Solving Simple Linear Equations",
        grade=8,
        subject="Mathematics",
        description="Synthesizing balance, inverse operations, and simplification to isolate unknowns in linear equations.",
        prerequisites=["MATH-C02", "MATH-C03", "MATH-C04"],
        order_index=5,
        lesson=Lesson(
            concept_id="MATH-C05",
            title="Solving Linear Equations in One Variable",
            objective="Solve linear equations with variables on one or both sides systematically.",
            key_principles=[
                "Step 1: Simplify both sides (distribute and combine like terms).",
                "Step 2: Collect variable terms on one side by adding or subtracting terms.",
                "Step 3: Collect constant terms on the opposite side.",
                "Step 4: Isolate the variable by dividing by its coefficient."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Expand brackets on LHS",
                    expression="2(3x - 1) = 4x + 10  ==>  6x - 2 = 4x + 10",
                    reasoning="Distribute 2 into (3x - 1)."
                ),
                WorkedStep(
                    step_number=2,
                    action="Collect variable terms on LHS",
                    expression="6x - 2 - 4x = 4x + 10 - 4x  ==>  2x - 2 = 10",
                    reasoning="Subtract 4x from both sides."
                ),
                WorkedStep(
                    step_number=3,
                    action="Collect constants on RHS",
                    expression="2x - 2 + 2 = 10 + 2  ==>  2x = 12",
                    reasoning="Add 2 to both sides."
                ),
                WorkedStep(
                    step_number=4,
                    action="Isolate x by dividing by coefficient",
                    expression="(2x) / 2 = 12 / 2  ==>  x = 6",
                    reasoning="Divide both sides by 2."
                )
            ],
            common_pitfalls=[
                "Transposing a term without inverting its sign.",
                "Dropping negative signs when the coefficient of x is negative (e.g. -3x = 12 implies x = -4, not +4)."
            ],
            interactive_prompt="Solve for x: 3x + 4 = 19"
        )
    ),
    "MATH-C06": Concept(
        id="MATH-C06",
        code="VERIF_SUB",
        title="Verifying Solutions by Substitution",
        grade=8,
        subject="Mathematics",
        description="Substituting a candidate solution back into the original equation to prove equality and catch algebra errors.",
        prerequisites=["MATH-C01", "MATH-C02", "MATH-C05"],
        order_index=6,
        lesson=Lesson(
            concept_id="MATH-C06",
            title="Checking Your Work: Verification by Substitution",
            objective="Evaluate LHS and RHS independently with the solved value to verify mathematical equivalence.",
            key_principles=[
                "Never assume a solution is correct without checking.",
                "Substitute the candidate value into the ORIGINAL unsimplified equation.",
                "Compute LHS value and RHS value separately using correct order of operations.",
                "If LHS == RHS, the solution is verified; if LHS != RHS, rework the equation."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Given equation and candidate solution",
                    expression="5x - 3 = 2x + 9, candidate x = 4",
                    reasoning="We test if x = 4 makes both sides equal."
                ),
                WorkedStep(
                    step_number=2,
                    action="Evaluate Left Hand Side (LHS)",
                    expression="LHS = 5(4) - 3 = 20 - 3 = 17",
                    reasoning="Substitute 4 in place of x on the LHS."
                ),
                WorkedStep(
                    step_number=3,
                    action="Evaluate Right Hand Side (RHS)",
                    expression="RHS = 2(4) + 9 = 8 + 9 = 17",
                    reasoning="Substitute 4 in place of x on the RHS."
                ),
                WorkedStep(
                    step_number=4,
                    action="Compare LHS and RHS",
                    expression="LHS (17) == RHS (17) ==> VERIFIED",
                    reasoning="Since both sides equal 17, x = 4 is proven to be the exact correct solution."
                )
            ],
            common_pitfalls=[
                "Manipulating both sides simultaneously during a check instead of evaluating each side independently.",
                "Substituting into an intermediate line where a mistake already occurred."
            ],
            interactive_prompt="Check if x = 3 satisfies 4x - 5 = 7."
        )
    ),
    "MATH-C07": Concept(
        id="MATH-C07",
        code="RAT_PROP",
        title="Properties of Rational Numbers",
        grade=8,
        subject="Mathematics",
        description="Understanding closure, commutativity, associativity, and distributivity for rational numbers (p/q, q != 0), plus additive and multiplicative inverses.",
        prerequisites=["MATH-C01"],
        order_index=7,
        lesson=Lesson(
            concept_id="MATH-C07",
            title="Rational Numbers and Their Core Algebraic Properties",
            objective="Identify and apply algebraic properties (closure, commutative, associative, distributive, and inverses) to rational numbers.",
            key_principles=[
                "A rational number is any number expressible as p/q where p, q are integers and q != 0.",
                "The additive inverse of a/b is -a/b (their sum is 0).",
                "The multiplicative inverse (reciprocal) of a/b is b/a (their product is 1, a != 0).",
                "Rational numbers are dense: between any two rational numbers, there are infinitely many rational numbers."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find the additive and multiplicative inverse of -3/8",
                    expression="Given: -3/8",
                    reasoning="Additive inverse produces sum 0; reciprocal produces product 1."
                ),
                WorkedStep(
                    step_number=2,
                    action="Compute additive inverse",
                    expression="-(-3/8) = 3/8",
                    reasoning="Adding 3/8 to -3/8 yields 0."
                ),
                WorkedStep(
                    step_number=3,
                    action="Compute multiplicative inverse (reciprocal)",
                    expression="(-3/8)^(-1) = -8/3",
                    reasoning="Multiplying -3/8 by -8/3 yields +1."
                )
            ],
            common_pitfalls=[
                "Confusing additive inverse (changing sign) with multiplicative inverse (flipping fraction).",
                "Assuming 0 has a reciprocal (division by zero is undefined)."
            ],
            interactive_prompt="What is the reciprocal of -5/7?"
        )
    ),
    "MATH-C08": Concept(
        id="MATH-C08",
        code="RAT_OPS",
        title="Operations on Rational Numbers",
        grade=8,
        subject="Mathematics",
        description="Addition, subtraction, multiplication, and division of rational numbers with like and unlike denominators.",
        prerequisites=["MATH-C07"],
        order_index=8,
        lesson=Lesson(
            concept_id="MATH-C08",
            title="Arithmetic Operations with Rational Numbers",
            objective="Perform addition, subtraction, multiplication, and division with rational numbers using common denominators and reciprocals.",
            key_principles=[
                "To add or subtract fractions with unlike denominators, find the LCM of denominators.",
                "To divide by a rational number, multiply by its reciprocal: (a/b) / (c/d) = (a/b) * (d/c).",
                "Always reduce fractions to lowest terms by dividing by the HCF of numerator and denominator."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Solve: 2/5 + (-3/7)",
                    expression="LCM of 5 and 7 is 35",
                    reasoning="Convert both fractions to common denominator 35."
                ),
                WorkedStep(
                    step_number=2,
                    action="Express with common denominator",
                    expression="14/35 + (-15/35)",
                    reasoning="2*7 = 14, -3*5 = -15."
                ),
                WorkedStep(
                    step_number=3,
                    action="Combine numerators",
                    expression="(14 - 15) / 35 = -1/35",
                    reasoning="14 - 15 = -1."
                )
            ],
            common_pitfalls=[
                "Adding denominators directly: 1/2 + 1/3 != 2/5.",
                "Forgetting to invert the second fraction during division."
            ],
            interactive_prompt="Evaluate: -4/9 * 3/8."
        )
    ),
    "MATH-C09": Concept(
        id="MATH-C09",
        code="QUAD_POLY",
        title="Polygons and Angle Sum Property",
        grade=8,
        subject="Mathematics",
        description="Classifying regular and irregular polygons, interior angle sum formula (n - 2) * 180 deg, and exterior angle sum (360 deg).",
        prerequisites=["MATH-C01"],
        order_index=9,
        lesson=Lesson(
            concept_id="MATH-C09",
            title="Polygon Geometry & Angle Sum Relations",
            objective="Calculate interior and exterior angle sums for any n-sided polygon.",
            key_principles=[
                "A polygon is a simple closed curve made up entirely of line segments.",
                "Sum of interior angles of an n-sided polygon is S = (n - 2) * 180 degrees.",
                "Sum of measures of external angles of ANY convex polygon is always exactly 360 degrees.",
                "For a regular polygon with n sides, each exterior angle is 360 / n degrees."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find interior angle sum of a hexagon (n = 6)",
                    expression="Formula: S = (n - 2) * 180",
                    reasoning="Divide polygon into (n - 2) triangles."
                ),
                WorkedStep(
                    step_number=2,
                    action="Substitute n = 6",
                    expression="S = (6 - 2) * 180 = 4 * 180",
                    reasoning="6 - 2 = 4 triangles."
                ),
                WorkedStep(
                    step_number=3,
                    action="Compute final angle sum",
                    expression="S = 720 degrees",
                    reasoning="4 * 180 = 720."
                )
            ],
            common_pitfalls=[
                "Using n * 180 instead of (n - 2) * 180.",
                "Thinking exterior angle sum increases with the number of sides (it is always 360 degrees)."
            ],
            interactive_prompt="What is the measure of each exterior angle of a regular octagon (8 sides)?"
        )
    ),
    "MATH-C10": Concept(
        id="MATH-C10",
        code="QUAD_SPEC",
        title="Special Quadrilaterals and Their Properties",
        grade=8,
        subject="Mathematics",
        description="Properties of parallelograms, rhombuses, rectangles, squares, kites, and trapeziums.",
        prerequisites=["MATH-C09"],
        order_index=10,
        lesson=Lesson(
            concept_id="MATH-C10",
            title="Classification and Properties of Quadrilaterals",
            objective="Identify and prove properties of parallelograms, rhombuses, rectangles, and squares.",
            key_principles=[
                "In a parallelogram: opposite sides are equal, opposite angles are equal, and diagonals bisect each other.",
                "Adjacent angles of a parallelogram are supplementary (sum to 180 degrees).",
                "A rhombus has all sides equal and diagonals bisect each other perpendicularly (at 90 degrees).",
                "A rectangle has all angles equal to 90 degrees and diagonals of equal length.",
                "A square has all sides equal, all angles 90 degrees, and equal perpendicular bisecting diagonals."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find angle y in parallelogram ABCD where angle A = 70 degrees",
                    expression="Given: angle A = 70 degrees",
                    reasoning="Adjacent angles in a parallelogram are supplementary."
                ),
                WorkedStep(
                    step_number=2,
                    action="Apply supplementary relation",
                    expression="angle A + angle B = 180",
                    reasoning="Angle B is adjacent to Angle A."
                ),
                WorkedStep(
                    step_number=3,
                    action="Solve for angle B",
                    expression="angle B = 180 - 70 = 110 degrees",
                    reasoning="The opposite angle C = 70 and angle D = 110 degrees."
                )
            ],
            common_pitfalls=[
                "Assuming diagonals of all parallelograms are equal (only rectangles and squares have equal diagonals).",
                "Confusing a rhombus with a square (a rhombus does not require 90 degree interior angles)."
            ],
            interactive_prompt="If one angle of a parallelogram is 80 degrees, find all its other angles."
        )
    ),
    "MATH-C11": Concept(
        id="MATH-C11",
        code="DATA_FREQ",
        title="Organizing and Grouping Data",
        grade=8,
        subject="Mathematics",
        description="Constructing frequency distributions, class intervals, upper/lower limits, and histograms.",
        prerequisites=["MATH-C01"],
        order_index=11,
        lesson=Lesson(
            concept_id="MATH-C11",
            title="Frequency Distributions and Grouped Data",
            objective="Group raw observational data into class intervals and represent them using histograms.",
            key_principles=[
                "Class interval represents data groups (e.g., 20-30 has lower limit 20, upper limit 30, class size 10).",
                "Class mark is the midpoint: (Lower limit + Upper limit) / 2.",
                "A histogram displays continuous grouped data using adjacent bars with no gaps between them."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find class size and class mark for interval 40-50",
                    expression="Lower limit = 40, Upper limit = 50",
                    reasoning="Read boundaries from interval notation."
                ),
                WorkedStep(
                    step_number=2,
                    action="Calculate class size (width)",
                    expression="Class size = 50 - 40 = 10",
                    reasoning="Upper limit minus lower limit."
                ),
                WorkedStep(
                    step_number=3,
                    action="Calculate class mark (midpoint)",
                    expression="Class mark = (40 + 50) / 2 = 45",
                    reasoning="Midpoint is the average of boundaries."
                )
            ],
            common_pitfalls=[
                "Leaving spaces between bars in a histogram (histograms represent continuous intervals, unlike bar graphs).",
                "Miscounting boundary values (by convention, 30 belongs to 30-40, not 20-30)."
            ],
            interactive_prompt="What is the class mark of the interval 25-35?"
        )
    ),
    "MATH-C12": Concept(
        id="MATH-C12",
        code="DATA_PIE",
        title="Circle Graphs (Pie Charts) and Probability",
        grade=8,
        subject="Mathematics",
        description="Calculating central angles for pie charts (fraction * 360 deg) and computing event probabilities.",
        prerequisites=["MATH-C11"],
        order_index=12,
        lesson=Lesson(
            concept_id="MATH-C12",
            title="Pie Charts and Theoretical Probability",
            objective="Calculate central angles to draw pie charts and calculate probabilities of equally likely outcomes.",
            key_principles=[
                "Total central angle of a circle is 360 degrees.",
                "Central angle for a component = (Component Value / Total Value) * 360 degrees.",
                "Probability of an event P(E) = Number of favourable outcomes / Total number of equally likely outcomes.",
                "0 <= P(E) <= 1 for every event."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find central angle for 15 students liking math out of a class of 60",
                    expression="Fraction = 15 / 60 = 1/4",
                    reasoning="Find the proportion of the whole."
                ),
                WorkedStep(
                    step_number=2,
                    action="Multiply by 360 degrees",
                    expression="Angle = (1/4) * 360 = 90 degrees",
                    reasoning="Each fourth of a circle occupies 90 degrees."
                )
            ],
            common_pitfalls=[
                "Multiplying by 100 instead of 360 when finding pie chart angles.",
                "Calculating probability greater than 1."
            ],
            interactive_prompt="A die is thrown once. What is the probability of rolling a prime number (2, 3, 5)?"
        )
    ),
    "MATH-C13": Concept(
        id="MATH-C13",
        code="SQ_NUM",
        title="Square Numbers and Pythagorean Triplets",
        grade=8,
        subject="Mathematics",
        description="Properties of perfect squares, unit digit patterns, sum of consecutive odd numbers, and Pythagorean triplets (2m, m^2 - 1, m^2 + 1).",
        prerequisites=["MATH-C01"],
        order_index=13,
        lesson=Lesson(
            concept_id="MATH-C13",
            title="Square Numbers and Pythagorean Triplets",
            objective="Identify square number properties and generate Pythagorean triplets.",
            key_principles=[
                "A number ending in 2, 3, 7, or 8 is NEVER a perfect square.",
                "A square number can only end in 0, 1, 4, 5, 6, or 9.",
                "The sum of the first n odd natural numbers is n^2: 1 + 3 + 5 + ... = n^2.",
                "For any natural number m > 1, (2m, m^2 - 1, m^2 + 1) forms a Pythagorean triplet: (2m)^2 + (m^2 - 1)^2 = (m^2 + 1)^2."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find a Pythagorean triplet whose smallest member is 6",
                    expression="Set 2m = 6",
                    reasoning="Using the form (2m, m^2 - 1, m^2 + 1)."
                ),
                WorkedStep(
                    step_number=2,
                    action="Solve for m",
                    expression="m = 3",
                    reasoning="6 / 2 = 3."
                ),
                WorkedStep(
                    step_number=3,
                    action="Compute other two members",
                    expression="m^2 - 1 = 3^2 - 1 = 8; m^2 + 1 = 3^2 + 1 = 10",
                    reasoning="Check: 6^2 + 8^2 = 36 + 64 = 100 = 10^2. Triplet is (6, 8, 10)."
                )
            ],
            common_pitfalls=[
                "Setting m^2 - 1 = 6 instead of 2m = 6 (which would make m = sqrt(7), not an integer).",
                "Assuming odd numbers cannot be part of Pythagorean triplets."
            ],
            interactive_prompt="What is the unit digit of the square of 28?"
        )
    ),
    "MATH-C14": Concept(
        id="MATH-C14",
        code="SQ_ROOT",
        title="Finding Square Roots",
        grade=8,
        subject="Mathematics",
        description="Prime factorisation and long division methods for finding square roots of integers and decimals.",
        prerequisites=["MATH-C13"],
        order_index=14,
        lesson=Lesson(
            concept_id="MATH-C14",
            title="Methods for Finding Square Roots",
            objective="Calculate exact square roots using prime factorisation and long division.",
            key_principles=[
                "Square root is the inverse operation of squaring: sqrt(x^2) = x for positive x.",
                "In prime factorisation, group identical prime factors in pairs: sqrt(p^2 * q^2) = p * q.",
                "In the division method, place bars over pairs of digits starting from the unit digit to the left."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find sqrt(576) by prime factorisation",
                    expression="576 = 2 * 2 * 2 * 2 * 2 * 2 * 3 * 3",
                    reasoning="Factor into prime components."
                ),
                WorkedStep(
                    step_number=2,
                    action="Pair the factors",
                    expression="576 = (2*2) * (2*2) * (2*2) * (3*3)",
                    reasoning="Group into pairs of identical primes."
                ),
                WorkedStep(
                    step_number=3,
                    action="Extract one factor from each pair",
                    expression="sqrt(576) = 2 * 2 * 2 * 3 = 24",
                    reasoning="24 * 24 = 576."
                )
            ],
            common_pitfalls=[
                "Halving the number instead of finding its square root (e.g. thinking sqrt(16) is 8).",
                "Leaving unpaired factors under the root."
            ],
            interactive_prompt="Find the square root of 784 using prime factorisation."
        )
    ),
    "MATH-C15": Concept(
        id="MATH-C15",
        code="CB_NUM",
        title="Cube Numbers and Patterns",
        grade=8,
        subject="Mathematics",
        description="Properties of cubes of numbers, unit digit rules, and patterns of adding consecutive odd numbers.",
        prerequisites=["MATH-C01"],
        order_index=15,
        lesson=Lesson(
            concept_id="MATH-C15",
            title="Understanding Perfect Cubes",
            objective="Recognize perfect cubes and predict their unit digits.",
            key_principles=[
                "The cube of a number is the number multiplied by itself three times: n^3 = n * n * n.",
                "Cubes of even numbers are always even; cubes of odd numbers are always odd.",
                "A natural number n has cube ending in same digit if unit digit is 0, 1, 4, 5, 6, 9. If unit digit is 2, cube ends in 8 (and vice versa: 8 -> 2; 3 -> 7; 7 -> 3)."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Examine 12^3 unit digit",
                    expression="Unit digit of 12 is 2",
                    reasoning="2^3 = 8."
                ),
                WorkedStep(
                    step_number=2,
                    action="Confirm cube calculation",
                    expression="12 * 12 * 12 = 144 * 12 = 1728",
                    reasoning="Unit digit is indeed 8."
                )
            ],
            common_pitfalls=[
                "Multiplying the number by 3 instead of cubing (e.g. thinking 4^3 = 12 instead of 64).",
                "Confusing cube root with square root."
            ],
            interactive_prompt="What is the unit digit of the cube of 27?"
        )
    ),
    "MATH-C16": Concept(
        id="MATH-C16",
        code="CB_ROOT",
        title="Finding Cube Roots through Prime Factorisation",
        grade=8,
        subject="Mathematics",
        description="Finding cube roots by grouping prime factors into triplets.",
        prerequisites=["MATH-C15"],
        order_index=16,
        lesson=Lesson(
            concept_id="MATH-C16",
            title="Computing Cube Roots",
            objective="Determine the cube root of a given number using prime factorisation.",
            key_principles=[
                "The cube root of x (written cbrt(x)) is the number whose cube is x.",
                "To find the cube root: resolve the number into prime factors and make triplets of equal factors.",
                "Extract one factor from each triplet and take their product."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find cbrt(1728) by prime factorisation",
                    expression="1728 = 2 * 2 * 2 * 2 * 2 * 2 * 3 * 3 * 3",
                    reasoning="Perform continuous division by primes."
                ),
                WorkedStep(
                    step_number=2,
                    action="Group into triplets",
                    expression="(2*2*2) * (2*2*2) * (3*3*3)",
                    reasoning="Each group contains 3 identical factors."
                ),
                WorkedStep(
                    step_number=3,
                    action="Extract one factor per triplet",
                    expression="cbrt(1728) = 2 * 2 * 3 = 12",
                    reasoning="Check: 12^3 = 1728."
                )
            ],
            common_pitfalls=[
                "Grouping in pairs (for square roots) instead of triplets.",
                "Overlooking negative signs (note: cbrt(-x) = -cbrt(x))."
            ],
            interactive_prompt="Find the cube root of 3375."
        )
    ),
    "MATH-C17": Concept(
        id="MATH-C17",
        code="COMP_PCT",
        title="Ratios, Percentages, Discounts and Taxes",
        grade=8,
        subject="Mathematics",
        description="Comparing quantities using ratios, percentage increase/decrease, discount = Marked Price - Sale Price, and GST calculation.",
        prerequisites=["MATH-C08"],
        order_index=17,
        lesson=Lesson(
            concept_id="MATH-C17",
            title="Commercial Arithmetic & Percentage Applications",
            objective="Solve problems involving ratios, discounts, profit/loss, and sales tax/GST.",
            key_principles=[
                "A ratio compares two quantities of the same unit: a:b = a/b.",
                "Discount = Marked Price (MP) - Sale Price (SP).",
                "Discount % = (Discount / MP) * 100.",
                "Profit % = (Profit / CP) * 100; Loss % = (Loss / CP) * 100 (always calculated on Cost Price CP).",
                "GST is added to the bill value: Final Price = Price + (GST % * Price)."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find selling price of an item marked at Rs 840 with a 15% discount",
                    expression="Discount = 15% of 840 = (15/100) * 840",
                    reasoning="Calculate discount amount."
                ),
                WorkedStep(
                    step_number=2,
                    action="Compute discount value",
                    expression="Discount = 0.15 * 840 = Rs 126",
                    reasoning="84 * 1.5 = 126."
                ),
                WorkedStep(
                    step_number=3,
                    action="Calculate Sale Price",
                    expression="SP = MP - Discount = 840 - 126 = Rs 714",
                    reasoning="Deduct discount from marked price."
                )
            ],
            common_pitfalls=[
                "Calculating profit or loss percentage on Selling Price instead of Cost Price.",
                "Calculating discount on Sale Price instead of Marked Price."
            ],
            interactive_prompt="An item costing Rs 500 is sold for Rs 600. Find the profit percentage."
        )
    ),
    "MATH-C18": Concept(
        id="MATH-C18",
        code="COMP_CI",
        title="Compound Interest",
        grade=8,
        subject="Mathematics",
        description="Understanding simple vs compound interest, annual and semi-annual compounding formulas: A = P(1 + R/100)^n and CI = A - P.",
        prerequisites=["MATH-C17"],
        order_index=18,
        lesson=Lesson(
            concept_id="MATH-C18",
            title="Compound Interest and Growth Formulas",
            objective="Calculate compound interest and total amount for annual compounding periods.",
            key_principles=[
                "Simple Interest: I = (P * R * T) / 100; principal remains constant every year.",
                "Compound Interest: Interest earned in previous year is added to principal for the next year.",
                "Amount formula: A = P * (1 + R/100)^n where P is Principal, R is annual rate %, n is time in years.",
                "Compound Interest CI = A - P."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find Amount for P = Rs 10000, R = 10% per annum, n = 2 years",
                    expression="A = 10000 * (1 + 10/100)^2",
                    reasoning="Substitute into compound interest formula."
                ),
                WorkedStep(
                    step_number=2,
                    action="Simplify the fraction",
                    expression="A = 10000 * (11/10)^2 = 10000 * (121/100)",
                    reasoning="1 + 1/10 = 11/10; (11/10)^2 = 121/100."
                ),
                WorkedStep(
                    step_number=3,
                    action="Calculate final Amount and CI",
                    expression="A = Rs 12100; CI = 12100 - 10000 = Rs 2100",
                    reasoning="Compare with Simple Interest: (10000*10*2)/100 = Rs 2000."
                )
            ],
            common_pitfalls=[
                "Confusing Amount (A) with Interest (CI = A - P).",
                "Forgetting to adjust rate and time when interest is compounded half-yearly (R/2, 2n)."
            ],
            interactive_prompt="Find CI on Rs 8000 for 1 year at 5% compounded annually."
        )
    ),
    "MATH-C19": Concept(
        id="MATH-C19",
        code="ALG_POLY_MULT",
        title="Multiplication of Algebraic Expressions",
        grade=8,
        subject="Mathematics",
        description="Multiplication of monomials by monomials, monomials by polynomials, and binomials by binomials using the distributive property.",
        prerequisites=["MATH-C04"],
        order_index=19,
        lesson=Lesson(
            concept_id="MATH-C19",
            title="Multiplication of Polynomial Expressions",
            objective="Multiply polynomials systematically using distributive law and exponent rules.",
            key_principles=[
                "Monomial * Monomial: Multiply coefficients, add exponents of same base: (3x^2)(4x^3) = 12x^5.",
                "Monomial * Binomial: a(b + c) = ab + ac.",
                "Binomial * Binomial: (a + b)(c + d) = a(c + d) + b(c + d) = ac + ad + bc + bd."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Multiply: (2x + 3)(3x - 5)",
                    expression="(2x)(3x - 5) + 3(3x - 5)",
                    reasoning="Distribute first binomial across second."
                ),
                WorkedStep(
                    step_number=2,
                    action="Expand individual products",
                    expression="6x^2 - 10x + 9x - 15",
                    reasoning="2x*3x=6x^2, 2x*(-5)=-10x, 3*3x=9x, 3*(-5)=-15."
                ),
                WorkedStep(
                    step_number=3,
                    action="Combine like terms",
                    expression="6x^2 - x - 15",
                    reasoning="-10x + 9x = -x."
                )
            ],
            common_pitfalls=[
                "Multiplying exponents instead of adding them when bases match: x^2 * x^3 = x^5, not x^6.",
                "Dropping negative signs during distribution: -(2x - 3) = -2x + 3."
            ],
            interactive_prompt="Expand: (x + 4)(x + 7)."
        )
    ),
    "MATH-C20": Concept(
        id="MATH-C20",
        code="ALG_IDENT",
        title="Standard Algebraic Identities",
        grade=8,
        subject="Mathematics",
        description="Applications of standard identities: (a + b)^2, (a - b)^2, (a + b)(a - b), and (x + a)(x + b).",
        prerequisites=["MATH-C19"],
        order_index=20,
        lesson=Lesson(
            concept_id="MATH-C20",
            title="Mastering Standard Algebraic Identities",
            objective="Apply standard algebraic identities to simplify expressions and compute numerical products rapidly.",
            key_principles=[
                "Identity I: (a + b)^2 = a^2 + 2ab + b^2.",
                "Identity II: (a - b)^2 = a^2 - 2ab + b^2.",
                "Identity III: (a + b)(a - b) = a^2 - b^2.",
                "Identity IV: (x + a)(x + b) = x^2 + (a + b)x + ab."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Evaluate 103 * 97 using an algebraic identity",
                    expression="(100 + 3)(100 - 3)",
                    reasoning="Recognize form (a + b)(a - b) with a = 100, b = 3."
                ),
                WorkedStep(
                    step_number=2,
                    action="Apply Identity III: a^2 - b^2",
                    expression="100^2 - 3^2",
                    reasoning="(a + b)(a - b) = a^2 - b^2."
                ),
                WorkedStep(
                    step_number=3,
                    action="Calculate result",
                    expression="10000 - 9 = 9991",
                    reasoning="Rapid mental calculation without long multiplication."
                )
            ],
            common_pitfalls=[
                "Forgetting the middle term 2ab: (a + b)^2 != a^2 + b^2.",
                "Mixing up signs in (a - b)^2: the middle term is -2ab, but the last term is +b^2."
            ],
            interactive_prompt="Expand (2x + 5y)^2 using Identity I."
        )
    ),
    "MATH-C21": Concept(
        id="MATH-C21",
        code="MENS_AREA",
        title="Area of Trapezium, Rhombus and Polygons",
        grade=8,
        subject="Mathematics",
        description="Formulas for area of trapezium = 1/2 * (a + b) * h, area of rhombus = 1/2 * d1 * d2, and area of general polygons by triangulation.",
        prerequisites=["MATH-C10"],
        order_index=21,
        lesson=Lesson(
            concept_id="MATH-C21",
            title="Mensuration: Surface Areas of 2D Polygons",
            objective="Calculate area of trapeziums, rhombuses, and irregular polygons.",
            key_principles=[
                "Area of Trapezium = (1/2) * (sum of parallel sides) * (perpendicular distance h) = (1/2)(a + b)h.",
                "Area of Rhombus = (1/2) * (product of diagonals) = (1/2) * d1 * d2.",
                "Area of general quadrilateral = (1/2) * diagonal * (h1 + h2) where h1, h2 are perpendicular offsets from opposite vertices."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find area of trapezium with parallel sides 10 cm and 14 cm, and height 6 cm",
                    expression="Formula: Area = (1/2)(a + b)h",
                    reasoning="a = 10, b = 14, h = 6."
                ),
                WorkedStep(
                    step_number=2,
                    action="Substitute values",
                    expression="Area = (1/2)(10 + 14) * 6 = (1/2)(24) * 6",
                    reasoning="Sum of parallel sides is 24."
                ),
                WorkedStep(
                    step_number=3,
                    action="Compute final area",
                    expression="Area = 12 * 6 = 72 cm^2",
                    reasoning="Units are square centimeters."
                )
            ],
            common_pitfalls=[
                "Using the non-parallel slant height instead of the perpendicular height h.",
                "Confusing perimeter units (cm) with area units (cm^2)."
            ],
            interactive_prompt="Find the area of a rhombus whose diagonals are 16 cm and 12 cm."
        )
    ),
    "MATH-C22": Concept(
        id="MATH-C22",
        code="MENS_VOL",
        title="Surface Area and Volume of 3D Solids",
        grade=8,
        subject="Mathematics",
        description="Total surface area, lateral surface area, and volume of cuboid, cube, and right circular cylinder.",
        prerequisites=["MATH-C21"],
        order_index=22,
        lesson=Lesson(
            concept_id="MATH-C22",
            title="Surface Area and Volume of Cuboids and Cylinders",
            objective="Calculate total surface area, lateral surface area, and volume of 3D solids.",
            key_principles=[
                "Cuboid: Total Surface Area TSA = 2(lb + bh + hl); Volume V = l * b * h.",
                "Cube: TSA = 6a^2; Lateral Area LSA = 4a^2; Volume V = a^3.",
                "Cylinder: Curved Surface Area CSA = 2*pi*r*h; Total Surface Area TSA = 2*pi*r*(r + h); Volume V = pi*r^2*h.",
                "1 Liter = 1000 cm^3; 1 m^3 = 1000 Liters."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Find volume of a cylinder with radius r = 7 cm and height h = 10 cm",
                    expression="V = pi * r^2 * h",
                    reasoning="Use pi = 22/7."
                ),
                WorkedStep(
                    step_number=2,
                    action="Substitute dimensions",
                    expression="V = (22/7) * 7 * 7 * 10",
                    reasoning="Cancel 7 in denominator with radius."
                ),
                WorkedStep(
                    step_number=3,
                    action="Compute volume",
                    expression="V = 22 * 7 * 10 = 1540 cm^3",
                    reasoning="Volume is 1540 cubic centimeters."
                )
            ],
            common_pitfalls=[
                "Confusing diameter with radius (always divide diameter by 2).",
                "Mixing units (e.g. centimeters with meters without converting)."
            ],
            interactive_prompt="What is the total surface area of a cube of edge length 5 cm?"
        )
    ),
    "MATH-C23": Concept(
        id="MATH-C23",
        code="EXP_NEG",
        title="Powers with Negative Exponents",
        grade=8,
        subject="Mathematics",
        description="Understanding negative exponents as multiplicative inverses: a^(-m) = 1 / a^m (a != 0).",
        prerequisites=["MATH-C08"],
        order_index=23,
        lesson=Lesson(
            concept_id="MATH-C23",
            title="Negative Exponents and Reciprocals",
            objective="Evaluate and simplify expressions containing negative integral exponents.",
            key_principles=[
                "For any non-zero integer a, a^(-m) = 1 / a^m.",
                "a^(-m) is the multiplicative inverse of a^m: a^m * a^(-m) = a^0 = 1.",
                "(a/b)^(-m) = (b/a)^m."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Evaluate (2/3)^(-3)",
                    expression="Apply rule: (a/b)^(-m) = (b/a)^m",
                    reasoning="Invert the fraction to make exponent positive."
                ),
                WorkedStep(
                    step_number=2,
                    action="Invert base",
                    expression="(3/2)^3",
                    reasoning="Reciprocal of 2/3 is 3/2."
                ),
                WorkedStep(
                    step_number=3,
                    action="Compute power",
                    expression="3^3 / 2^3 = 27 / 8",
                    reasoning="3*3*3 = 27; 2*2*2 = 8."
                )
            ],
            common_pitfalls=[
                "Making the base negative because the exponent is negative: 2^(-3) != -8 (it is 1/8).",
                "Confusing -3^2 (= -9) with (-3)^2 (= +9)."
            ],
            interactive_prompt="Find the value of 5^(-2)."
        )
    ),
    "MATH-C24": Concept(
        id="MATH-C24",
        code="EXP_LAWS",
        title="Laws of Exponents and Scientific Form",
        grade=8,
        subject="Mathematics",
        description="Applying exponent laws (a^m * a^n = a^(m+n), a^m / a^n = a^(m-n), (a^m)^n = a^(mn)) and standard scientific form m * 10^k.",
        prerequisites=["MATH-C23"],
        order_index=24,
        lesson=Lesson(
            concept_id="MATH-C24",
            title="Laws of Exponents & Standard Scientific Form",
            objective="Simplify complex exponential expressions and express very small or large numbers in standard scientific notation.",
            key_principles=[
                "Product Law: a^m * a^n = a^(m + n).",
                "Quotient Law: a^m / a^n = a^(m - n).",
                "Power of Power: (a^m)^n = a^(m * n).",
                "Product Base: a^m * b^m = (a * b)^m.",
                "Quotient Base: a^m / b^m = (a / b)^m.",
                "Standard Form: k * 10^n where 1.0 <= k < 10 and n is an integer."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Express 0.000035 in standard scientific form",
                    expression="Shift decimal point 5 places to the right",
                    reasoning="Number must be between 1.0 and 10.0: k = 3.5."
                ),
                WorkedStep(
                    step_number=2,
                    action="Assign negative power of 10",
                    expression="3.5 * 10^(-5)",
                    reasoning="Moving decimal to the right indicates division by 10^5."
                )
            ],
            common_pitfalls=[
                "Adding exponents during division instead of subtracting.",
                "Leaving the mantissa k >= 10 in standard form (e.g. writing 35 * 10^(-6) instead of 3.5 * 10^(-5))."
            ],
            interactive_prompt="Simplify: (3^5 * 3^(-2)) / 3^2."
        )
    ),
    "MATH-C25": Concept(
        id="MATH-C25",
        code="PROP_DIR",
        title="Direct Proportion",
        grade=8,
        subject="Mathematics",
        description="Identifying direct proportion relationships where x/y = k (constant ratio), setting up proportional equations.",
        prerequisites=["MATH-C08"],
        order_index=25,
        lesson=Lesson(
            concept_id="MATH-C25",
            title="Direct Variation and Proportional Reasoning",
            objective="Solve problems where an increase in one quantity produces a proportionate increase in another.",
            key_principles=[
                "Two quantities x and y are in direct proportion if x / y = k (a constant).",
                "If x1 and y1 are initial values, and x2, y2 are new values: x1 / y1 = x2 / y2.",
                "Examples: Distance covered and time taken at uniform speed; quantity of goods and total cost."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="If 14 metres of cloth costs Rs 1890, find the cost of 6 metres",
                    expression="Set up ratio: x1 / y1 = x2 / y2",
                    reasoning="Cloth length and cost are in direct proportion."
                ),
                WorkedStep(
                    step_number=2,
                    action="Substitute values: 14 / 1890 = 6 / y2",
                    expression="14 * y2 = 6 * 1890",
                    reasoning="Cross-multiply to solve for y2."
                ),
                WorkedStep(
                    step_number=3,
                    action="Solve for y2",
                    expression="y2 = (6 * 1890) / 14 = 6 * 135 = Rs 810",
                    reasoning="Cost of 6 metres is Rs 810."
                )
            ],
            common_pitfalls=[
                "Inverting the ratio when cross-multiplying.",
                "Assuming every increasing relationship is direct proportion (ratio must be constant!)."
            ],
            interactive_prompt="If 8 pens cost Rs 96, how much do 15 pens cost?"
        )
    ),
    "MATH-C26": Concept(
        id="MATH-C26",
        code="PROP_INV",
        title="Inverse Proportion",
        grade=8,
        subject="Mathematics",
        description="Identifying inverse proportion relationships where x * y = k (constant product), solving worker/days and speed/time problems.",
        prerequisites=["MATH-C25"],
        order_index=26,
        lesson=Lesson(
            concept_id="MATH-C26",
            title="Inverse Variation and Constant Product",
            objective="Recognize and solve inverse proportion problems where increase in one variable decreases the other.",
            key_principles=[
                "Two quantities x and y are in inverse proportion if x * y = k (a constant).",
                "If x1, y1 and x2, y2 are corresponding values: x1 * y1 = x2 * y2.",
                "Examples: Number of workers and time taken to finish a job; speed of vehicle and travel time for fixed distance."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="If 6 workers build a wall in 24 hours, how many hours will 8 workers take?",
                    expression="x1 * y1 = x2 * y2",
                    reasoning="Workers and hours are inversely proportional (more workers take less time)."
                ),
                WorkedStep(
                    step_number=2,
                    action="Substitute values: 6 * 24 = 8 * y2",
                    expression="144 = 8 * y2",
                    reasoning="Total worker-hours is constant = 144."
                ),
                WorkedStep(
                    step_number=3,
                    action="Solve for y2",
                    expression="y2 = 144 / 8 = 18 hours",
                    reasoning="8 workers take 18 hours."
                )
            ],
            common_pitfalls=[
                "Treating inverse proportion as direct proportion: writing 6/24 = 8/y instead of 6*24 = 8*y.",
                "Failing to check if the answer makes common sense (more workers must take FEWER hours!)."
            ],
            interactive_prompt="A car travelling at 60 km/h takes 4 hours. How long will it take at 80 km/h?"
        )
    ),
    "MATH-C27": Concept(
        id="MATH-C27",
        code="FACT_IDENT",
        title="Factorisation by Common Factors and Identities",
        grade=8,
        subject="Mathematics",
        description="Factorising algebraic expressions using common monomial extraction, regrouping terms, and reverse algebraic identities.",
        prerequisites=["MATH-C20"],
        order_index=27,
        lesson=Lesson(
            concept_id="MATH-C27",
            title="Techniques of Algebraic Factorisation",
            objective="Factorise polynomials completely using common factors, regrouping, and standard identities.",
            key_principles=[
                "Factorisation expresses an algebraic sum/difference as a product of factors.",
                "Common factor method: 6x^2 + 9x = 3x(2x + 3).",
                "Difference of squares: a^2 - b^2 = (a + b)(a - b).",
                "Perfect square trinomials: a^2 + 2ab + b^2 = (a + b)^2; a^2 - 2ab + b^2 = (a - b)^2.",
                "Quadratic trinomials: x^2 + (a + b)x + ab = (x + a)(x + b)."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Factorise: 49x^2 - 36",
                    expression="(7x)^2 - (6)^2",
                    reasoning="Recognize difference of two perfect squares: a^2 - b^2."
                ),
                WorkedStep(
                    step_number=2,
                    action="Apply identity: a^2 - b^2 = (a + b)(a - b)",
                    expression="(7x + 6)(7x - 6)",
                    reasoning="a = 7x, b = 6."
                )
            ],
            common_pitfalls=[
                "Stopping before factoring is complete (e.g. factoring 4x^2 - 16 as 4(x^2 - 4) but forgetting (x-2)(x+2)).",
                "Sign error when factoring negative common factors: -3x + 6 = -3(x - 2), not -3(x + 2)."
            ],
            interactive_prompt="Factorise: x^2 + 7x + 12."
        )
    ),
    "MATH-C28": Concept(
        id="MATH-C28",
        code="FACT_DIV",
        title="Division of Algebraic Expressions",
        grade=8,
        subject="Mathematics",
        description="Dividing monomials by monomials, polynomials by monomials, and polynomials by polynomials using factor cancellation.",
        prerequisites=["MATH-C27"],
        order_index=28,
        lesson=Lesson(
            concept_id="MATH-C28",
            title="Division and Simplification of Expressions",
            objective="Divide algebraic expressions cleanly by factorising numerator and canceling common factors.",
            key_principles=[
                "Monomial by Monomial: Divide coefficients and subtract exponents of like variables.",
                "Polynomial by Monomial: Divide each term in polynomial by monomial divisor.",
                "Polynomial by Polynomial: First factorise both numerator and denominator completely, then cancel identical factor binomials."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Divide (x^2 + 7x + 10) by (x + 2)",
                    expression="Numerator = x^2 + 7x + 10",
                    reasoning="Factorise the numerator first."
                ),
                WorkedStep(
                    step_number=2,
                    action="Factorise numerator",
                    expression="(x + 2)(x + 5)",
                    reasoning="Find numbers whose product is 10 and sum is 7: 2 and 5."
                ),
                WorkedStep(
                    step_number=3,
                    action="Cancel common factor (x + 2)",
                    expression="[(x + 2)(x + 5)] / (x + 2) = x + 5",
                    reasoning="(x + 2) cancels out."
                )
            ],
            common_pitfalls=[
                "Canceling individual terms across addition: (x^2 + 5) / x != x + 5.",
                "Forgetting to check if denominator is non-zero."
            ],
            interactive_prompt="Divide: (28x^4) / (7x^2)."
        )
    ),
    "MATH-C29": Concept(
        id="MATH-C29",
        code="GRAPH_COORD",
        title="Cartesian Plane and Coordinates",
        grade=8,
        subject="Mathematics",
        description="Understanding horizontal x-axis, vertical y-axis, origin (0, 0), quadrants, and plotting ordered pairs (x, y).",
        prerequisites=["MATH-C01"],
        order_index=29,
        lesson=Lesson(
            concept_id="MATH-C29",
            title="The Coordinate Plane & Point Plotting",
            objective="Plot and read coordinates (x, y) accurately in all four quadrants.",
            key_principles=[
                "The horizontal axis is the x-axis; vertical axis is the y-axis; intersection is origin (0, 0).",
                "In ordered pair (x, y), x is abscissa (horizontal displacement) and y is ordinate (vertical displacement).",
                "Sign conventions: Quadrant I (+, +), Quadrant II (-, +), Quadrant III (-, -), Quadrant IV (+, -).",
                "Any point on the x-axis has y = 0: (x, 0). Any point on the y-axis has x = 0: (0, y)."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Identify coordinates of a point 4 units right of origin and 3 units down",
                    expression="Horizontal shift = +4; Vertical shift = -3",
                    reasoning="Right is positive x, down is negative y."
                ),
                WorkedStep(
                    step_number=2,
                    action="Form ordered pair",
                    expression="(4, -3)",
                    reasoning="x-coordinate first, then y-coordinate."
                ),
                WorkedStep(
                    step_number=3,
                    action="Identify quadrant",
                    expression="Quadrant IV",
                    reasoning="(+, -) corresponds to Quadrant IV."
                )
            ],
            common_pitfalls=[
                "Reversing x and y coordinates: plotting (3, 5) as (5, 3).",
                "Confusing which coordinate is zero on the axes."
            ],
            interactive_prompt="In which quadrant does the point (-3, -5) lie?"
        )
    ),
    "MATH-C30": Concept(
        id="MATH-C30",
        code="GRAPH_LINEAR",
        title="Reading and Interpreting Linear Graphs",
        grade=8,
        subject="Mathematics",
        description="Interpreting continuous linear graphs, rate of change, distance-time graphs, and distinguishing dependent vs independent variables.",
        prerequisites=["MATH-C29", "MATH-C05"],
        order_index=30,
        lesson=Lesson(
            concept_id="MATH-C30",
            title="Linear Graphs and Real-World Interpretations",
            objective="Read and interpret relationships between independent and dependent variables on a line graph.",
            key_principles=[
                "A line graph consists of bits of line segments joined consecutively; when it is a single unbroken straight line, it is a linear graph.",
                "Independent variable is usually plotted along the horizontal x-axis (e.g., Time, Quantity).",
                "Dependent variable is plotted along the vertical y-axis (e.g., Distance, Cost).",
                "Slope or steepness of the line indicates the rate of change (e.g. Distance / Time = Speed)."
            ],
            worked_steps=[
                WorkedStep(
                    step_number=1,
                    action="Determine distance traveled at time t = 3 hours from a linear graph passing through (0, 0) and (2, 80)",
                    expression="Speed = 80 km / 2 hours = 40 km/h",
                    reasoning="Compute constant rate of change (slope)."
                ),
                WorkedStep(
                    step_number=2,
                    action="Calculate distance at t = 3",
                    expression="Distance = Speed * Time = 40 * 3 = 120 km",
                    reasoning="Multiply constant speed by target time."
                )
            ],
            common_pitfalls=[
                "Swapping independent and dependent variables on the axes.",
                "Assuming non-linear relationships can be evaluated using a single constant slope."
            ],
            interactive_prompt="If a line passes through (1, 15) and (3, 45), what is the y-value when x = 4?"
        )
    )
}


def get_concept(concept_id: str) -> Concept:
    if concept_id not in CONCEPTS_REGISTRY:
        raise KeyError(f"Concept '{concept_id}' not found in registry.")
    return CONCEPTS_REGISTRY[concept_id]


def get_all_concepts() -> List[Concept]:
    return sorted(list(CONCEPTS_REGISTRY.values()), key=lambda c: c.order_index)


def get_prerequisite_graph() -> Dict[str, List[str]]:
    return {c.id: c.prerequisites for c in CONCEPTS_REGISTRY.values()}

