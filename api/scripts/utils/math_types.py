""" Code for custom math types. """
import typing
import sympy as sp


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


class Limit(typing.NamedTuple):
    """ Represents a domain or range. """
    lower: sp.Expr
    upper: sp.Expr


class Var:
    """ Contains some common variables. """
    X = sp.Symbol('x')
    Y = sp.Symbol('y')
    T = sp.Symbol('t')
