import sympy as sp

from scripts.parser import parse_expr, parse_var, parse_dir
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def limit_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_var = args['var']
        raw_val = args['val']
        raw_dir = args['dir']
        expr = parse_expr(raw_expr)
        var = parse_var(raw_var)
        val = parse_expr(raw_val)
        dir = parse_dir(raw_dir)
        # Don't use the unevaluated limit as when rendered looks a bit squashed
        res = sp.limit(expr, var, val, dir)
        pretty = {
            "expr": make_pretty(expr),
            "var": make_pretty(var),
            "val": make_pretty(val),
            "dir": make_pretty(dir)
        }
        dir_tex = f"^{dir}" if dir != '+-' else ''
        image = render_tex("$"
                           f"\\lim_{{{var} \\to {sp.latex(val)}{dir_tex}}} "
                           f"({sp.latex(expr)}) = "
                           f"{sp.latex(res)}"
                           "$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
