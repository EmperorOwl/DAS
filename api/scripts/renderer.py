""" Code for rendering. """
import io
import base64
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import warnings
# from sympy.plotting.plot import Plot, MatplotlibBackend

TEX_DPI = 300
PLOT_DPI = 300

matplotlib.use('agg')  # Non-interactive backend
plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern
plt.rcParams['font.family'] = 'DejaVu Serif'
warnings.filterwarnings('ignore', category=UserWarning)  # Suppress warnings


def _strip(tex: str) -> str:
    """ Removes some unnecessary latex symbols. """
    tex = tex.replace(r'\left\{', '')
    tex = tex.replace(r'\right\}', '')
    tex = tex.replace(r'\middle', '')
    tex = tex.replace(r'\;', '')  # Space
    tex = tex.replace(r'|', r',\;')
    tex = tex.replace(r'\bmod', r'\; \text{mod} \;')
    return tex


def _encode(buf: io.BytesIO) -> str:
    """ Encodes the image to Base64. """
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def render_tex(tex: str) -> str:
    """ Converts the TeX expression to a PNG image. """
    tex = _strip(tex)
    fig = plt.figure()
    buf = io.BytesIO()
    try:
        fig.text(x=0, y=0, s=tex, color='black')
        plt.savefig(buf,
                    format='png',
                    dpi=TEX_DPI,
                    bbox_inches='tight',
                    pad_inches=0.05,
                    transparent=False)
        buf.seek(0)
    finally:
        plt.close(fig)
    image = _encode(buf)
    buf.close()
    return image


def render_plot(plot: Any, legend: list[str]) -> str:
    """ Styles and saves the plot as a PNG image. """
    buf = io.BytesIO()
    try:
        plot.process_series()
        plot.ax.grid(True, linestyle=':')
        plot.fig.legend([_strip(item) for item in legend])
        plot.fig.savefig(buf, format='png', dpi=PLOT_DPI)
        buf.seek(0)
    finally:
        plot.close()
    image = _encode(buf)
    buf.close()
    return image
