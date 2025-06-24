import sympy as sp

from scripts.parser import parse_expr
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Var
from scripts.utils import Result, Error, Response


def graph_parametric(args: dict) -> Response:
    try:
        raw_xt = args['xt']
        raw_yt = args['yt']
        raw_t_start = args['t_start']
        raw_t_end = args['t_end']
        xt = parse_expr(raw_xt)
        yt = parse_expr(raw_yt)
        t_start = parse_expr(raw_t_start)
        t_end = parse_expr(raw_t_end)
        plot = sp.plot_parametric(xt,
                                  yt,
                                  (Var.T, t_start, t_end),
                                  show=False)
        legend = [f'$x(t) = {sp.latex(xt)}$, '
                  f'$y(t) = {sp.latex(yt)}$']
        pretty = {"xt": make_pretty(xt),
                  "yt": make_pretty(yt),
                  "t_start": make_pretty(t_start),
                  "t_end": make_pretty(t_end)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
