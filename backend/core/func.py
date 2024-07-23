import typing
import sympy as sp

from backend import printer


class Func(typing.NamedTuple):
    """ Represents a mathematical function with a name, variable and
    expression.
    """
    name: str
    var: sp.Symbol
    expr: sp.Expr

    def get_latex(self) -> str:
        """ Returns the LaTeX representation. """
        return f"${self.name}({self.var})={sp.latex(self.expr)}$"

    def __str__(self) -> str:
        """ Returns the pretty print. """
        return f"{self.name}({self.var})={printer.pretty(self.expr)}"
