import sympy as sp

from scripts.parser import parse_rel, parse_lim
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Var
from scripts.utils import Result, Error, Response


COLOR = 'darkorange'


def graph_rel_single(args: dict) -> Response:
    try:
        raw_rel = args['rel']
        raw_dom = args['dom']
        raw_ran = args['ran']
        rel = parse_rel(raw_rel)
        dom = parse_lim(raw_dom)
        ran = parse_lim(raw_ran)
        plot = sp.plot_implicit(rel,
                                (Var.X, dom.lower, dom.upper),
                                (Var.Y, ran.lower, ran.upper),
                                show=False,
                                line_color=COLOR,
                                xlabel=None,
                                ylabel=None)
        legend = [f'${sp.latex(rel)}$']
        pretty = {"rel": make_pretty(rel),
                  "dom": make_pretty(dom),
                  "ran": make_pretty(ran)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
