""" Code for plotting.

References:
    https://docs.sympy.org/latest/modules/plotting.html

"""

import sympy as sp
import matplotlib.pyplot as plt

from modules import transform
from modules.bot import RENDERS_PATH

plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern.
plt.rcParams['font.family'] = 'DejaVu Serif'

X, Y, T = sp.Symbol('x'), sp.Symbol('y'), sp.Symbol('t')
FNAME = f'{RENDERS_PATH}/plot.png'
DPI = 300


def _style_and_save(graph, labels: list[str]) -> None:
    """ Styles and saves the graph. """
    backend = graph.backend(graph)
    backend.ax[0].grid(True, linestyle=':')
    backend.ax[0].xaxis.set_label_coords(0, 0)
    backend.ax[0].yaxis.set_label_coords(0, 0)
    backend.process_series()
    backend.fig.legend(labels)
    backend.fig.savefig(fname=FNAME, dpi=DPI)
    backend.close()


def plot_single_function(function: transform.Function,
                         variable: str,
                         domain: transform.Limit,
                         range: transform.Limit) -> None:
    """ Plots a single function. """
    _style_and_save(
        graph=sp.plot(
            function.expr,
            (sp.Symbol(variable),) + domain,
            show=False,
            line_color='lightskyblue',
            xlabel=None,
            ylabel=None,
            xlim=domain,
            ylim=range
        ),
        labels=[f'${function.name}={sp.latex(function.expr)}$']
    )


def plot_single_relation(relation: transform.Relation,
                         domain: transform.Limit,
                         range: transform.Limit) -> None:
    """ Plots a single relation. """
    _style_and_save(
        graph=sp.plot_implicit(
            relation,
            (X,) + domain,
            (Y,) + range,
            show=False,
            line_color='darkorange',
            xlabel='y',
            ylabel='x'
        ),
        labels=[f'${sp.latex(relation)}$']
    )


def plot_single_3d(expression: transform.Expression,
                   domain: transform.Limit,
                   range: transform.Limit) -> None:
    """ Plots a single expression in 3D. """
    _style_and_save(
        graph=sp.plotting.plot3d(
            expression,
            (X,) + domain,
            (Y,) + range,
            show=False,
            title=f'${sp.latex(expression)}$\n'
        ),
        labels=[]
    )


def plot_multiple_functions(func1: transform.Function,
                            func2: transform.Function,
                            var: str,
                            domain: transform.Limit,
                            range: transform.Limit) -> None:
    """ Plots two functions. """
    graph = sp.plot(
        func1.expr,
        func2.expr,
        (sp.Symbol(var),) + domain,
        show=False,
        xlabel=None,
        ylabel=None,
        xlim=domain,
        ylim=range
    )
    graph[0].line_color = 'lightskyblue'
    graph[1].line_color = 'lightgreen'
    _style_and_save(graph, labels=[f'${func1.name}={sp.latex(func1.expr)}$',
                                   f'${func2.name}={sp.latex(func2.expr)}$'])


def plot_multiple_relations(rel1: transform.Relation,
                            rel2: transform.Relation,
                            domain: transform.Limit,
                            range: transform.Limit) -> None:
    """ Plots two relations. """
    graph = sp.plot_implicit(
        rel1,
        (X,) + domain,
        (Y,) + range,
        show=False,
        line_color='darkorange',
        xlabel='y',
        ylabel='x'
    )
    graph2 = sp.plot_implicit(
        rel2,
        (X,) + domain,
        (Y,) + range,
        show=False,
        line_color='darkslateblue',
        xlabel='y',
        ylabel='x'
    )
    graph.append(graph2[0])
    _style_and_save(graph, labels=[f'${sp.latex(rel1)}$',
                                   f'${sp.latex(rel2)}$'])


def plot_multiple_3d(expr1: transform.Expression,
                     expr2: transform.Expression,
                     domain: transform.Limit,
                     range: transform.Limit) -> None:
    """ Plots two expressions in 3D. """
    _style_and_save(
        graph=sp.plotting.plot3d(
            expr1,
            expr2,
            (X,) + domain,
            (Y,) + range,
            show=False,
            title=f'${sp.latex(expr1)}\\qquad{sp.latex(expr2)}$\n'
        ),
        labels=[]
    )


def plot_parametric_equations(xt: transform.Function,
                              yt: transform.Function,
                              t_start: float,
                              t_end: float) -> None:
    """ Plots a pair of parametric equations. """
    _style_and_save(
        graph=sp.plot_parametric(
            xt.expr,
            yt.expr,
            (T, t_start, t_end),
            show=False
        ),
        labels=[f'$x(t)={sp.latex(xt.expr)}, \\ y(t)={sp.latex(yt.expr)}$']
    )


def _style_and_save_vector(x_max: float, y_max: float):
    """ Styles and saves vector graphs. """
    plt.grid(True, linestyle=':')  # Set grid.
    plt.xlim(-x_max, x_max)  # Set horizontal limits.
    plt.ylim(-y_max, y_max)  # Set vertical limits.
    ax = plt.gca()  # Fetch current axes.
    ax.spines['left'].set_position('center')  # Move left axis to center.
    ax.spines['bottom'].set_position('center')  # Move bottom axis to center.
    ax.spines['right'].set_color('none')  # Remove right axis.
    ax.spines['top'].set_color('none')  # Remove top axis.
    plt.savefig(fname=FNAME, dpi=DPI)  # Save figure.


def plot_single_vector(v: transform.Vector,
                       o: transform.Vector) -> None:
    """ Plots a vector. """
    try:
        plt.quiver(
            o.x,
            o.y,
            v.x,
            v.y,
            color='lightskyblue',
            angles='xy',
            scale_units='xy',
            scale=1
        )
        # Label the end of the vector.
        plt.text(
            o.x + v.x,
            o.y + v.y,
            f"$({o.x + v.x:g}, {o.y + v.y:g})$"
        )
        _style_and_save_vector(
            x_max=1.5 * max(map(abs, [o.x + v.x, o.x, v.x])),
            y_max=1.5 * max(map(abs, [o.y + v.y, o.y, v.y]))
        )
    finally:
        plt.close()


def plot_multiple_vectors(v1: transform.Vector,
                          v2: transform.Vector,
                          o1: transform.Vector,
                          o2: transform.Vector) -> None:
    """ Plots two vectors. """
    try:
        plt.quiver(
            [o1.x, o2.x],
            [o1.y, o2.y],
            [v1.x, v2.x],
            [v1.y, v2.y],
            color=['darkorange', 'darkslateblue'],
            angles='xy',
            scale_units='xy',
            scale=1
        )
        # Label the end of the first vector.
        plt.text(
            o1.x + v1.x,
            o1.y + v1.y,
            f"$({o1.x + v1.x:g}, {o1.y + v1.y:g})$"
        )
        # Label the end of the second vector.
        plt.text(
            o2.x + v2.x,
            o2.y + v2.y,
            f"$({o2.x + v2.x:g}, {o2.y + v2.y:g})$"
        )
        _style_and_save_vector(
            x_max=1.5 * max(map(abs, [o1.x + v1.x, o2.x + v2.x, o1.x, v1.x, o2.x, v2.x])),
            y_max=1.5 * max(map(abs, [o1.y + v1.y, o2.y + v2.y, o1.y, v1.y, o2.y, v2.y])),
        )
    finally:
        plt.close()
