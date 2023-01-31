""" Code for plotting.

References:
    https://docs.sympy.org/latest/modules/plotting.html

"""

import sympy as sp
import matplotlib.pyplot as plt
from pathlib import Path

from backend.parser import sp_obj

plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern.
plt.rcParams['font.family'] = 'DejaVu Serif'

X, Y, T = sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('t')
FNAME = f'{Path(__file__).parent.parent}/renders/plot.png'
DPI = 300


def _style_and_save(graph, labels: list[str]) -> None:
    """ Styles and saves the graph. """
    backend = graph.backend(graph)
    backend.ax[0].grid(True, linestyle=':')
    backend.process_series()
    backend.fig.legend(labels)
    backend.fig.savefig(fname=FNAME, dpi=DPI)
    backend.close()


def plot_single_function(function: sp_obj,
                         domain: tuple[float, float],
                         range: tuple[float, float]) -> None:
    """ Plots a single function. """
    _style_and_save(
        graph=sp.plot(
            function.expr, (X,) + domain, show=False,
            line_color='lightskyblue',
            xlabel=None, ylabel=None,
            xlim=domain, ylim=range
        ),
        labels=[f'${function.name}={sp.latex(function.expr)}$']
    )


def plot_single_relation(relation: sp_obj,
                         domain: tuple[float, float],
                         range: tuple[float, float]) -> None:
    """ Plots a single relation. """
    _style_and_save(
        graph=sp.plot_implicit(
            relation, (X,) + domain, (Y,) + range, show=False,
            line_color='darkorange',
            xlabel=None, ylabel=None
        ),
        labels=[f'${sp.latex(relation)}$']
    )


def plot_single_3d(expression: sp_obj,
                   domain: tuple[float, float],
                   range: tuple[float, float]) -> None:
    """ Plots a single expression in 3D. """
    _style_and_save(
        graph=sp.plotting.plot3d(
            expression, (X,) + domain, (Y,) + range, show=False,
            title=f'${sp.latex(expression)}$\n',
            xlabel=None, ylabel=None, zlabel=None
        ),
        labels=[]
    )


def plot_multiple_functions(func1: sp_obj,
                            func2: sp_obj,
                            domain: tuple[float, float],
                            range: tuple[float, float]) -> None:
    """ Plots two functions. """
    graph = sp.plot(
        func1.expr, func2.expr, (X,) + domain, show=False,
        xlabel=None, ylabel=None,
        xlim=domain, ylim=range
    )
    graph[0].line_color = 'lightskyblue'
    graph[1].line_color = 'lightgreen'
    _style_and_save(graph, labels=[f'${func1.name}={sp.latex(func1.expr)}$',
                                   f'${func2.name}={sp.latex(func2.expr)}$'])


def plot_multiple_relations(rel1: sp_obj,
                            rel2: sp_obj,
                            domain: tuple[float, float],
                            range: tuple[float, float]) -> None:
    """ Plots two relations. """
    graph = sp.plot_implicit(
        rel1, (X,) + domain, (Y,) + range, show=False,
        line_color='darkorange',
        xlabel=None, ylabel=None
    )
    graph2 = sp.plot_implicit(
        rel2, (X,) + domain, (Y,) + range, show=False,
        line_color='darkslateblue',
        xlabel=None, ylabel=None
    )
    graph.append(graph2[0])
    _style_and_save(graph, labels=[f'${sp.latex(rel1)}$',
                                   f'${sp.latex(rel2)}$'])


def plot_multiple_3d(expr1: sp_obj,
                     expr2: sp_obj,
                     domain: tuple[float, float],
                     range: tuple[float, float]) -> None:
    """ Plots two expressions in 3D. """
    _style_and_save(
        graph=sp.plotting.plot3d(
            expr1, expr2, (X,) + domain, (Y,) + range, show=False,
            title=f'${sp.latex(expr1)}\\qquad{sp.latex(expr2)}$\n',
            xlabel=None, ylabel=None, zlabel=None
        ),
        labels=[]
    )


def plot_parametric_equations(xt: sp_obj,
                              yt: sp_obj,
                              t_start: float,
                              t_end: float) -> None:
    """ Plots a pair of parametric equations. """
    _style_and_save(
        graph=sp.plot_parametric(
            xt.expr, yt.expr, (T, t_start, t_end), show=False,
            xlabel=None, ylabel=None
        ),
        labels=[f'$x(t)={sp.latex(xt.expr)}, \\ y(t)={sp.latex(yt.expr)}$']
    )
