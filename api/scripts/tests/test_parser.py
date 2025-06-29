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
from scripts.utils.error_messages import (invalid_character,
                                          invalid_input,
                                          no_latex,
                                          invalid_factorial,
                                          invalid_syntax,
                                          missing_closing_bracket,
                                          only_one_argument,
                                          invalid_log,
                                          invalid_root,
                                          invalid_mod)


class TestParser(unittest.TestCase):

    def run_subtests(self, f: Callable, tests: list[tuple[str, str]]) -> None:
        for expr, expected in tests:
            with self.subTest(expr):
                res = f(expr)
                self.assertEqual(expected, str(res))

    def run_invalid_subtests(self,
                             f: Callable,
                             tests: list[tuple[str, str]]) -> None:
        for expr, expected_error_message in tests:
            with self.subTest(expr):
                with self.assertRaises(ParsingError) as cm:
                    f(expr)
                self.assertEqual(expected_error_message, str(cm.exception))

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
            ("1 billion", "1*10**9"),

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
            # Invalid character
            ("2_2", invalid_character("_")),
            ("'hello' + 1", invalid_character("'")),
            ("$x^2$", invalid_character("$")),

            # Invalid input
            ("import", invalid_input("import")),
            ("config", invalid_input("config")),
            ("echo hello", invalid_input("echo hello")),

            # No latex
            ("\\sqrt{2} + 1", no_latex()),

            # Invalid factorial
            ("5!!!", invalid_factorial()),

            # Invalid syntax
            ("|x|", invalid_syntax("abs(x)", "|x|")),
            ("2{x+1}", invalid_syntax("()", "{}")),
            ("2³", invalid_syntax("^3", "³")),
            ("2 squared", invalid_syntax("^2", "squared")),
            ("2 cubed", invalid_syntax("^3", "cubed")),
            ("√4", invalid_syntax("sqrt(x) or root(x, 2)", "√x")),
            ("square root 4", invalid_syntax("sqrt(x) or root(x, 2)",
                                             "square root x")),

            # Brackets
            ("2{x+1}", invalid_syntax("()", "{}")),
            ("2[x+1]", invalid_syntax("()", "[]")),

            # Missing closing bracket
            ("(2 + 3", missing_closing_bracket("(2 + 3")),
            ("sin(2x", missing_closing_bracket("sin(2x")),
            ("sqrt(16", missing_closing_bracket("sqrt(16")),
            ("root(8, 3", missing_closing_bracket("root(8, 3")),

            # Use * instead of . for multiplication
            ("sin(x).cos(x)", invalid_syntax("*", ".")),

            # Only one argument
            ("sqrt()", only_one_argument("sqrt")),
            ("sqrt(2, 3)", only_one_argument("sqrt")),
            ("abs()", only_one_argument("abs")),
            ("abs(-1, -2)", only_one_argument("abs")),
            ("sin()", only_one_argument("sin")),
            ("sin(1, 2)", only_one_argument("sin")),
            ("cos()", only_one_argument("cos")),
            ("cos(1, 2)", only_one_argument("cos")),
            ("tan()", only_one_argument("tan")),
            ("tan(1, 2)", only_one_argument("tan")),
            ("asin()", only_one_argument("asin")),
            ("asin(1, 2)", only_one_argument("asin")),
            ("sinh()", only_one_argument("sinh")),
            ("sinh(1, 2)", only_one_argument("sinh")),
            ("asinh()", only_one_argument("asinh")),
            ("asinh(1, 2)", only_one_argument("asinh")),
            ("exp()", only_one_argument("exp")),
            ("exp(1, 2)", only_one_argument("exp")),

            # Invalid log
            ("log()", invalid_log()),
            ("log(10, 2, 3)", invalid_log()),

            # Invalod root
            ("root()", invalid_root()),
            ("root(8)", invalid_root()),
            # ("root(8, 3, 4)", invalid_root()),  # Actually valid?

            # Invalid mod
            ("mod()", invalid_mod()),
            ("mod(5)", invalid_mod()),
            ("mod(5, 2, 3)", invalid_mod()),
            ("5 mod 2", invalid_mod()),

            # Combination of invalid to check return the correct one
            ("root(8, 3) * mod(5)", invalid_mod()),
            ("root(8) * mod(5, 2)", invalid_root()),
            ("sin() - mod(5, 2)", only_one_argument("sin")),

            # Syntax error
            ("1 +", invalid_input("1 +")),
            ("1 -", invalid_input("1 -")),
            ("1 *", invalid_input("1 *")),
            ("1 /", invalid_input("1 /")),
            ("1 ^", invalid_input("1 ^")),
            ("1 %", invalid_input("1 %")),
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
            ("1 = 1", "Do not use = in expressions"),
            ("f(x) = x+2", "Do not use = in expressions"),
            ("x+4 > 2", "x+4 > 2 is not an expression")
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
            ("i", "i is an invalid variable name"),
            ("pi", "pi is an invalid variable name"),
            ("deg", "deg is an invalid variable name"),
            ("e", "e is an invalid variable name"),
            ("1", "1 is an invalid variable name"),
            ("123", "123 is an invalid variable name"),
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
            ("x + 1", "x + 1 is not an equation"),
            ("sin(x)", "sin(x) is not an equation"),
            ("1 + 2", "1 + 2 is not an equation"),
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
            ("z = 1", "Relation must contain x or y or both"),
            ("a + b = 2", "Relation must contain x or y or both"),
            ("1 = 1", "Relation must contain x or y or both"),
            ("1 + 1", "Relation must contain x or y or both"),
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
            ("0", "0 is not a limit"),
            ("0 1", "0 1 is not a limit"),
            ("1,0", "Upper bound is smaller than lower bound"),
            ("-5,-10", "Upper bound is smaller than lower bound"),
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
            ("reals", "reals is not a valid domain"),
            ("complexs", "complexs is not a valid domain"),
            ("realz", "realz is not a valid domain"),
            ("complexz", "complexz is not a valid domain"),
        ]
        self.run_subtests(parse_dom, valid)
        self.run_invalid_subtests(parse_dom, invalid)


if __name__ == '__main__':
    unittest.main()
