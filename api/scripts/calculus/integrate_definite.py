import sympy as sp

from scripts.parser import parse_expr, parse_var
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def integrate_definite_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_var = args['var']
        raw_lt = args['lt']
        raw_ut = args['ut']
        expr = parse_expr(raw_expr)
        var = parse_var(raw_var)
        lt = parse_expr(raw_lt)
        ut = parse_expr(raw_ut)
        res = sp.integrate(expr, (var, lt, ut))
        pretty = {
            "expr": make_pretty(expr),
            "var": make_pretty(var),
            "lt": make_pretty(lt),
            "ut": make_pretty(ut)
        }
        image = render_tex("$"
                           f"\\int_{{{sp.latex(lt)}}}^"
                           f"{{{sp.latex(ut)}}} \\ "
                           f"({sp.latex(expr)}) \\ "
                           f"{{d{var}}} = "
                           f"{sp.latex(res)}"
                           "$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
