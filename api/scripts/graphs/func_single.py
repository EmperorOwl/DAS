import sympy as sp

from scripts.parser import parse_func, parse_var, parse_lim
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


COLOR = 'lightskyblue'


def graph_func_single(args: dict) -> Response:
    try:
        raw_func = args['func']
        raw_var = args['var']
        raw_dom = args['dom']
        raw_ran = args.get('ran', None)
        func = parse_func(raw_func, raw_var)
        var = parse_var(raw_var)
        dom = parse_lim(raw_dom)
        ran = parse_lim(raw_ran) if raw_ran else None
        plot = sp.plot(func.expr,
                       (var, dom.lower, dom.upper),
                       show=False,
                       line_color=COLOR,
                       xlabel=None,
                       ylabel=None,
                       xlim=dom,
                       ylim=ran)
        legend = [func.get_latex()]
        pretty = {"func": make_pretty(func),
                  "dom": make_pretty(dom),
                  "var": make_pretty(var),
                  "ran": make_pretty(ran)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
