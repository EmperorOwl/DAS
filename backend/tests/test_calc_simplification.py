import unittest
from typing import Callable

from backend import calculator


class TestSimplification(unittest.TestCase):
    """ Contains unit tests to check `expand`, `factor`, `simplify` and
    `evaluate`.
    """

    def run_subtests(self, in_: list[str], out: list[str], f: Callable):
        """ [Helper] Runs a subtest for each pair input and output
        checking the correctness of the function f.
        """
        for expr, res in zip(in_, out):
            with self.subTest(expr=expr, res=res):
                self.assertEqual(f(expr)[0], res)

    def test00(self):
        """ expand """
        inputs = [
            '2(x+1)'
        ]
        outputs = [
            '2x+2'
        ]
        self.run_subtests(inputs, outputs, f=calculator.expand)

    def test01(self):
        """ factor """
        inputs = [
            '2x+2'
        ]
        outputs = [
            '2(x+1)'
        ]
        self.run_subtests(inputs, outputs, f=calculator.factor)

    def test02(self):
        """ simplify """
        inputs = [
            'cos(x)**2 + sin(x)**2'
        ]
        outputs = [
            '1'
        ]
        self.run_subtests(inputs, outputs, f=calculator.simplify)

    def test03(self):
        """ evaluate """
        inputs = [
            '1+1',
            'cos(pi)',
            'sin(90deg)',
            '5 % 2',
        ]
        outputs = [
            '2',
            '-1',
            '1',
            '1'
        ]
        outputs = [s + '.' + '0' * 14 for s in outputs]
        self.run_subtests(inputs, outputs, f=calculator.evaluate)

    def test04(self):
        """ evaluate - letters"""
        inputs = [
            'x',
            'a*b*c',
            'a+b'
        ]
        outputs = [
            'x',
            'abc',
            'a+b'
        ]
        self.run_subtests(inputs, outputs, f=calculator.evaluate)

    def test05(self):
        """ evaluate - large numbers """
        inputs = [
            '99^99',
            '-1*99^99'
        ]
        outputs = [
            'inf',
            '-inf'
        ]
        self.run_subtests(inputs, outputs, f=calculator.evaluate)
