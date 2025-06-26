""" Code for printing. """
import re
import sympy as sp
from typing import Any

from scripts.utils import Func, Limit


def _neaten(s: str) -> str:
    """ Replaces some characters with more readable ones
    and strips unnecessary characters. 
    """
    STRIP = [' ']
    for char in STRIP:
        s = s.replace(char, '')

    REPLACEMENTS = [('**', '^'),
                    ('E', 'e'),
                    ('I', 'i'),
                    ('-1*', '-'),
                    ('(-1)*', '-'),
                    ('Mod', 'mod')]
    for old, new in REPLACEMENTS:
        s = s.replace(old, new)

    # Strip * between non-number*non-number or number*non-number
    # Don't strip between number*non-number or number*number
    s = re.sub(r'(?<=[a-zA-Z0-9\)\]])\*(?=[a-zA-Z\(])', '', s)

    s = s.replace('pi', 'π')
    return s


def make_pretty(obj: Any) -> str:
    """ Returns the pretty print of the object. """
    # Func
    if isinstance(obj, Func):
        return f"{obj.name}({obj.var})={make_pretty(obj.expr)}"

    # Limit
    if isinstance(obj, Limit):
        return f"[{make_pretty(obj.lower)},{make_pretty(obj.upper)}]"

    # Simple Sets
    if obj == sp.EmptySet:
        return "∅"
    if obj == sp.Reals:
        return "Reals"
    if obj == sp.Complexes:
        return "Complexes"

    # Equations
    if isinstance(obj, sp.Eq):
        s = f"{obj.lhs} = {obj.rhs}"
    elif isinstance(obj, sp.Ne):
        s = f"{obj.lhs} != {obj.rhs}"

    # Interval
    elif isinstance(obj, sp.Interval):
        left_bracket = '(' if obj.left_open else '['
        right_bracket = ')' if obj.right_open else ']'
        s = f"{left_bracket}{obj.start},{obj.end}{right_bracket}"

    # Image Set
    elif isinstance(obj, sp.ImageSet):
        s = str(obj.lamda.expr).replace('_n', 'n')

    else:
        s = str(obj)

    return _neaten(s)


def make_pretty_multiple(obj: Any) -> list[str]:
    """ Returns the pretty print of a sequence of objects. """
    if isinstance(obj, (sp.FiniteSet, sp.Union, sp.Intersection)):
        return [make_pretty(arg) for arg in obj.args]
    return [make_pretty(obj)]
