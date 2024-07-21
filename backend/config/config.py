""" Contains some configuration variables for the backend. """
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

TEX_DPI = 300
PLOT_DPI = 300

TEX_FNAME = 'tex.png'
PLOT_FNAME = 'plot.png'

TEX_PATH = os.path.abspath(os.path.join(CURR_DIR, '../../renders/' + TEX_FNAME))
PLOT_PATH = os.path.abspath(os.path.join(CURR_DIR, '../../renders/' + PLOT_FNAME))
