import sympy as sp

from scripts.parser import parse_expr, parse_var
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def derive_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_var = args['var']
        expr = parse_expr(raw_expr)
        var = parse_var(raw_var)
        res = sp.diff(expr, var)
        pretty = {
            "expr": make_pretty(expr),
            "var": make_pretty(var)
        }
        image = render_tex("$"
                           f"\\frac{{d}}{{d{var}}} "
                           f"({sp.latex(expr)}) = "
                           f"{sp.latex(res)}"
                           "$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
