import typing
import sympy as sp

from backend import printer


class Limit(typing.NamedTuple):
    """ Represents a domain or range. """
    lower: sp.Expr | int
    upper: sp.Expr | int

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """ Returns the pretty print. """
        return f"[{printer.pretty(self.lower)},{printer.pretty(self.upper)}]"
