import unittest
from typing import Callable

from scripts.solvers import solve_equation, solve_linear_system


class TestSolvers(unittest.TestCase):

    def run_subtests(self,
                     f: Callable,
                     tests: list[tuple[tuple, list[str]]],
                     arg_names: list[str]) -> None:
        for arg_vals, expected in tests:
            args = {name: val for name, val in zip(arg_names, arg_vals)}
            with self.subTest(args):
                res = f(args)
                self.assertIsInstance(res.answer, list)
                self.assertEqual(expected, res.answer)

    def test_solve(self):
        arg_names = ["eq", "var", "dom"]
        tests = [
            # Linear equations
            (("x = 0", "x", "real"), ["0"]),
            (("2*x - 6 = 0", "x", "real"), ["3"]),
            (("3*x + 9 = 0", "x", "real"), ["-3"]),
            (("x - 5 = 0", "x", "real"), ["5"]),
            (("2*x = 10", "x", "real"), ["5"]),

            # Quadratic equations
            (("x^2 = 0", "x", "real"), ["0"]),
            (("x^2 = 9", "x", "real"), ["-3", "3"]),
            (("x^2 - 4 = 0", "x", "real"), ["-2", "2"]),
            (("x^2 - 9 = 0", "x", "real"), ["-3", "3"]),
            (("x^2 - 1 = 0", "x", "real"), ["-1", "1"]),
            (("x^2 + 1 = 0", "x", "real"), ["∅"]),

            # Complex solutions
            (("x^2 + 1 = 0", "x", "complex"), ["i", "-i"]),
            (("x^2 + 4 = 0", "x", "complex"), ["-2i", "2i"]),
            (('z(3i+2)=7-5i', 'z', 'complex'), ["-(5i-7)/(3i+2)"]),
            (('z^3=1', 'z', 'complex'), ["1",
                                         "-1/2-sqrt(3)i/2",
                                         "-1/2+sqrt(3)i/2"]),

            # All real numbers solutions
            (("0 = 0", "x", "real"), ["Reals"]),
            (("x = x", "x", "real"), ["Reals"]),
            (("1 = 1", "x", "real"), ["Reals"]),
            (('x^2+1 > 0', 'x', 'real'), ["Reals"]),

            # All complex numbers solutions
            (("0 = 0", "x", "complex"), ["Complexes"]),
            (("x = x", "x", "complex"), ["Complexes"]),
            (("1 = 1", "x", "complex"), ["Complexes"]),

            # Inequalities (intervals)
            (("x^2 <= 4", "x", "real"), ["[-2,2]"]),
            (("x^2 < 4", "x", "real"), ["(-2,2)"]),
            (("x^2 >= 1", "x", "real"), ["(-oo,-1]", "[1,oo)"]),
            (("x^2 > 1", "x", "real"), ["(-oo,-1)", "(1,oo)"]),
            (("x != 1", "x", "real"), ["(-oo,1)", "(1,oo)"]),

            # Trigonometric equations
            (("sin(x) = 1", "x", "real"), ["2nπ+π/2"]),
            (("cos(x) = 1", "x", "real"), ["2nπ"]),
            (("tan(x) = 1", "x", "real"), ["nπ+π/4"]),
            (("sin(x) = 0", "x", "real"), ['2nπ', '2nπ+π']),
            (("cos(x) = 0", "x", "real"), ['2nπ+π/2', '2nπ+3π/2']),
            (("tan(x) = 0", "x", "real"), ["nπ"]),

            # Complex trigonometric equations
            (('sin(2x)+cos(x)=0', 'x', 'real'), ["2nπ+π/2",
                                                 "2nπ+3π/2",
                                                 "2nπ+7π/6",
                                                 "2nπ+11π/6"]),
            (('sin(x)cos(x)=1/4', 'x', 'real'), ["nπ+5π/12", "nπ+π/12"]),
            # (('sin(cos(x)) = 0', 'x', 'real'), ["x"]),

            # Different variables
            (("y^2 - 4 = 0", "y", "real"), ["-2", "2"]),
            (("z^2 - 9 = 0", "z", "real"), ["-3", "3"]),

            # Higher degree polynomials
            (("x^3 - 8 = 0", "x", "real"), ["2"]),
            (("x^3 + 8 = 0", "x", "real"), ["-2"]),
            (("x^4 - 16 = 0", "x", "real"), ["-2", "2"]),

            # Exponential and logarithmic
            (("e^x = 1", "x", "real"), ["0"]),
            (("ln(x) = 0", "x", "real"), ["1"]),
            (("2^x = 8", "x", "real"), ["3"]),
            (('-7e^x+3e^(2x)+2=0', 'x', 'real'), ["log(2)", "-log(3)"]),

            # Absolute value
            (("abs(x) = 3", "x", "real"), ["-3", "3"]),
            (("abs(x) <= 2", "x", "real"), ["[-2,2]"]),
            (("abs(x) > 1", "x", "real"), ["(-oo,-1)", "(1,oo)"]),

            # Rational equations
            (("1/x = 1", "x", "real"), ["1"]),
            (("1/x = 0", "x", "real"), ["∅"]),

            # Radical equations
            (("sqrt(x) = 2", "x", "real"), ["4"]),
            (("sqrt(x^2) = 3", "x", "real"), ["-3", "3"]),

            # Intersection
            (('x=a', 'x', 'real'), ["Reals", "{a}"]),

            # No solution cases
            (("x^2 + 1 = 0", "x", "real"), ["∅"]),
            (("1 = 0", "x", "real"), ["∅"]),
            (("x = x + 1", "x", "real"), ["∅"]),
            (('x^2+1<0', 'x', 'real'), ["∅"]),
            (("1 = 0", "x", "real"), ["∅"]),
            (("1 = 0", "x", "complex"), ["∅"]),
        ]
        self.run_subtests(solve_equation, tests, arg_names)

    def test_linsolve(self):
        arg_names = ["eqs", "vars"]
        tests = [
            # Simple 2x2 systems
            ((["x + y = 3", "x - y = 1"], ["x", "y"]), ["2", "1"]),
            ((["2*x + y = 5", "x - y = 1"], ["x", "y"]), ["2", "1"]),
            ((["x + 2*y = 4", "2*x + y = 5"], ["x", "y"]), ["2", "1"]),

            # 3x3 systems
            ((["x+y+z=6", "x-y+z=2", "x+y-z=0"], ["x", "y", "z"]),
                ["1", "2", "3"]),
            ((["x+y+z=1", "2*x+y+z=2", "x+2*y+z=3"], ["x", "y", "z"]),
                ["1", "2", "-2"]),

            # Systems with no solution
            ((["x + y = 1", "x + y = 2"], ["x", "y"]), ["∅"]),
            ((["x + y = 1", "2*x + 2*y = 3"], ["x", "y"]), ["∅"]),

            # Systems with infinite solutions
            ((["x + y = 1", "2*x + 2*y = 2"], ["x", "y"]), ["1-y", "y"]),
            ((["x + y = 1", "3*x + 3*y = 3"], ["x", "y"]), ["1-y", "y"]),

            # Systems with fractions
            ((["x/2 + y/2 = 1", "x - y = 0"], ["x", "y"]), ["1", "1"]),
        ]
        self.run_subtests(solve_linear_system, tests, arg_names)


if __name__ == '__main__':
    unittest.main()
