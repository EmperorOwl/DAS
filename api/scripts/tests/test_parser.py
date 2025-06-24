import unittest
from typing import Callable

from scripts.parser import (ParsingError,
                            _parse,
                            parse_expr,
                            parse_var,
                            parse_eq,
                            parse_rel,
                            parse_func,
                            parse_lim,
                            parse_dom)


class TestParser(unittest.TestCase):

    def run_subtests(self, f: Callable, tests: list[tuple[str, str]]) -> None:
        for expr, expected in tests:
            with self.subTest(expr):
                res = f(expr)
                self.assertEqual(expected, str(res))

    def run_invalid_subtests(self, f: Callable, tests: list[str]) -> None:
        for expr in tests:
            with self.subTest(expr):
                with self.assertRaises(ParsingError):
                    f(expr)

    def test_parse(self):
        valid = [
            # No evaluate
            ("1 + 1", "1 + 1"),
            ("2 * 3", "2*3"),
            ("6 / 2", "6/2"),
            ("2^3", "2**3"),
            ("5 - 3", "5 - 1*3"),

            # Conversions
            ("e", "E"),
            ("π", "pi"),
            ("arcsin(x)", "asin(x)"),
            ("arccos(x)", "acos(x)"),
            ("arctan(x)", "atan(x)"),
            ("cosec(x)", "csc(x)"),
            ("arcsinh(x)", "asinh(x)"),
            ("arccosh(x)", "acosh(x)"),
            ("arctanh(x)", "atanh(x)"),

            # Replacements
            ("x⋅y", "x*y"),
            ("x×y", "x*y"),
            ("x÷y", "x/y"),
            ("x–y", "x - y"),
            ("sin(90°)", "sin(90*pi/180)"),
            ("cos(180deg)", "cos(180*pi/180)"),
            ("x⋅y÷z–w", "-w + x*y/z"),

            # Implicit multiplication / split symbols
            ("2x", "2*x"),
            ("xyz", "x*y*z"),
            ("theta", "theta"),

            # Implicit application
            ("sin 1", "sin(1)"),
            ("sin 2x", "sin(2*x)"),

            # Function exponentation
            ("sin^2(x)", "sin(x)**2"),
            ("cos**2(x)", "cos(x)**2"),

            # Convert XOR
            ("x ^ y", "x**y"),
            ("2^3", "2**3"),
        ]
        invalid = [
            "__import__('os')",
            "config",
            "eval('1+1')",
            "echo hello",
            "!!!",
            "$",
            "|x|",  # Should use abs(x)
            "{x}",  # Should use (x)
        ]
        self.run_subtests(_parse, valid)
        self.run_invalid_subtests(_parse, invalid)

    def test_parse_expr(self):
        valid = [
            ("1 + 1", "1 + 1"),
            ("2 * 3", "2*3"),
            ("6 / 2", "6/2"),
            ("2^3", "2**3"),
            ("5 - 3", "5 - 1*3"),
        ]
        invalid = [
            "1 = 1",
            "f(x) = x+2"
            "x+4 > 2"
        ]
        self.run_subtests(parse_expr, valid)
        self.run_invalid_subtests(parse_expr, invalid)

    def test_parse_var(self):
        valid = [
            ("x", "x"),
            ("y", "y"),
            ("z", "z"),
        ]
        invalid = [
            "i",
            "pi",
            "deg",
            "e",
            "1",
            "123",
        ]
        self.run_subtests(parse_var, valid)
        self.run_invalid_subtests(parse_var, invalid)

    def test_parse_eq(self):
        valid = [
            ("x = 1", "Eq(x, 1)"),
            ("x + y = 2", "Eq(x + y, 2)"),
            ("x^2 + y^2 = 1", "Eq(x**2 + y**2, 1)"),
        ]
        invalid = [
            "x + 1",
            "sin(x)",
            "1 + 2",
        ]
        self.run_subtests(parse_eq, valid)
        self.run_invalid_subtests(parse_eq, invalid)

    def test_parse_rel(self):
        valid = [
            ("x > 1", "x > 1"),
            ("x < 2", "x < 2"),
            ("x >= 3", "x >= 3"),
            ("x <= 4", "x <= 4"),
        ]
        invalid = [
            "z = 1",
            "a + b = 2",
            "1 = 1",
            "1 + 1",
        ]
        self.run_subtests(parse_rel, valid)
        self.run_invalid_subtests(parse_rel, invalid)

    def test_parse_func(self):
        valid = [
            (("f(x) = x + 1", "x"), "Func(name='f', var=x, expr=x + 1)"),
            (("f(x)=x+1", "x"), "Func(name='f', var=x, expr=x + 1)"),
            (("g(y) = y^2", "y"), "Func(name='g', var=y, expr=y**2)"),
            (("h(x) = sin(x)", "x"), "Func(name='h', var=x, expr=sin(x))"),
            (("abc(x) = x + 1", "x"), "Func(name='abc', var=x, expr=x + 1)"),
        ]
        invalid = [
            ("f(y) = x + 1", "x"),
            ("g(z) = y^2", "y"),
            ("f(x) = f(y) = x + 1", "x"),
        ]
        for (func_str, var_str), expected in valid:
            with self.subTest(f"{func_str} with var {var_str}"):
                res = parse_func(func_str, var_str)
                self.assertEqual(expected, str(res))
        for (func_str, var_str) in invalid:
            with self.subTest(f"{func_str} with var {var_str}"):
                with self.assertRaises(ParsingError):
                    parse_func(func_str, var_str)

    def test_parse_lim(self):
        valid = [
            ("0,1", "Limit(lower=0, upper=1)"),
            ("[0,1]", "Limit(lower=0, upper=1)"),
            ("(0,1)", "Limit(lower=0, upper=1)"),
            ("[0,1)", "Limit(lower=0, upper=1)"),
            ("(0,1]", "Limit(lower=0, upper=1)"),
            (" (0,     1)  ", "Limit(lower=0, upper=1)"),
            ("-5,5", "Limit(lower=-5, upper=5)"),
            ("0,pi", "Limit(lower=0, upper=pi)"),
            ("-pi, pi", "Limit(lower=-pi, upper=pi)"),
            ("-pi-4, 2pi", "Limit(lower=-1*4 - pi, upper=2*pi)"),
        ]
        invalid = [
            "0",
            "0 1",
            "1,0",
            "-5,-10",
        ]
        self.run_subtests(parse_lim, valid)
        self.run_invalid_subtests(parse_lim, invalid)

    def test_parse_dom(self):
        valid = [
            ("real", "Reals"),
            ("Real", "Reals"),
            ("complex", "Complexes"),
            ("Complex", "Complexes")
        ]
        invalid = [
            "reals",
            "complexs",
            "realz",
            "complexz",
        ]
        self.run_subtests(parse_dom, valid)
        self.run_invalid_subtests(parse_dom, invalid)


if __name__ == '__main__':
    unittest.main()
