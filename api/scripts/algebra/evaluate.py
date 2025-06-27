import sympy as sp
import humanize

from scripts.parser import parse_expr
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def evaluate_expression(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        expr = parse_expr(raw_expr)  # Don't evaluate to display original
        res = parse_expr(raw_expr, evaluate=True)
        pretty = {"expr": make_pretty(expr)}
        symbol = '='
        try:
            # Integer result
            res = int(res) if float(res).is_integer() else float(res)
            # Humanized notation
            if 10**6 <= abs(res) <= 10**35:
                humanized_res = humanize.intword(res, format="%.3g")
                pretty['humanized_res'] = humanized_res
            # Result too large
            elif abs(res) > 10**35:
                res = sp.oo if res > 0 else -sp.oo
                symbol = r'\approx'
            # Result too small
            elif 0 < abs(res) < 10**(-35):
                res = 0
                symbol = r'\approx'
        except TypeError:
            pass  # As not a number, user probably entered a variable.
        image = render_tex(f"${sp.latex(expr)} {symbol} {sp.latex(res)}$")
        answer = make_pretty(res)
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
