"""
SUTRA LEARN — Deterministic Mathematical Output Validator
Verifies algebraic transformation steps, arithmetic operations, rational numbers,
exponents, geometry formulas, commercial arithmetic, and equation consistency
across NCERT Class 8 Mathematics.
"""

import re
import math
import logging
from fractions import Fraction
from typing import List, Tuple, Optional, Dict, Any, Union

logger = logging.getLogger("sutra.ai.math_validator")


class MathematicalValidator:
    """
    Comprehensive deterministic mathematical validator for NCERT Class 8 topics:
    - Linear Equations in One Variable
    - Rational Numbers & Arithmetic
    - Exponents and Powers
    - Squares, Cubes and Roots
    - Algebraic Identities
    - Commercial Mathematics (Percentages, Discounts, Profit/Loss)
    - Geometry & Quadrilaterals (Angle Sums)
    - Mensuration (Perimeter, Area, Volume)
    - Direct and Inverse Proportions
    """

    @staticmethod
    def parse_linear_equation(eq_str: str) -> Optional[float]:
        """
        Parses simple linear equations into single-variable root x*.
        Supports:
          ax + b = c
          ax - b = c
          ax = b
          x + b = c
          ax + b = cx + d
        Returns solution x* if valid single-variable linear equation.
        """
        # Clean equation string
        s = eq_str.replace(" ", "").replace("−", "-").replace("×", "*")
        if "=" not in s:
            return None
        parts = s.split("=")
        if len(parts) != 2:
            return None

        lhs, rhs = parts[0], parts[1]

        def extract_terms(expr: str) -> Tuple[float, float]:
            """Returns (x_coeff, constant)"""
            term_matches = re.findall(r'([+-]?[0-9]*\.?[0-9]*[a-zA-Z]?)', expr)
            x_coeff = 0.0
            const = 0.0

            for t in term_matches:
                if not t:
                    continue
                if re.search(r'[a-zA-Z]', t):
                    var_str = re.sub(r'[a-zA-Z]', '', t)
                    if var_str == '' or var_str == '+':
                        coeff = 1.0
                    elif var_str == '-':
                        coeff = -1.0
                    else:
                        try:
                            coeff = float(var_str)
                        except ValueError:
                            continue
                    x_coeff += coeff
                else:
                    try:
                        const += float(t)
                    except ValueError:
                        continue
            return x_coeff, const

        try:
            lhs_x, lhs_c = extract_terms(lhs)
            rhs_x, rhs_c = extract_terms(rhs)

            net_x = lhs_x - rhs_x
            net_c = rhs_c - lhs_c

            if abs(net_x) < 1e-9:
                return None  # No unique solution or no variable

            sol = net_c / net_x
            return round(sol, 4)
        except Exception:
            return None

    @staticmethod
    def validate_rational_arithmetic(op: str, a: Tuple[int, int], b: Tuple[int, int], result: Tuple[int, int]) -> bool:
        """Verifies rational operations a/b (op) c/d == p/q."""
        try:
            if a[1] == 0 or b[1] == 0 or result[1] == 0:
                return False
            f_a = Fraction(a[0], a[1])
            f_b = Fraction(b[0], b[1])
            f_res = Fraction(result[0], result[1])

            if op in ("+", "add"):
                expected = f_a + f_b
            elif op in ("-", "sub", "subtract"):
                expected = f_a - f_b
            elif op in ("*", "×", "mul", "multiply"):
                expected = f_a * f_b
            elif op in ("/", "÷", "div", "divide"):
                if f_b == 0:
                    return False
                expected = f_a / f_b
            else:
                return False

            return expected == f_res
        except Exception:
            return False

    @staticmethod
    def validate_exponent_law(base: float, m: float, n: float, law: str) -> bool:
        """
        Verifies exponential laws:
        - 'product': a^m * a^n = a^(m+n)
        - 'quotient': a^m / a^n = a^(m-n)
        - 'power_of_power': (a^m)^n = a^(m*n)
        - 'negative_exponent': a^(-n) = 1 / (a^n)
        """
        try:
            if base == 0 and (m <= 0 or n <= 0):
                return False
            if law == "product":
                lhs = (base ** m) * (base ** n)
                rhs = base ** (m + n)
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            elif law == "quotient":
                lhs = (base ** m) / (base ** n)
                rhs = base ** (m - n)
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            elif law == "power_of_power":
                lhs = (base ** m) ** n
                rhs = base ** (m * n)
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            elif law == "negative_exponent":
                lhs = base ** (-n)
                rhs = 1.0 / (base ** n)
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            return False
        except Exception:
            return False

    @staticmethod
    def validate_square_and_root(x: float, root: float) -> bool:
        """Verifies root * root == x for non-negative x."""
        try:
            if x < 0:
                return False
            return math.isclose(root * root, x, rel_tol=1e-5)
        except Exception:
            return False

    @staticmethod
    def validate_cube_and_root(x: float, root: float) -> bool:
        """Verifies root^3 == x."""
        try:
            return math.isclose(root * root * root, x, rel_tol=1e-5)
        except Exception:
            return False

    @staticmethod
    def validate_polygon_angle_sum(sides: int, total_degrees: float) -> bool:
        """Verifies polygon interior angle sum S = (n - 2) * 180 degrees."""
        if sides < 3:
            return False
        expected = (sides - 2) * 180.0
        return math.isclose(expected, total_degrees, rel_tol=1e-5)

    @staticmethod
    def validate_percentage_commercial(base: float, rate_pct: float, mode: str, result: float) -> bool:
        """
        Verifies percentage calculations:
        - discount: base * (1 - r/100)
        - profit: base * (1 + r/100)
        - loss: base * (1 - r/100)
        - tax/gst: base * (1 + r/100)
        - percentage_of: base * (r/100)
        """
        try:
            mode_lower = mode.lower()
            if mode_lower in ("discount", "loss"):
                expected = base * (1.0 - rate_pct / 100.0)
            elif mode_lower in ("profit", "tax", "gst", "markup"):
                expected = base * (1.0 + rate_pct / 100.0)
            elif mode_lower in ("percentage_of", "part"):
                expected = base * (rate_pct / 100.0)
            else:
                return False
            return math.isclose(expected, result, rel_tol=1e-4)
        except Exception:
            return False

    @staticmethod
    def validate_mensuration(shape: str, dims: Dict[str, float], metric: str, val: float) -> bool:
        """
        Verifies perimeter, area, and volume for NCERT mensuration shapes:
        - trapezium: area = 0.5 * (a + b) * h
        - cuboid: volume = l * b * h, surface_area = 2*(lb + bh + hl)
        - cylinder: volume = pi * r^2 * h, csa = 2 * pi * r * h
        - circle: area = pi * r^2, circumference = 2 * pi * r
        """
        try:
            shape_l = shape.lower()
            metric_l = metric.lower()
            pi = math.pi
            if shape_l == "trapezium" and metric_l == "area":
                exp = 0.5 * (dims["a"] + dims["b"]) * dims["h"]
            elif shape_l == "cuboid" and metric_l == "volume":
                exp = dims["l"] * dims["b"] * dims["h"]
            elif shape_l == "cuboid" and metric_l in ("surface_area", "tsa"):
                exp = 2.0 * (dims["l"] * dims["b"] + dims["b"] * dims["h"] + dims["h"] * dims["l"])
            elif shape_l == "cylinder" and metric_l == "volume":
                exp = pi * (dims["r"] ** 2) * dims["h"]
            elif shape_l == "cylinder" and metric_l in ("curved_surface_area", "csa"):
                exp = 2.0 * pi * dims["r"] * dims["h"]
            elif shape_l == "circle" and metric_l == "area":
                exp = pi * (dims["r"] ** 2)
            elif shape_l == "circle" and metric_l in ("circumference", "perimeter"):
                exp = 2.0 * pi * dims["r"]
            else:
                return False
            return math.isclose(exp, val, rel_tol=1e-3)
        except Exception:
            return False

    @staticmethod
    def validate_proportion(x1: float, y1: float, x2: float, y2: float, prop_type: str = "direct") -> bool:
        """
        Verifies proportion relations:
        - direct: x1/y1 = x2/y2 (x1*y2 = x2*y1)
        - inverse: x1*y1 = x2*y2
        """
        try:
            if prop_type.lower() == "direct":
                return math.isclose(x1 * y2, x2 * y1, rel_tol=1e-5)
            elif prop_type.lower() == "inverse":
                return math.isclose(x1 * y1, x2 * y2, rel_tol=1e-5)
            return False
        except Exception:
            return False

    @staticmethod
    def validate_algebraic_identity(identity_name: str, a: float, b: float) -> bool:
        """
        Verifies standard NCERT Class 8 identities:
        - identity_1: (a+b)^2 = a^2 + 2ab + b^2
        - identity_2: (a-b)^2 = a^2 - 2ab + b^2
        - identity_3: (a+b)(a-b) = a^2 - b^2
        """
        try:
            if identity_name == "identity_1":
                lhs = (a + b) ** 2
                rhs = a ** 2 + 2.0 * a * b + b ** 2
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            elif identity_name == "identity_2":
                lhs = (a - b) ** 2
                rhs = a ** 2 - 2.0 * a * b + b ** 2
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            elif identity_name == "identity_3":
                lhs = (a + b) * (a - b)
                rhs = a ** 2 - b ** 2
                return math.isclose(lhs, rhs, rel_tol=1e-5)
            return False
        except Exception:
            return False

    @classmethod
    def validate_step_consistency(cls, text: str) -> Dict[str, Any]:
        """
        Extracts equation and arithmetic lines from text and verifies that:
        1. All consecutive linear equations solve to the same root x*.
        2. Explicit arithmetic assertions (e.g. 10 - 2 = 8) are accurate.
        """
        lines = text.split("\n")
        detected_equations = []

        # 1. Check basic arithmetic claims (e.g. "15 - 5 = 10" or "4 * 5 = 20")
        arith_pattern = re.compile(r'^\s*([+-]?\d+(?:\.\d+)?)\s*([+\-*/×÷−])\s*([+-]?\d+(?:\.\d+)?)\s*=\s*([+-]?\d+(?:\.\d+)?)\s*$')

        for line in lines:
            line_clean = line.strip().replace("−", "-").replace("×", "*").replace("÷", "/")
            if len(line_clean) > 90:
                continue

            # Strip markdown bullets or numbers like "1. ", "- "
            clean_expr = re.sub(r'^[0-9]+[\.\)]\s*|^\s*[-*•]\s*', '', line_clean).strip()

            # Check explicit simple arithmetic equality
            match = arith_pattern.match(clean_expr)
            if match:
                n1 = float(match.group(1))
                op = match.group(2)
                n2 = float(match.group(3))
                stated_res = float(match.group(4))

                if op == "+":
                    expected = n1 + n2
                elif op == "-":
                    expected = n1 - n2
                elif op == "*":
                    expected = n1 * n2
                elif op == "/":
                    if abs(n2) < 1e-9:
                        continue
                    expected = n1 / n2
                else:
                    continue

                if abs(stated_res - expected) > 1e-3:
                    logger.warning(f"Arithmetic validation failure in step '{line}': {n1} {op} {n2} != {stated_res}")
                    return {
                        "valid": False,
                        "verified_steps": len(detected_equations),
                        "failed_line": line_clean,
                        "reason": f"Arithmetic contradiction: '{line_clean}' asserts {n1} {op} {n2} = {stated_res}, but calculated value is {expected}."
                    }

            # Check linear equations containing variables
            if "=" in line_clean and re.search(r'[a-zA-Z]', line_clean):
                eq_match = re.search(r'([+-]?\s*\d*[a-zA-Z]?\s*[+-]?\s*\d*\s*=\s*[+-]?\s*\d*[a-zA-Z]?\s*[+-]?\s*\d*)', line_clean)
                if eq_match:
                    eq_text = eq_match.group(1).strip()
                    sol = cls.parse_linear_equation(eq_text)
                    if sol is not None:
                        detected_equations.append((eq_text, sol))

        if len(detected_equations) < 2:
            return {
                "valid": True,
                "verified_steps": len(detected_equations),
                "reason": "Single equation or conceptual narrative without step contradiction."
            }

        # Check that all detected linear equation steps share the same root
        reference_sol = detected_equations[0][1]
        for eq_text, sol in detected_equations[1:]:
            if abs(sol - reference_sol) > 1e-3:
                logger.warning(
                    f"Mathematical validation failed: '{detected_equations[0][0]}' (x={reference_sol}) contradicts "
                    f"'{eq_text}' (x={sol})"
                )
                return {
                    "valid": False,
                    "verified_steps": len(detected_equations),
                    "failed_equation": eq_text,
                    "expected_root": reference_sol,
                    "actual_root": sol,
                    "reason": f"Algebraic transformation error: step '{eq_text}' has solution {sol}, conflicting with initial root {reference_sol}."
                }

        return {
            "valid": True,
            "verified_steps": len(detected_equations),
            "common_root": reference_sol,
            "reason": f"All {len(detected_equations)} algebraic steps consistently solve to x = {reference_sol}."
        }
