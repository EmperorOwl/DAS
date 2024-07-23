import unittest

from backend import printer, parser


class TestParseEq(unittest.TestCase):
    """ Contains unit tests to check the correctness of the equation
    parser and printer.
    """

    def run_subtests(self, inputs: list[str], outputs: list[str]):
        """ [Helper] Runs a subtest for each pair input and output. """
        for s, res in zip(inputs, outputs):
            with self.subTest(s=s, res=res):
                self.assertEqual(printer.pretty(parser.parse_eq(s)), res)

    def test00(self):
        """ main """
        inputs = [
            'x^2 = 4',
            'x+2 < 5',
            'x^2 - 1 <= 0',
            'x != 1'
        ]
        outputs = [
            'x^2=4',
            'x+2<5',
            'x^2-1<=0',
            'x!=1'
        ]
        self.run_subtests(inputs, outputs)
