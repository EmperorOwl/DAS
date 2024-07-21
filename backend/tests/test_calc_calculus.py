import unittest
from typing import Callable

from backend import calculator


class TestCalculus(unittest.TestCase):
    """ Contains unit tests to check `derive`, `integrate` and `limit`. """

    def run_subtests(self, in_: list[tuple], out: list[str], f: Callable):
        """ [Helper] Runs a subtest for each pair input and output
        checking the correctness of the function f.
        """
        for args, res in zip(in_, out):
            expr, var, *args = args
            with self.subTest(expr=expr, res=res):
                self.assertEqual(f(expr, var, *args)[0], res)

    def test00(self):
        """ derive """
        inputs = [
            ('2x', 'x'),
            ('x^2', 'x'),
        ]
        outputs = [
            "2",
            "2x"
        ]
        self.run_subtests(inputs, outputs, f=calculator.derive)

    def test01(self):
        """ integrate indefinite """
        inputs = [
            ('2', 'x'),
            ('2x', 'x'),
            ('cos(x)', 'x'),
            ('tan(x)', 'x'),
            ('1/x', 'x'),
            ('e^x', 'x')
        ]
        outputs = [
            '2x',
            'x^2',
            'sin(x)',
            '-log(cos(x))',
            'log(x)',
            'e^x'
        ]
        self.run_subtests(inputs, outputs, f=calculator.integrate_indefinite)

    def test02(self):
        """ integrate definite """
        inputs = [
            ('2x', 'x', '1', '5'),
        ]
        outputs = [
            '24'
        ]
        self.run_subtests(inputs, outputs, f=calculator.integrate_definite)

    def test03(self):
        """ limit """
        inputs = [
            ('x^2', 'x', '1'),
            ('1/x', 'x', '0'),
            ('2x', 'x', '1+pi')
        ]
        outputs = [
            '1',
            'oo',
            '2+2π'
        ]
        self.run_subtests(inputs, outputs, f=calculator.limit)
