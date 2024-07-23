import unittest

from backend import parser


class TestParseFunc(unittest.TestCase):
    """ Contains unit tests to check the correctness of the function
    parser.
    """

    def run_subtests(self,
                     inputs: list[tuple[str, str]],
                     outputs: list[tuple[str, str, str]]):
        """ [Helper] Runs a subtest for each pair input and output. """
        for args, res in zip(inputs, outputs):
            with self.subTest(args=args, res=res):
                func = parser.parse_func(args[0], args[1])
                self.assertEqual(func.name, res[0])
                self.assertEqual(str(func.var), res[1])
                self.assertEqual(str(func.expr), res[2])

    def test00(self):
        """ one letter function and variable names """
        inputs = [
            ('f(x)=2x+2', 'x'),
            ('g(x)=3x+3', 'x')
        ]
        outputs = [
            ('f', 'x', '2*x + 2'),
            ('g', 'x', '3*x + 3')
        ]
        self.run_subtests(inputs, outputs)

    def test01(self):
        """ more than one letter variable names """
        inputs = [
            ('f(abc)=2abc+2', 'abc'),
            ('g(abc)=3abc+3', 'abc')
        ]
        outputs = [
            ('f', 'abc', '2*abc + 2'),
            ('g', 'abc', '3*abc + 3')
        ]
        self.run_subtests(inputs, outputs)

    def test02(self):
        """ more than one letter function names """
        inputs = [
            ('func(x)=2x+2', 'x'),
            ('function(x)=3x+3', 'x')
        ]
        outputs = [
            ('func', 'x', '2*x + 2'),
            ('function', 'x', '3*x + 3')
        ]
        self.run_subtests(inputs, outputs)

    def test10(self):
        """ no function notation just expression """
        inputs = [
            ('2x+2', 'x')
        ]
        outputs = [
            ('f', 'x', '2*x + 2')
        ]
        self.run_subtests(inputs, outputs)
