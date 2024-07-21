""" Code for rendering. """
import matplotlib.pyplot as plt
from sympy.plotting.plot import MatplotlibBackend

from backend.config import TEX_PATH, TEX_DPI
from backend.config import PLOT_PATH, PLOT_DPI


def _setup() -> None:
    """ Configures the fonts. """
    plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern.
    plt.rcParams['font.family'] = 'DejaVu Serif'


def _strip(tex: str) -> str:
    """ Removes some unnecessary latex symbols. """
    tex = tex.replace(r'\left\{', '')
    tex = tex.replace(r'\right\}', '')
    tex = tex.replace(r'\middle', '')
    tex = tex.replace(r'\;', '')  # Space
    tex = tex.replace(r'|', r',\;')
    return tex


def render(tex: str) -> None:
    """ Converts the TeX expression to a PNG image. """
    _setup()
    tex = _strip(tex)
    fig = plt.figure()
    try:
        fig.text(x=0, y=0, s=tex, color='black')
        plt.savefig(fname=TEX_PATH,
                    dpi=TEX_DPI,
                    bbox_inches='tight',
                    pad_inches=0.05,
                    transparent=False)
    finally:
        plt.close()


def render_plot(plot: MatplotlibBackend, legend: list[str]) -> None:
    """ Styles and saves the plot as a PNG. """
    _setup()
    try:
        plot.process_series()
        plot.ax.grid(True, linestyle=':')
        plot.fig.legend(legend)
        plot.fig.savefig(fname=PLOT_PATH, dpi=PLOT_DPI)
    finally:
        plot.close()
