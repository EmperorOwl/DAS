""" Code for parsing.

References:
    https://docs.sympy.org/latest/modules/parsing.html
    https://stackoverflow.com/questions/45996040
"""
import re
import sympy as sp
from sympy.parsing import sympy_parser
from tokenize import TokenError

from scripts.utils import Func, Limit, BANNED


class ParsingError(ValueError):
    """ Represents an error in the parsing of a string to a SymPy object. """
    pass


def _parse(s: str,
           local_dict: dict | None = None,
           evaluate: bool = False) -> sp.Basic:
    """ Converts the string s to a SymPy object.
    If the string is an equation, then a SymPy relational object is returned.
    Otherwise, a SymPy expression object is returned.
    """
    # Blacklist
    INAVLID = ['_', '$', '#', ';', '!!!']
    for item in BANNED + INAVLID:
        if item in s.lower():
            raise ParsingError(f"{s} is invalid")
    # Latex
    if '\\' in s:
        raise ParsingError("Latex input is not accepted")
    # Absolute value
    if '|' in s:
        raise ParsingError("Please use abs(x) instead of |x|")
    # Power
    for i, digit in enumerate(['²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']):
        if digit in s:
            raise ParsingError(f"Please use ^{i+2} instead of {digit}")
    if 'squared' in s.lower():
        raise ParsingError("Please use ^2 instead of squared")
    if 'cubed' in s.lower():
        raise ParsingError("Please use ^3 instead of cubed")
    # Square root
    if '√' in s or 'square root' in s.lower():
        raise ParsingError("Please use sqrt(x) or root(x, 2) "
                           "instead of √x or square root x")
    # Brackets
    if '{' in s or '}' in s:
        raise ParsingError(f"Please use () instead of {{}}")
    if '[' in s or ']' in s:
        raise ParsingError(f"Please use () instead of []")
    # Local dict
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
    if local_dict is None:
        local_dict = {}
    local_dict.update(CONVERSIONS)
    # Manual replacements
    REPLACEMENTS = {
        '⋅': '*',
        '×': '*',
        '÷': '/',
        '–': '-',
        '°': '*(pi/180)',
        'deg': '*(pi/180)',
        'mod': 'Mod',
        'million': '*(10^6)',
        'billion': '*(10^9)',
        'trillion': '*(10^12)',
        'quadrillion': '*(10^15)',
        'quintillion': '*(10^18)',
        'sextillion': '*(10^21)',
        'septillion': '*(10^24)',
        'octillion': '*(10^27)',
        'nonillion': '*(10^30)',
        'decillion': '*(10^33)',
    }
    for old, new in REPLACEMENTS.items():
        s = s.replace(old, new)
    # Parsing
    transformations = sympy_parser.T[:11]  # Skip rationalize
    try:
        with sp.evaluate(evaluate):  # Prevents 1=1 from evaluating to True
            return sympy_parser.parse_expr(s,
                                           local_dict=local_dict,
                                           transformations=transformations,
                                           evaluate=evaluate)
    except TokenError:
        raise ParsingError(f"{s} is probably missing a closing bracket")
    except AttributeError:
        if '.' in s:
            raise ParsingError(f"Please use * instead of .")
        raise ParsingError(f"{s} is invalid")
    except TypeError:
        if 'root' in s.lower():
            raise ParsingError("root() requires 2 arguments\n"
                               "root(n, k) returns the kth root of n\n"
                               "e.g. root(8, 3) returns the cube root of 8")
        raise ParsingError(f"{s} is invalid")
    except SyntaxError:
        raise ParsingError(f"{s} is invalid")


def parse_expr(s: str,
               local_dict: dict | None = None,
               evaluate: bool = False) -> sp.Expr:
    """ Converts the string s to a SymPy expression object. """
    if '=' in s:
        raise ParsingError("Do not use = in expressions")
    res = _parse(s, local_dict, evaluate)
    if not isinstance(res, sp.Expr):
        raise ParsingError(f"{s} is not an expression")
    return res


def parse_var(s: str) -> sp.Symbol:
    """ Converts the string s to a SymPy symbol object.  """
    BANNED = ['i', 'pi', 'deg', 'e']
    if s.lower() in BANNED or s.isdigit():
        raise ParsingError(f'{s} is an invalid variable name')
    return sp.Symbol(s)


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


def parse_func(s: str, var_str: str) -> Func:
    """ Converts the string s to a function object.
    The string can contain function notation to specify the function's name.
    If the string is an expression, then a default function name is added.
    """
    DEFAULT_FUNCTION_NAME = 'f'
    PATTERN = r"(.+)\((\w+)\)\s*=\s*(.+)"
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
    if sp.Lt(upper, lower):
        raise ParsingError(f"Upper bound is smaller than lower bound")
    return Limit(lower, upper)


def parse_dom(s: str) -> sp.Set:
    """ Converts the string s to a Sympy set object representing either the
    real or complex domain.
    """
    if s.lower() == 'real':
        return sp.Reals
    elif s.lower() == 'complex':
        return sp.Complexes
    raise ParsingError(f'{s} is not a valid domain')


def parse_dir(s: str) -> str:
    """ Converts the string s to a direction. """
    if s not in ['+', '-', '+-']:
        raise ParsingError(f'{s} is not a valid direction')
    return s
