import sympy as sp

from scripts.parser import parse_eq, parse_var, parse_dom
from scripts.renderer import render_tex
from scripts.printer import make_pretty, make_pretty_multiple
from scripts.utils import Result, Error, Response


def solve_equation(args) -> Response:
    try:
        raw_eq = args['eq']
        raw_var = args['var']
        raw_dom = args['dom']
        eq = parse_eq(raw_eq)
        var = parse_var(raw_var)
        dom = parse_dom(raw_dom)
        res = sp.solveset(eq, var, dom)
        pretty = {"eq": make_pretty(eq),
                  "var": make_pretty(var)}
        if res == sp.EmptySet:
            image = render_tex(f"No solution")
        elif res == sp.Reals:
            image = render_tex(f"${var} \\in \\mathbb{{R}}$")
        elif res == sp.Complexes:
            image = render_tex(f"${var} \\in \\mathbb{{C}}$")
        elif isinstance(res, sp.Interval):
            image = render_tex(f"${var} \\in {sp.latex(res)}$")
        else:
            image = render_tex(f"${var} = {sp.latex(res)}$")
        answer = make_pretty_multiple(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
