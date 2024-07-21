""" Code for plotting.

References:
    https://docs.sympy.org/latest/modules/plotting.html
"""
from backend.operations import *


# FUNCTIONS -------------------------------------------------------------------

def plot_single_func(func: str, var: str, dom: str = None, ran: str = None) -> str:
    """ Plots a single function. """
    return GraphSingleFuncOperation(func, var, dom, ran).execute()[1]


def plot_multiple_func(f1: str, f2: str, var: str, dom: str = None, ran: str = None) -> str:
    """ Plots two functions. """
    return GraphMultipleFuncOperation(f1, f2, var, dom, ran).execute()[1]


# RELATIONS -------------------------------------------------------------------

def plot_single_rel(rel: str, dom: str = None, ran: str = None) -> str:
    """ Plots a single relation. """
    return GraphSingleRelOperation(rel, dom, ran).execute()[1]


def plot_multiple_rel(rel1: str, rel2: str, dom: str = None, ran: str = None) -> str:
    """ Plots two relations. """
    return GraphMultipleRelOperation(rel1, rel2, dom, ran).execute()[1]


# 3D --------------------------------------------------------------------------

def plot_single_3d(expr: str, dom: str = None, ran: str = None) -> str:
    """ Plots a single 3D expression. """
    return GraphSingleExprOperation(expr, dom, ran).execute()[1]


def plot_multiple_3d(expr1: str, expr2: str, dom: str = None, ran: str = None) -> str:
    """ Plots two 3D expressions. """
    return GraphMultipleExprOperation(expr1, expr2, dom, ran).execute()[1]


# PARAMETRIC ------------------------------------------------------------------

def plot_parametric(xt: str, yt: str, t_start: str, t_end: str) -> str:
    """ Plots a pair of parametric equations. """
    return GraphParametricOperation(xt, yt, t_start, t_end).execute()[1]
