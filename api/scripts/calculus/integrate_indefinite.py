import sympy as sp

from scripts.parser import parse_expr, parse_var
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def integrate_indefinite_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_var = args['var']
        expr = parse_expr(raw_expr)
        var = parse_var(raw_var)
        unevaluated = sp.Integral(expr, var)
        res = unevaluated.doit()
        pretty = {
            "expr": make_pretty(expr),
            "var": make_pretty(var)
        }
        tex = f"${sp.latex(unevaluated)} = {sp.latex(res)} + C$"
        tex = tex.replace(r'\int', r'\int \; \;')  # Add two spaces
        image = render_tex(tex)
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
