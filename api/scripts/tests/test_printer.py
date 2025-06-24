import unittest
from typing import Callable

from scripts.parser import parse_expr
from scripts.printer import make_pretty


class TestAlgebra(unittest.TestCase):

    def test_printer(self):
        tests = [
            ("1 + 1", "1+1"),
            ("2 * 3", "2*3"),
            ("6 / 2", "6/2"),
            ("2^3", "2^3"),
            ("-1-2", "-2-1"),  # Weird
            ("2 + 1", "1+2"),  # Weird
            ("5 - 8", "5-8"),
            ("-2 - 2", "-2-2"),
            ("-2 * 2", "-2*2"),
            ("-2 / 2", "-2/2"),
            ("-4 + 1.25", "-4+1.25"),

            # Strip the multplication sign
            ("x*y", "xy"),
            ("x*y*z", "xyz"),
            ("a*b*c*d", "abcd"),
            ("2*x", "2x"),
            ("3*x*y", "3xy"),
            ("2*x*y*z", "2xyz"),
            ("1.5*x", "1.5x"),
            ("2*(x+1)", "2(x+1)"),
            ("2*(a+b)", "2(a+b)"),
            ("(x+1)*(x+2)", "(x+1)(x+2)"),
            ("x*cos(x)", "xcos(x)"),
            ("(x+1)^2*y", "y(x+1)^2"),  # Weird
            ("(a+b)*(c+d)*(e+f)", "(a+b)(c+d)(f+e)"),  # Weird

            # Don't strip the multplication sign
            ("(x+1)*2", "(x+1)*2"),
            ("x*2", "x*2"),
            ("x*y*z*2", "xyz*2"),
            ("9*8", "9*8"),
            ("4*3*2*1", "4*3*2*1"),

            # Mix of strip and don't strip
            ("x*2*y", "x*2y"),
            ("x^3*y^2", "x^3y^2"),
            ("x*2*y*3*z", "x*2y*3z"),
            ("2*x^3*y^2", "2x^3y^2"),
            ("x^3*2*y^2", "x^3*2y^2"),

            # Replace ** with ^
            ("x**2", "x^2"),
            ("x**y", "x^y"),
            ("2**3", "2^3"),
            ("(x+1)**2", "(x+1)^2"),

            # Replace E with e
            ("E", "e"),
            ("x*E", "ex"),
            ("E*x", "ex"),

            # Replace I with i
            ("I", "i"),
            ("x*I", "ix"),
            ("I*x", "ix"),

            # Replace pi with π
            ("pi", "π"),
            ("x*pi", "πx"),
            ("pi*x", "πx"),
            ("2*pi", "2π"),

            # Replace -1* with -
            ("-1*x", "-x"),
            ("-1*y", "-y"),
            ("-1*(x+1)", "-(x+1)"),
            ("x*-1*y", "x*-y"),
            ("-2*x", "-2x"),
            ("-3*y", "-3y"),
        ]
        for i, (expr, expected) in enumerate(tests, 1):
            with self.subTest(f"Test {i}: {expr} = {expected}"):
                res = make_pretty(parse_expr(expr))
                self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
