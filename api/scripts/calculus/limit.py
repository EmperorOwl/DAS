import sympy as sp

from scripts.parser import parse_expr, parse_var
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def limit_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_var = args['var']
        raw_val = args['val']
        expr = parse_expr(raw_expr)
        var = parse_var(raw_var)
        val = parse_expr(raw_val)
        res = sp.limit(expr, var, val)
        pretty = {
            "expr": make_pretty(expr),
            "var": make_pretty(var),
            "val": make_pretty(val)
        }
        image = render_tex("$"
                           f"\\lim_{{{var} \\to {sp.latex(val)}}} "
                           f"({sp.latex(expr)}) = "
                           f"{sp.latex(res)}"
                           "$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
