""" Code for parsing.

References:
    https://docs.sympy.org/latest/modules/parsing.html
    https://stackoverflow.com/questions/45996040
"""
import re
import sympy as sp
from sympy.parsing import sympy_parser

from backend.core import Func, Limit


class ParsingError(ValueError):
    """ Represents an error in the parsing of a string to a SymPy object. """
    pass


def _parse(s: str, local_dict: dict = None) -> sp.Basic:
    """ Converts the string s to a SymPy object.
    If the string is an equation, then a SymPy relational object is returned.
    Otherwise, a SymPy expression object is returned.
    """
    BANNED = ['__', 'import', 'config', 'eval']
    for banned in BANNED:
        if banned in s.lower():
            raise ParsingError(f"{s} is invalid")
    CONVERSIONS = {
        'e': sp.E,
        'π': sp.pi,
        'arcsin': sp.asin,
        'arccos': sp.acos,
        'arctan': sp.atan,
        'cosec': sp.csc,
        'arcsinh': sp.asinh,
        'arccosh': sp.acosh,
        'arctanh': sp.atanh,
    }
    REPLACEMENTS = {
        '⋅': '*',
        '×': '*',
        '÷': '/',
        '–': '-',
        '°': '*(pi/180)',
        'deg': '*(pi/180)'
    }
    # Update local dict.
    if local_dict is None:
        local_dict = {}
    local_dict.update(CONVERSIONS)
    # Perform some replacements.
    for old, new in REPLACEMENTS.items():
        s = s.replace(old, new)
    # Finally, return the parsed expression without evaluating it.
    with sp.evaluate(False):
        return sympy_parser.parse_expr(s,
                                       local_dict=local_dict,
                                       transformations='all',
                                       evaluate=False)


def parse_eq(s: str) -> sp.Rel:
    """ Converts the string s to a SymPy relational object. """
    res = _parse(s)
    if not isinstance(res, sp.Rel):
        raise ParsingError(f"{s} is not an equation")
    return res


def parse_rel(s: str) -> sp.Rel:
    """ Converts the string s to a SymPy relational object that must contain
    either x by itself or y by itself or both x and y.
    """
    if 'x' not in s and 'y' not in s:
        raise ParsingError("Relation must contain x or y or both")
    return parse_eq(s)


def parse_expr(s, local_dict: dict = None) -> sp.Expr:
    """ Converts the string s to a SymPy expression object. """
    res = _parse(s, local_dict)
    if not isinstance(res, sp.Expr):
        raise ParsingError(f"{s} is not an expression")
    return res


def parse_func(s: str, var_str: str) -> Func:
    """ Converts the string s to a function object.
    The string can contain function notation to specify the function's name.
    If the string is an expression, then a default function name is added.
    """
    DEFAULT_FUNCTION_NAME = 'f'
    PATTERN = r"(.+)\((\w+)\)=(.+)"
    match = re.match(PATTERN, s)
    # If the user has entered a function, then check the variable in their
    # function notation matches the variable they have specified.
    # e.g. f(x) = 2x, x => check x vs x => pass
    #      f(x) = 2x, z => check x vs z => fail
    if match:
        name, func_var_str, expr_str = match.groups()
        if func_var_str != var_str:
            raise ParsingError(f"The variable in your function does not match "
                               f"the variable you have specified: "
                               f"{func_var_str} != {var_str}")
    # Otherwise, check if the user has entered an expression.
    # If so, add the function notation.
    # e.g. 2x => f(x) = 2x
    else:
        try:
            _ = parse_expr(s)
        except Exception:
            raise ParsingError(f"{s} is not a function")
        else:
            name = DEFAULT_FUNCTION_NAME
            expr_str = s
    # Finally, return the function object.
    var = parse_var(var_str)
    expr = parse_expr(expr_str, local_dict={var_str: var})
    return Func(name, var, expr)


def parse_lim(s: str) -> Limit:
    """ Converts the string s to a limit. """
    if ',' not in s:
        raise ParsingError(f'{s} is not a limit')
    for char in ['(', ')', '[', ']']:
        s = s.replace(char, '')
    lower, upper = s.split(',')
    lower, upper = parse_expr(lower), parse_expr(upper)
    if upper < lower:
        raise ParsingError(f"Upper bound is smaller than lower bound")
    return Limit(lower, upper)


def parse_dom(s: str) -> sp.S:
    """ Converts the string s to a Sympy set object. """
    s = s.lower()
    if s == 'real':
        return sp.S.Reals
    elif s == 'complex':
        return sp.S.Complexes
    raise ParsingError(f'{s} is not a valid domain')


def parse_var(s: str) -> sp.Symbol:
    """ Converts the string s to a SymPy symbol object.  """
    BANNED = ['i', 'pi', 'deg', 'e']
    if s.lower() in BANNED:
        raise ParsingError(f'{s} is an invalid variable name')
    return sp.Symbol(s)
