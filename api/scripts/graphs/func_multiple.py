import sympy as sp

from scripts.parser import parse_func, parse_var, parse_lim
from scripts.renderer import render_plot
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


COLOR1 = 'lightskyblue'
COLOR2 = 'lightgreen'


def graph_func_multiple(args: dict) -> Response:
    try:
        raw_func1 = args['func1']
        raw_func2 = args['func2']
        raw_var = args['var']
        raw_dom = args['dom']
        raw_ran = args.get('ran', None)
        func1 = parse_func(raw_func1, raw_var)
        func2 = parse_func(raw_func2, raw_var)
        var = parse_var(raw_var)
        dom = parse_lim(raw_dom)
        ran = parse_lim(raw_ran) if raw_ran else None
        plot = sp.plot(func1.expr,
                       func2.expr,
                       (var, dom.lower, dom.upper),
                       show=False,
                       xlabel=None,
                       ylabel=None,
                       xlim=dom,
                       ylim=ran)
        plot[0].line_color = COLOR1
        plot[1].line_color = COLOR2
        legend = [func1.get_latex(), func2.get_latex()]
        pretty = {"func1": make_pretty(func1),
                  "func2": make_pretty(func2),
                  "dom": make_pretty(dom),
                  "var": make_pretty(var),
                  "ran": make_pretty(ran)}
        image = render_plot(plot, legend)
        return Result(pretty, image)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
