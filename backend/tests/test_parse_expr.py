import unittest

from backend import parser


class TestParseExpr(unittest.TestCase):
    """ Contains unit tests to check the correctness of the expression
    parser.
    """

    def run_subtests(self, inputs: list[str], outputs: list[str]):
        """ [Helper] Runs a subtest for each pair input and output. """
        for s, res in zip(inputs, outputs):
            with self.subTest(s=s, res=res):
                self.assertEqual(str(parser.parse_expr(s)), res)

    def test00(self):
        """ implicit multiplication """
        inputs = [
            '2x',
            '3 x y'
        ]
        outputs = [
            '2*x',
            '3*x*y'
        ]
        self.run_subtests(inputs, outputs)

    def test01(self):
        """ XOR, ^, is treated as exponentiation, ** """
        inputs = [
            '2^3',
            '2^3^4'
        ]
        outputs = [
            '2**3',
            '2**(3**4)'
        ]
        self.run_subtests(inputs, outputs)

    def test02(self):
        """ expression is not evaluated """
        inputs = [
            '2**3',
            '1+1'
        ]
        outputs = [
            '2**3',
            '1 + 1'
        ]
        self.run_subtests(inputs, outputs)

    @unittest.skip("Not implemented yet")
    def test03(self):
        """ order is preserved """
        inputs = [
            '1+x',
            '2+3*4',
            '2*3+4'
        ]
        outputs = [
            '1 + x',
            '2 + 3*4',
            '2*3 + 4'
        ]
        self.run_subtests(inputs, outputs)

    def test10(self):
        """ conversions """
        inputs = [
            'e',
            'π',
            'arcsin(pi)',
            'arccos(pi)',
            'arctan(pi)',
            'cosec(pi)',
        ]
        outputs = [
            'E',
            'pi',
            'asin(pi)',
            'acos(pi)',
            'atan(pi)',
            'csc(pi)',
        ]
        self.run_subtests(inputs, outputs)

    def test11(self):
        """ replacements """
        inputs = [
            '2×3',
            '5÷3',
            '2–4'
        ]
        outputs = [
            '2*3',
            '5/3',
            '2 - 1*4'
        ]
        self.run_subtests(inputs, outputs)

    def test12(self):
        """ err: relational operators """
        inputs = [
            '2 = 3',
            '2 < 3',
            '2 > 3'
        ]
        for s in inputs:
            with self.subTest(s=s):
                with self.assertRaises(Exception):
                    parser.parse_expr(s)
