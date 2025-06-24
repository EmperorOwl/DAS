import sympy as sp

from scripts.parser import parse_rel, parse_lim
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Var
from scripts.utils import Result, Error, Response


COLOR1 = 'darkorange'
COLOR2 = 'darkslateblue'


def graph_rel_multiple(args: dict) -> Response:
    try:
        raw_rel1 = args['rel1']
        raw_rel2 = args['rel2']
        raw_dom = args['dom']
        raw_ran = args['ran']
        rel1 = parse_rel(raw_rel1)
        rel2 = parse_rel(raw_rel2)
        dom = parse_lim(raw_dom)
        ran = parse_lim(raw_ran)
        plot = sp.plot_implicit(rel1,
                                (Var.X, dom.lower, dom.upper),
                                (Var.Y, ran.lower, ran.upper),
                                show=False,
                                line_color=COLOR1,
                                xlabel=None,
                                ylabel=None)
        plot2 = sp.plot_implicit(rel2,
                                 (Var.X, dom.lower, dom.upper),
                                 (Var.Y, ran.lower, ran.upper),
                                 show=False,
                                 line_color=COLOR2,
                                 xlabel=None,
                                 ylabel=None)
        plot.append(plot2[0])
        legend = [f'${sp.latex(rel1)}$', f'${sp.latex(rel2)}$']
        pretty = {"rel1": make_pretty(rel1),
                  "rel2": make_pretty(rel2),
                  "dom": make_pretty(dom),
                  "ran": make_pretty(ran)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
