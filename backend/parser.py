""" Code for parsing.

References:
    https://docs.sympy.org/latest/modules/parsing.html

"""

import typing
import sympy as sp

CONVERSIONS = {
    'e': sp.E,
    'π': sp.pi,
}

REPLACEMENTS = {
    '×': '*',
    '÷': '/',
    '–': '-',
    'arcsin': 'asin',
    'arccos': 'acos',
    'arctan': 'atan',
    'cosec': 'csc',
    ',': '',
    '°': '*(pi/180)',
    'deg': '*(pi/180)'
}

sp_obj = typing.TypeVar('sp_obj')


def parse(expr: str) -> sp_obj:
    """ Converts the string to its equivalent SymPy object. """
    for old, new in REPLACEMENTS.items():
        expr = expr.replace(old, new)
    return sp.parsing.sympy_parser.parse_expr(expr,
                                              local_dict=CONVERSIONS,
                                              transformations='all',
                                              evaluate=False)


def split(func: str, var: str) -> (str, sp_obj):
    """ Converts only the expression part of the function. """
    try:
        name, expr = func.split('=')
    except ValueError:
        name, expr = f'f({var})', func
    return name, parse(expr)
