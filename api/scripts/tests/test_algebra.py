import unittest
from typing import Callable

from scripts.algebra import (evaluate_expression,
                             expand_expression,
                             factor_expression,
                             simplify_expression)


class TestAlgebra(unittest.TestCase):

    def run_subtests(self, f: Callable, tests: list[tuple[str, str]]) -> None:
        for expr, expected in tests:
            with self.subTest(expr):
                res = f({"expr": expr})
                self.assertEqual(expected, res.answer)

    def test_evaluate(self):
        tests = [
            # Numeric
            ("2 + 2", "4"),
            ("5 - 3", "2"),
            ("2 * 3", "6"),
            ("6 / 2", "3"),
            ("2^3", "8"),
            ("5 % 2", "1"),

            # Negative
            ("-1-2", "-3"),
            ("5 - 8", "-3"),
            ("-2 - 2", "-4"),
            ("-2 * 2", "-4"),
            ("-2 / 2", "-1"),
            ("-2^3", "-8"),

            # Decimals
            ("2.5 + 1.25", "3.75"),
            ("2.5 - 0.2", "2.3"),
            ("2.5 * 2.5", "6.25"),
            ("2.5 / 5", "0.5"),
            ("2.5^3", "15.625"),

            # Trigonometric
            ("sin(0)", "0"),
            ("sin(pi/2)", "1"),
            ("sin(pi)", "0"),

            ("cos(0)", "1"),
            ("cos(pi/2)", "0"),
            ("cos(pi)", "-1"),

            ("tan(0)", "0"),
            ("tan(pi)", "0"),

            ("csc(pi/2)", "1"),
            ("sec(0)", "1"),
            ("cot(pi/4)", "1"),

            # Inverse Trigonometric
            ("asin(0)", "0"),
            ("acos(1)", "0"),
            ("atan(0)", "0"),

            # Hyperbolic
            ("sinh(0)", "0"),
            ("cosh(0)", "1"),
            ("tanh(0)", "0"),

            # Log
            ("log(100, 10)", "2"),
            ("ln(e)", "1"),

            # Combination
            ("sqrt(16) + 3^2", "13"),
            ("2 * (3 + 4)", "14"),
            ("sin(pi/2) + cos(0)", "2"),

            # Special characters
            ("sin(π)", "0"),
            ("e^0", "1"),

            # Decimal precision
            ("sqrt(2)", "1.4142135623730951"),

            # Already evaluated
            ("1", "1"),
            ("1.0", "1"),
            ("2.1", "2.1"),

            # Variable
            ("x + 1", "x+1.0"),
        ]
        self.run_subtests(evaluate_expression, tests)

    def test_expand(self):
        tests = [
            # Basic binomial expansion
            ("(x + y)^2", "x^2+2xy+y^2"),
            ("(x - y)^2", "x^2-2xy+y^2"),
            ("(x + y)^3", "x^3+3x^2y+3xy^2+y^3"),

            # Multiple terms
            ("(x + y + z)^2", "x^2+2xy+2xz+y^2+2yz+z^2"),

            # With coefficients
            ("(2*x + 3*y)^2", "4x^2+12xy+9y^2"),

            # Nested expressions
            ("(x + (y + z))^2", "x^2+2xy+2xz+y^2+2yz+z^2"),

            # Already expanded expressions
            ("x + y", "x+y"),
            ("2x+4", "2x+4"),

            # With negative terms
            ("(x - y)*(x + y)", "x^2-y^2"),

            # Multiple factors
            ("(x + 1)*(x + 2)*(x + 3)", "x^3+6x^2+11x+6"),
        ]
        self.run_subtests(expand_expression, tests)

    def test_factor(self):
        tests = [
            # Basic factoring
            ("x^2 - 1", "(x-1)(x+1)"),
            ("x^2 - 4", "(x-2)(x+2)"),
            ("x^2 - 9", "(x-3)(x+3)"),

            # Quadratic factoring
            ("x^2 + 5x + 6", "(x+2)(x+3)"),
            ("x^2 - 5x + 6", "(x-3)(x-2)"),
            ("x^2 + x - 6", "(x-2)(x+3)"),

            # Higher degree polynomials
            ("x^3 - 1", "(x-1)(x^2+x+1)"),
            ("x^3 + 1", "(x+1)(x^2-x+1)"),

            # With coefficients
            ("4x^2 - 9", "(2x-3)(2x+3)"),
            ("9x^2 - 16", "(3x-4)(3x+4)"),

            # Already factored expressions
            ("(x + 1)*(x - 1)", "(x-1)(x+1)"),

            # Multiple variables
            ("x^2 - y^2", "(x-y)(x+y)"),
            ("x^2 - 4y^2", "(x-2y)(x+2y)"),
        ]
        self.run_subtests(factor_expression, tests)

    def test_simplify(self):
        tests = [
            # Basic
            ("x + x", "2x"),
            ("x - x", "0"),
            ("x * x", "x^2"),
            ("x / x", "1"),

            # Fractions
            ("(x + 1)/(x + 1)", "1"),
            ("(x^2 - 1)/(x - 1)", "x+1"),
            ("(x^2 + 2x + 1)/(x + 1)", "x+1"),

            # Trigonometric
            ("sin(x) / cos(x)", "tan(x)"),
            ("sin(x) / tan(x)", "cos(x)"),
            ("tan(x) * cos(x)", "sin(x)"),

            ("sin(x)^2 + cos(x)^2", "1"),
            ("cos(x)^2 + sin(x)^2", "1"),

            ("1 + tan(x)^2", "cos(x)^(-2)"),  # sec(x)^2
            ("tan(x)^2 + 1", "cos(x)^(-2)"),  # sec(x)^2
            ("1 + cot(x)^2", "sin(x)^(-2)"),  # csc(x)^2
            ("cot(x)^2 + 1", "sin(x)^(-2)"),  # csc(x)^2

            ("sin(x)cos(y) + cos(x)sin(y)", "sin(x+y)"),
            ("sin(x)cos(y) - cos(x)sin(y)", "sin(x-y)"),
            ("cos(x)cos(y) - sin(x)sin(y)", "cos(x+y)"),
            ("cos(x)cos(y) + sin(x)sin(y)", "cos(x-y)"),

            ("2*sin(x)*cos(x)", "sin(2x)"),
            ("cos(x)^2 - sin(x)^2", "cos(2x)"),
            ("2*cos(x)^2 - 1", "cos(2x)"),
            ("1 - 2*sin(x)^2", "cos(2x)"),
            ("2*tan(x) / (1 - tan(x)^2)", "tan(2x)"),

            ("1/2 * (1 - cos(2x))", "sin(x)^2"),
            ("1/2 * (1 + cos(2x))", "cos(x)^2"),

            # Complex expressions
            ("(x + 1)^2 - (x^2 + 2x + 1)", "0"),
            ("(x + y)^2 - (x^2 + 2*x*y + y^2)", "0"),
            ("sin(x)^2 + cos(x)^2 - 1", "0"),

            # Already simplified
            ("1", "1"),
            ("x + y", "x+y"),
            ("2*x + 3", "2x+3"),

            ("sin(x)", "sin(x)"),
            ("cos(x)", "cos(x)"),
            ("tan(x)", "tan(x)"),
            ("sec(x)", "sec(x)"),
            ("csc(x)", "csc(x)"),
            ("cot(x)", "cot(x)"),

            ("sin(2*x)", "sin(2x)"),
            ("cos(2*x)", "cos(2x)"),
            ("tan(2*x)", "tan(2x)"),

            ("sec(x)^2", "sec(x)^2"),
            ("csc(x)^2", "csc(x)^2"),
            ("cot(x)^2", "cot(x)^2"),

            ("sin(x)^-2", "sin(x)^(-2)"),
            ("cos(x)^-2", "cos(x)^(-2)"),
            ("tan(x)^-2", "tan(x)^(-2)"),

            ("log(x) + log(y)", "log(x)+log(y)"),
            ("log(x) - log(y)", "log(x)-log(y)"),
            ("log(x^n)", "log(x^n)"),

            ("log(x*y)", "log(xy)"),
            ("log(x/y)", "log(x/y)"),
            ("n*log(x)", "nlog(x)"),
        ]
        self.run_subtests(simplify_expression, tests)


if __name__ == '__main__':
    unittest.main()
