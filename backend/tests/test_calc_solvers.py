import unittest
from typing import Callable

from backend import calculator


class TestSolvers(unittest.TestCase):
    """ Contains unit tests to check `solve` and `linsolve`. """

    def run_subtests(self, in_: list[tuple], out: list[str], f: Callable):
        """ [Helper] Runs a subtest for each pair input and output
        checking the correctness of the function f.
        """
        for args, res in zip(in_, out):
            eq, *args = args
            with self.subTest(eq=eq, res=res):
                self.assertEqual(f(eq, *args)[0], res)

    # FINITE SET --------------------------------------------------------------

    def test000(self):
        """ FiniteSet - real - integers """
        inputs = [
            ('x=2', 'x'),
            ('x+2=5', 'x'),
            ('x^2=4', 'x'),
            ('abs(x)=1', 'x')
        ]
        outputs = [
            '2',
            '3',
            '-2,2',
            '-1,1'
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    def test001(self):
        """ FiniteSet - complex """
        inputs = [
            ('x^2=-4', 'x', 'complex'),
            ('z(3i+2)=7-5i', 'z', 'complex'),
            ('z^3=1', 'z', 'complex')
        ]
        outputs = [
            '-2i,2i',
            '-(5i-7)/(3i+2)',
            '1,-1/2-sqrt(3)i/2,-1/2+sqrt(3)i/2'
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    def test002(self):
        """ FiniteSet - real - logs """
        inputs = [
            ('-7e^x+3e^(2x)+2=0', 'x'),

        ]
        outputs = [
            'log(2),-log(3)',

        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # INTERVAL ----------------------------------------------------------------

    def test010(self):
        """ """
        pass

    # PRODUCT -----------------------------------------------------------------

    def test020(self):
        """ """
        pass

    # IMAGE -------------------------------------------------------------------

    def test030(self):
        """ ImageSet - trig """
        inputs = [
            ('cos(x)=1', 'x'),
            ('sin(x)=1', 'x'),
            ('tan(x)=1', 'x'),
            ('tan(x)=0', 'x'),
            ('tan(x)=-1', 'x')
        ]
        outputs = [
            '2nπ',
            '2nπ+π/2',
            'nπ+π/4',
            'nπ',
            'nπ+3π/4'
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # COMPLEX_REGION ----------------------------------------------------------

    def test040(self):
        """ """
        pass

    # CONDITION ---------------------------------------------------------------

    @unittest.skip("Not implemented yet")
    def test050(self):
        """ ConditionSet - trig """
        inputs = [
            ('sin(cos(x)) = 0', 'x')
        ]
        outputs = ['todo']
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # NATURALS ----------------------------------------------------------------

    def test060(self):
        """ """
        pass

    # NATURALS0 ---------------------------------------------------------------

    def test070(self):
        """ """
        pass

    # INTEGERS ----------------------------------------------------------------

    def test080(self):
        """ """
        pass

    # REALS -------------------------------------------------------------------

    def test090(self):
        """ Reals """
        inputs = [
            ('x=x', 'x', 'real'),
            ('x^2+1 > 0', 'x', 'real')
        ]
        outputs = ['Reals'] * len(inputs)
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # COMPLEXES ---------------------------------------------------------------

    def test100(self):
        """ Complexes """
        inputs = [
            ('x=x', 'x', 'complex'),
        ]
        outputs = ['Complexes'] * len(inputs)
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # EMPTY -------------------------------------------------------------------

    def test110(self):
        """ EmptySet """
        inputs = [
            ('x^2=-4', 'x', 'real'),
            ('x^2+1<0', 'x', 'real')
        ]
        outputs = ['∅'] * len(inputs)
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # UNION -------------------------------------------------------------------

    def test120(self):
        """ Union[ImageSet, ImageSet] - trig """
        inputs = [
            ('sin(x)=0', 'x'),
            ('cos(x)=0', 'x'),
            ('sin(x)cos(x)=1/4', 'x')
        ]
        outputs = [
            '2nπ,2nπ+π',
            '2nπ+π/2,2nπ+3π/2',
            'nπ+5π/12,nπ+π/12'
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    def test121(self):
        """ Union[ImageSet] - trig """
        inputs = [
            ('sin(2x)+cos(x)=0', 'x'),
        ]
        outputs = [
            '2nπ+π/2,2nπ+3π/2,2nπ+7π/6,2nπ+11π/6',
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    def test125(self):
        """ Union[Interval, Interval] """
        inputs = [
            ('x != 1', 'x')
        ]
        outputs = [
            '(-oo,1),(1,oo)'
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # INTERSECTION ------------------------------------------------------------

    def test130(self):
        """ Intersection """
        inputs = [
            ('x=a', 'x'),
        ]
        outputs = [
            'Reals,a',
        ]
        self.run_subtests(inputs, outputs, f=calculator.solve)

    # LINSOLVE ----------------------------------------------------------------

    def test999(self):
        """ linsolve """
        inputs = [
            (['3x+2y-z=1', '2x-2y+4z=-2', '2x-y+2z=0'], ['x', 'y', 'z']),
            (['x+y=2', '2x+y=4'], ['x', 'y'])
        ]
        outputs = [
            '(1,-2,-2)',
            '(2,0)'
        ]
        self.run_subtests(inputs, outputs, f=calculator.linsolve)
