""" Code for printing. """
import sympy as sp
from typing import Any

from backend.utils import Set


def _neaten(s: str) -> str:
    """ Neatens output string. """
    REPLACEMENTS = [('**', '^'),
                    ('E', 'e'),
                    ('I', 'i'),
                    ('pi', 'π')]
    for old, new in REPLACEMENTS:
        s = s.replace(old, new)
    STRIP = [' 1*', ' ', '*', '{', '}']
    for char in STRIP:
        s = s.replace(char, '')
    return s


def pretty_individual(obj: Any) -> str:
    # Simple Sets
    if isinstance(obj, Set.EMPTY):
        return "∅"

    if isinstance(obj, Set.REALS):
        return "Reals"

    if isinstance(obj, Set.COMPLEXES):
        return "Complexes"

    # Equations
    if isinstance(obj, sp.Eq):
        s = f"{obj.lhs} = {obj.rhs}"
    elif isinstance(obj, sp.Ne):
        s = f"{obj.lhs} != {obj.rhs}"

    # Other Sets
    elif isinstance(obj, Set.INTERVAL):
        left_bracket = '(' if obj.left_open else '['
        right_bracket = ')' if obj.right_open else ']'
        s = f"{left_bracket}{obj.start},{obj.end}{right_bracket}"

    elif isinstance(obj, Set.IMAGE):
        s = str(obj.lamda.expr).replace('_n', 'n')

    else:
        s = str(obj)

    return _neaten(s)


def pretty(obj: Any) -> str:
    """ Returns the pretty print of the object. """
    if isinstance(obj, Set.UNION | Set.INTERSECTION):
        res = ",".join(pretty_individual(arg) for arg in obj.args)
        return res
    return pretty_individual(obj)
