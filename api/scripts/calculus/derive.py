import sympy as sp

from scripts.parser import parse_expr, parse_var
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def derive_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_vars = args['vars']
        expr = parse_expr(raw_expr)
        vars = [parse_var(raw_var) for raw_var in raw_vars]
        unevaluated = sp.Derivative(expr, *vars)
        res = unevaluated.doit()
        pretty = {
            "expr": make_pretty(expr),
            "vars": [make_pretty(var) for var in vars]
        }
        image = render_tex(f"${sp.latex(unevaluated)} = {sp.latex(res)}$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
