import sympy as sp

from scripts.parser import parse_expr
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def simplify_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        expr = parse_expr(raw_expr)
        res = sp.simplify(expr)
        pretty = {"expr": make_pretty(expr)}
        image = render_tex(f"${sp.latex(expr)} = {sp.latex(res)}$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
