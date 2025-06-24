import sympy as sp
from sympy.plotting import plot3d

from scripts.parser import parse_expr, parse_lim
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Var
from scripts.utils import Result, Error, Response


def graph_expr_single(args: dict) -> Response:
    try:
        raw_expr = args['expr']
        raw_dom = args['dom']
        raw_ran = args['ran']
        expr = parse_expr(raw_expr)
        dom = parse_lim(raw_dom)
        ran = parse_lim(raw_ran)
        plot = plot3d(expr,
                      (Var.X, dom.lower, dom.upper),
                      (Var.Y, ran.lower, ran.upper),
                      show=False)
        legend = [f'$f(x,y)={sp.latex(expr)}$']
        pretty = {"expr": make_pretty(expr),
                  "dom": make_pretty(dom),
                  "ran": make_pretty(ran)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
