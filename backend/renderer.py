""" Code for rendering. """

import matplotlib.pyplot as plt
from pathlib import Path

FNAME = f'{Path(__file__).parent.parent}/renders/tex.png'
DPI = 300


def render(tex: str):
    """ Converts the TeX expression to a PNG image. """
    plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern.
    plt.rcParams['font.family'] = 'DejaVu Serif'
    fig = plt.figure()  # Create new empty figure.
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
    plt.close()
