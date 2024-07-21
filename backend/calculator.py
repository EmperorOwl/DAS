""" Code for calculating.

Each function returns two strings.
1. The result of the operation.
2. The pretty print of the result.

References:
    https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html
    https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html
    https://docs.sympy.org/latest/tutorials/intro-tutorial/solvers.html
    https://docs.sympy.org/latest/modules/solvers/solveset.html
"""
from backend.operations import *


def display(text: str) -> (str, str):
    """ Converts the string text to an image taking into account any tex. """
    return DisplayOperation(text).execute()


# ALGEBRA ---------------------------------------------------------------------

def expand(expr: str) -> (str, str):
    """ Returns the expanded form of the expression expr. """
    return ExpandOperation(expr).execute()


def factor(expr: str) -> (str, str):
    """ Returns the factored form of the expression expr. """
    return FactorOperation(expr).execute()


def simplify(expr: str) -> (str, str):
    """ Returns the simplified form of the expression expr. """
    return SimplifyOperation(expr).execute()


def evaluate(expr: str) -> (str, str):
    """ Returns the evaluated form of the expression expr. """
    return EvaluateOperation(expr).execute()


# CALCULUS --------------------------------------------------------------------

def derive(expr: str, var: str) -> (str, str):
    """ Returns the derivative of the expression expr with respect to the
    variable var.
    """
    return DeriveOperation(expr, var).execute()


def integrate_indefinite(expr: str, var: str) -> (str, str):
    """ Returns the indefinite integral of the expression expr with respect to
    the variable var.
    """
    return IntegrateIndefiniteOperation(expr, var).execute()


def integrate_definite(expr: str, var: str, lt: str, ut: str) -> (str, str):
    """ Returns the definite integral of the expression expr with respect to
    the variable var over the interval (lt, ut).
    """
    return IntegrateDefiniteOperation(expr, var, lt, ut).execute()


def limit(expr: str, var: str, val: str) -> (str, str):
    """ Returns the limit of the expression expr with respect to the variable
    var at value val.
    """
    return LimitOperation(expr, var, val).execute()


# SOLVERS ---------------------------------------------------------------------

def solve(eq: str, var: str, dom: str = 'real') -> (str, str):
    """ Returns the solutions to the solved equation eq for variable var over
    the domain dom.
    """
    return SolveOperation(eq, var, dom).execute()


def linsolve(equations: list[str], variables: list[str]) -> (str, str):
    """ Returns the solution set of the linear system equations. """
    return LinsolveOperation(equations, variables).execute()
