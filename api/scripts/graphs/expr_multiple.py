import sympy as sp
from sympy.plotting import plot3d

from scripts.parser import parse_expr, parse_lim
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Var
from scripts.utils import Result, Error, Response


def graph_expr_multiple(args: dict) -> Response:
    try:
        raw_expr1 = args['expr1']
        raw_expr2 = args['expr2']
        raw_dom = args['dom']
        raw_ran = args['ran']
        expr1 = parse_expr(raw_expr1)
        expr2 = parse_expr(raw_expr2)
        dom = parse_lim(raw_dom)
        ran = parse_lim(raw_ran)
        plot = plot3d(expr1,
                      expr2,
                      (Var.X, dom.lower, dom.upper),
                      (Var.Y, ran.lower, ran.upper),
                      show=False)
        legend = [f'$f1(x,y) = {sp.latex(expr1)}$',
                  f'$f2(x,y) = {sp.latex(expr2)}$']
        pretty = {"expr1": make_pretty(expr1),
                  "expr2": make_pretty(expr2),
                  "dom": make_pretty(dom),
                  "ran": make_pretty(ran)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
