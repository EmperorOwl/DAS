""" Code for rendering. """

import matplotlib.pyplot as plt

from modules.bot import RENDERS_PATH

FNAME = f'{RENDERS_PATH}/tex.png'
DPI = 300


def render(tex: str):
    """ Converts the TeX expression to a PNG image. """
    plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern.
    plt.rcParams['font.family'] = 'DejaVu Serif'
    fig = plt.figure()  # Create new empty figure.
    try:
        fig.text(
            x=0,
            y=0,
            s=tex,
            color='black'
        )
        plt.savefig(
            fname=FNAME,
            dpi=DPI,
            bbox_inches='tight',
            pad_inches=0.05,
            transparent=False
        )
    finally:
        plt.close()
