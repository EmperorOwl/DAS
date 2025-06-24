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
        res = sp.integrate(expr, var)
        pretty = {
            "expr": make_pretty(expr),
            "var": make_pretty(var)
        }
        image = render_tex("$"
                           f"\\int \\ ({sp.latex(expr)}) \\ "
                           f"{{d{var}}} = "
                           f"{sp.latex(res)} + C"
                           "$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
