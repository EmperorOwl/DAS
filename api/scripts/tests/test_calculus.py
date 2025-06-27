import unittest
from typing import Callable

from scripts.calculus import (derive_expression,
                              integrate_definite_expression,
                              integrate_indefinite_expression,
                              limit_expression)


class TestCalculus(unittest.TestCase):

    def run_subtests(self,
                     f: Callable,
                     tests: list[tuple[tuple, str]],
                     arg_names: list[str]) -> None:
        for arg_vals, expected in tests:
            args = {name: val for name, val in zip(arg_names, arg_vals)}
            with self.subTest(args):
                result = f(args)
                self.assertEqual(expected, result.answer)

    def test_derive(self):
        arg_names = ["expr", "vars"]
        tests = [
            # Basic derivatives
            (("x^2", ["x"]), "2x"),
            (("x^3", ["x"]), "3x^2"),
            (("x^n", ["x"]), "nx^n/x"),

            # Trigonometric
            (("sin(x)", ["x"]), "cos(x)"),
            (("cos(x)", ["x"]), "-sin(x)"),
            (("tan(x)", ["x"]), "tan(x)^2+1"),  # sec(x)^2
            (("sec(x)", ["x"]), "tan(x)sec(x)"),
            (("csc(x)", ["x"]), "-cot(x)csc(x)"),
            (("cot(x)", ["x"]), "-cot(x)^2-1"),

            # Exponential and logarithmic
            (("e^x", ["x"]), "exp(x)"),
            (("a^x", ["x"]), "a^xlog(a)"),
            (("log(x)", ["x"]), "1/x"),
            (("ln(x)", ["x"]), "1/x"),

            # Multiple variables
            (("x^2 + y^2", ["x"]), "2x"),
            (("x^2 + y^2", ["y"]), "2y"),
            (("x*y", ["x"]), "y"),
            (("x*y", ["y"]), "x"),

            # Chain rule
            (("sin(x^2)", ["x"]), "2xcos(x^2)"),
            (("e^(x^2)", ["x"]), "2xexp(x^2)"),
            (("log(sin(x))", ["x"]), "cos(x)/sin(x)"),

            # Product rule
            (("x*sin(x)", ["x"]), "xcos(x)+sin(x)"),
            (("x*e^x", ["x"]), "xexp(x)+exp(x)"),

            # Quotient rule
            (("sin(x)/x", ["x"]), "cos(x)/x-sin(x)/x^2"),
            (("x/log(x)", ["x"]), "1/log(x)-1/log(x)^2"),

            # Higher order derivatives
            (("x^2 + y^2", ["x", "y"]), "0"),
            (("x^2 + y^2", ["y", "x"]), "0"),
            (("x^3*y^2", ["x", "y"]), "6x^2y"),
            (("x^3*y^2", ["y", "x"]), "6x^2y"),
            (("x^2*y^3", ["x", "x"]), "2y^3"),
            (("x^2*y^3", ["y", "y"]), "6x^2y"),
            (("sin(x*y)", ["x", "y"]), "-xysin(xy)+cos(xy)"),
            (("e^(x*y)", ["x", "y"]), "(xy+1)exp(xy)"),

            # Second variable missing
            (("x^2 + y^2", ["x"]), "2x"),
            (("x^2 + y^2", ["y"]), "2y"),

            # Three variable derivatives
            (("x^2*y*z", ["x", "y", "z"]), "2x"),
            (("x*y^2*z^3", ["x", "y", "z"]), "6yz^2"),
            (("sin(x*y*z)", ["x", "y", "z"]),
             "-x^2y^2z^2cos(xyz)-3xyzsin(xyz)+cos(xyz)"),
            (("e^(x*y*z)", ["x", "y", "z"]), "(x^2y^2z^2+3xyz+1)exp(xyz)"),

            # Second derivative
            (("x^2", ["x", "x"]), "2"),
            (("x^3*y^2*z", ["x", "x", "y"]), "12xyz"),
            (("x*y*z^2", ["z", "z", "x"]), "2y"),
        ]
        self.run_subtests(derive_expression, tests, arg_names)

    def test_integrate_definite(self):
        arg_names = ["expr", "var", "lt", "ut"]
        tests = [
            # Basic integrals
            (("x", "x", "0", "1"), "1/2"),
            (("x^2", "x", "0", "1"), "1/3"),
            (("x^3", "x", "0", "1"), "1/4"),

            # Trigonometric
            (("sin(x)", "x", "0", "pi"), "2"),
            (("cos(x)", "x", "0", "pi"), "0"),
            (("sin(x)^2", "x", "0", "pi"), "π/2"),
            (("cos(x)^2", "x", "0", "pi"), "π/2"),

            # Exponential
            (("e^x", "x", "0", "1"), "-1+e"),
            (("e^(-x)", "x", "0", "1"), "1-exp(-1)"),

            # Logarithmic
            (("log(x)", "x", "1", "E"), "1"),
            (("1/x", "x", "1", "E"), "1"),

            # Multiple variables
            (("x*y", "x", "0", "1"), "y/2"),
            (("x^2 + y^2", "x", "0", "1"), "y^2+1/3"),

            # Definite integrals with constants
            (("2*x", "x", "0", "1"), "1"),
            (("3*x^2", "x", "0", "1"), "1"),

            # Definite integrals with negative bounds
            (("x", "x", "-1", "1"), "0"),
            (("x^2", "x", "-1", "1"), "2/3"),

            # Definite integrals with infinite bounds
            (("e^(-x)", "x", "0", "oo"), "1"),
            (("1/(1 + x^2)", "x", "-oo", "oo"), "π"),
        ]
        self.run_subtests(integrate_definite_expression, tests, arg_names)

    def test_integrate_indefinite(self):
        arg_names = ["expr", "var"]
        tests = [
            # Basic integrals
            (("1", "x"), "x"),
            (("x", "x"), "x^2/2"),
            (("x^2", "x"), "x^3/3"),
            (("x^3", "x"), "x^4/4"),

            # Trigonometric
            (("sin(x)", "x"), "-cos(x)"),
            (("cos(x)", "x"), "sin(x)"),
            (("sec(x)^2", "x"), "sin(x)/cos(x)"),
            (("csc(x)^2", "x"), "-cos(x)/sin(x)"),

            # Exponential
            (("e^x", "x"), "e^x"),
            (("e^(-x)", "x"), "-exp(-x)"),
            # (("a^x", "x"), "a**x/log(a)"),

            # Logarithmic
            (("1/x", "x"), "log(x)"),
            (("log(x)", "x"), "xlog(x)-x"),

            # Multiple variables
            (("x*y", "x"), "x^2y/2"),
            (("x^2 + y^2", "x"), "x^3/3+xy^2"),

            # Constants
            (("2*x", "x"), "x^2"),
            (("3*x^2", "x"), "x^3"),

            # Chain rule
            (("sin(x^2)*2*x", "x"), "-cos(x^2)"),
            (("e^(x^2)*2*x", "x"), "e^(x^2)"),

            # Product rule
            (("x*sin(x)", "x"), "-xcos(x)+sin(x)"),
            (("x*e^x", "x"), "(x-1)exp(x)"),

            # Quotient rule
            (("sin(x)/x", "x"), "Si(x)"),  # Sine integral
            (("1/log(x)", "x"), "li(x)"),  # Logarithmic integral
        ]
        self.run_subtests(integrate_indefinite_expression, tests, arg_names)

    def test_limit(self):
        arg_names = ["expr", "var", "val"]
        tests = [
            # Basic limits
            (("x", "x", "0"), "0"),
            (("x^2", "x", "2"), "4"),
            (("x^3", "x", "3"), "27"),

            # Trigonometric
            (("sin(x)/x", "x", "0"), "1"),
            (("(1 - cos(x))/x", "x", "0"), "0"),
            (("tan(x)/x", "x", "0"), "1"),

            # Exponential
            (("(e^x - 1)/x", "x", "0"), "1"),
            (("(a^x - 1)/x", "x", "0"), "log(a)"),

            # Logarithmic
            (("log(1 + x)/x", "x", "0"), "1"),
            (("(log(x) - log(a))/(x - a)", "x", "a"), "1/a"),

            # Infinite limits
            (("1/x", "x", "oo"), "0"),
            (("1/x", "x", "-oo"), "0"),
            (("x", "x", "oo"), "oo"),
            (("x", "x", "-oo"), "-oo"),

            # Limits at infinity
            (("(x^2 + 1)/(x^2 - 1)", "x", "oo"), "1"),
            (("(x^3 + 1)/(x^3 - 1)", "x", "oo"), "1"),

            # Indeterminate forms
            (("(x^2 - 1)/(x - 1)", "x", "1"), "2"),
            (("(sin(x) - x)/x^3", "x", "0"), "-1/6"),

            # One-sided limits
            # (("1/x", "x", "0+"), "oo"),
            # (("1/x", "x", "0-"), "-oo"),

            # Multiple variables
            (("x*y", "x", "2"), "2y"),
            (("x^2 + y^2", "x", "1"), "y^2+1"),

            # Special limits
            (("(1 + 1/x)^x", "x", "oo"), "e"),
            (("(1 + x)^(1/x)", "x", "0"), "e"),
        ]
        self.run_subtests(limit_expression, tests, arg_names)


if __name__ == '__main__':
    unittest.main()
