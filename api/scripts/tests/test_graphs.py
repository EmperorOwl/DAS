import unittest
from typing import Callable

from scripts.graphs import (graph_expr_single,
                            graph_expr_multiple,
                            graph_func_single,
                            graph_func_multiple,
                            graph_parametric,
                            graph_rel_single,
                            graph_rel_multiple)
from scripts.utils import Error


class TestGraphs(unittest.TestCase):

    def run_subtests(self, f: Callable, tests: list[dict]) -> None:
        for args in tests:
            with self.subTest(args):
                res = f(args)
                self.assertNotIsInstance(res, Error)

    def test_expr_single(self):
        tests = [
            # Basic 3D expression
            {
                "expr": "x + y",
                "dom": "(-5, 5)",
                "ran": "(-5, 5)"
            },
            # Trigonometric expression
            {
                "expr": "sin(x) * cos(y)",
                "dom": "(-pi, pi)",
                "ran": "(-pi, pi)"
            },
            # Polynomial expression
            {
                "expr": "x^2 + y^2",
                "dom": "(-3, 3)",
                "ran": "(-3, 3)"
            },
            # Exponential expression
            {
                "expr": "exp(-(x^2 + y^2))",
                "dom": "(-2, 2)",
                "ran": "(-2, 2)"
            }
        ]
        self.run_subtests(graph_expr_single, tests)

    def test_expr_multiple(self):
        tests = [
            # Two simple expressions
            {
                "expr1": "x + y",
                "expr2": "x - y",
                "dom": "(-3, 3)",
                "ran": "(-3, 3)"
            },
            # Trigonometric expressions
            {
                "expr1": "sin(x) * cos(y)",
                "expr2": "cos(x) * sin(y)",
                "dom": "(-pi, pi)",
                "ran": "(-pi, pi)"
            },
            # Polynomial expressions
            {
                "expr1": "x^2 + y^2",
                "expr2": "x^2 - y^2",
                "dom": "(-2, 2)",
                "ran": "(-2, 2)"
            }
        ]
        self.run_subtests(graph_expr_multiple, tests)

    def test_func_single(self):
        tests = [
            # Basic linear function
            {
                "func": "x + 1",
                "var": "x",
                "dom": "(-5, 5)"
            },
            # Quadratic function
            {
                "func": "x^2",
                "var": "x",
                "dom": "(-3, 3)"
            },
            # Trigonometric function
            {
                "func": "sin(x)",
                "var": "x",
                "dom": "(-2*pi, 2*pi)"
            },
            # Function with range specified
            {
                "func": "x^3",
                "var": "x",
                "dom": "(-2, 2)",
                "ran": "(-8, 8)"
            },
            # Exponential function
            {
                "func": "exp(x)",
                "var": "x",
                "dom": "(-2, 2)"
            },
            # Modulo function
            {
                "func": "2 % 5",
                "var": "x",
                "dom": "(-5, 5)"
            },
            {
                "func": "Mod(2, 5)",
                "var": "x",
                "dom": "(-5, 5)"
            },
            {
                "func": "mod(2, 5)",
                "var": "x",
                "dom": "(-5, 5)"
            },
            {
                "func": "x + mod(2, 5)",
                "var": "x",
                "dom": "(-5, 5)"
            },
            {
                "func": "sin(x) % 2",
                "var": "x",
                "dom": "(-5, 5)"
            }
        ]
        self.run_subtests(graph_func_single, tests)

    def test_func_multiple(self):
        tests = [
            # Two linear functions
            {
                "func1": "x + 1",
                "func2": "x - 1",
                "var": "x",
                "dom": "(-5, 5)"
            },
            # Linear and quadratic
            {
                "func1": "x",
                "func2": "x^2",
                "var": "x",
                "dom": "(-3, 3)"
            },
            # Trigonometric functions
            {
                "func1": "sin(x)",
                "func2": "cos(x)",
                "var": "x",
                "dom": "(-2*pi, 2*pi)"
            },
            # With range specified
            {
                "func1": "x^2",
                "func2": "x^3",
                "var": "x",
                "dom": "(-2, 2)",
                "ran": "(-8, 8)"
            }
        ]
        self.run_subtests(graph_func_multiple, tests)

    def test_parametric(self):
        tests = [
            # Circle
            {
                "xt": "cos(t)",
                "yt": "sin(t)",
                "t_start": "0",
                "t_end": "2*pi"
            },
            # Ellipse
            {
                "xt": "2*cos(t)",
                "yt": "sin(t)",
                "t_start": "0",
                "t_end": "2*pi"
            },
            # Spiral
            {
                "xt": "t*cos(t)",
                "yt": "t*sin(t)",
                "t_start": "0",
                "t_end": "4*pi"
            },
            # Lemniscate
            {
                "xt": "cos(t)/(1 + sin(t)^2)",
                "yt": "sin(t)*cos(t)/(1 + sin(t)^2)",
                "t_start": "0",
                "t_end": "2*pi"
            }
        ]
        self.run_subtests(graph_parametric, tests)

    def test_rel_single(self):
        tests = [
            # Circle
            {
                "rel": "x^2 + y^2 = 1",
                "dom": "(-2, 2)",
                "ran": "(-2, 2)"
            },
            # Ellipse
            {
                "rel": "x^2/4 + y^2 = 1",
                "dom": "(-3, 3)",
                "ran": "(-2, 2)"
            },
            # Hyperbola
            {
                "rel": "x^2 - y^2 = 1",
                "dom": "(-3, 3)",
                "ran": "(-3, 3)"
            },
            # Parabola
            {
                "rel": "y = x^2",
                "dom": "(-2, 2)",
                "ran": "(-1, 4)"
            }
        ]
        self.run_subtests(graph_rel_single, tests)

    def test_rel_multiple(self):
        tests = [
            # Two circles
            {
                "rel1": "x^2 + y^2 = 1",
                "rel2": "(x-2)^2 + y^2 = 1",
                "dom": "(-1, 3)",
                "ran": "(-2, 2)"
            },
            # Circle and line
            {
                "rel1": "x^2 + y^2 = 4",
                "rel2": "y = x",
                "dom": "(-3, 3)",
                "ran": "(-3, 3)"
            },
            # Two ellipses
            {
                "rel1": "x^2/4 + y^2 = 1",
                "rel2": "x^2 + y^2/4 = 1",
                "dom": "(-3, 3)",
                "ran": "(-3, 3)"
            },
            # Hyperbola and circle
            {
                "rel1": "x^2 - y^2 = 1",
                "rel2": "x^2 + y^2 = 2",
                "dom": "(-3, 3)",
                "ran": "(-3, 3)"
            }
        ]
        self.run_subtests(graph_rel_multiple, tests)


if __name__ == '__main__':
    unittest.main()
