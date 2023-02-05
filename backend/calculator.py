""" Code for calculating. """

import sympy as sp

from backend import renderer
from backend.parser import sp_obj


def display(func: sp_obj) -> None:
    """ Displays a function. """
    renderer.render(f'${func.name}={sp.latex(func.expr)}$')


def limit(func: sp_obj, var: str, coord: str) -> sp_obj:
    """ Finds the limit of a function at a coordinate. """
    var = sp.Symbol(var)
    res = sp.limit(func.expr, var, coord)
    coord = coord.replace('oo', '\\infty') if 'oo' in coord else coord
    renderer.render(f"$\\lim_{{{var} \\rightarrow {coord}}} "
                    f"({sp.latex(func.expr)}) = {sp.latex(res)}$")
    return res


def derive(func: sp_obj, var: str) -> sp_obj:
    """ Derives a function with respect to a variable. """
    var = sp.Symbol(var)
    res = sp.diff(func.expr, var)
    renderer.render(f"$\\frac{{d}}{{d{var}}} "
                    f"({sp.latex(func.expr)}) = {sp.latex(res)}$")
    return res


def integrate(func: sp_obj,
              var: str,
              lt: int = None,
              ut: int = None) -> (sp_obj, sp_obj):
    """ Integrates a function with respect to a variable. """
    var = sp.Symbol(var)
    indefinite = sp.expand(sp.simplify(sp.integrate(func.expr, var)))
    if lt and ut:  # If terminals, then evaluate for the definite integral.
        definite = sp.integrate(func.expr, (var, lt, ut))
        renderer.render(f"$\\int_{{{lt}}}^{{{ut}}} \\ "
                        f"({sp.latex(func.expr)}) \\ dx = {definite}$")
    else:
        definite = None
        renderer.render(f"$\\int \\ ({sp.latex(func.expr)}) \\ dx "
                        f"= {sp.latex(indefinite)} + C$")
    return indefinite, definite


def solve(eq: sp_obj, var: str, dom: str) -> None:
    """ Solves an equation with respect to a variable and domain. """
    var = sp.Symbol(var)
    dom = sp.S.Reals if dom.lower() == 'real' else sp.S.Complexes
    sols = sp.solveset(eq, var, dom)
    if type(sols) == sp.sets.sets.EmptySet:  # Equation has no sols.
        renderer.render("No solution over ℝ")
    elif type(sols) == sp.sets.fancysets.Reals:  # Equation has infinite sols.
        renderer.render(f'${var} \\in \\mathbb{{R}}$')
    else:
        renderer.render(f"${var} = {sp.latex(sols)}$".replace(
            '\\left', '').replace(
            '\\middle', '').replace(
            '\\right', '').replace(
            '\\{', '').replace(
            '\\}', '').replace(
            ' |', ',')
        )


def linsolve(eq1: sp_obj, eq2: sp_obj, var1: str, var2: str) -> None:
    """ Solves a pair of linear equations. """
    sols = sp.linsolve([eq1, eq2], sp.Symbol(var1), sp.Symbol(var2))
    if type(sols) == sp.sets.sets.EmptySet:  # Equation has no sols.
        renderer.render("No solution; the linear system is inconsistent.")
    else:
        renderer.render(
            f"${var1} = {sp.latex(sols.args[0][0])}$, "
            f"${var2} = {sp.latex(sols.args[0][1])}$".replace(
                '\\left', '').replace(
                '\\middle', '').replace(
                '\\right', '').replace(
                '\\{', '').replace(
                '\\}', '').replace(
                ' |', ',')
        )


def expand(expr: sp_obj) -> None:
    """ Expands the expression. """
    res = sp.expand(expr)
    renderer.render(f'${sp.latex(expr)} = {sp.latex(res)}$')


def factor(expr: sp_obj) -> None:
    """ Factors the expression. """
    res = sp.factor(expr)
    renderer.render(f'${sp.latex(expr)} = {sp.latex(res)}$')


def simplify(expr: sp_obj) -> None:
    """ Simplifies the expression. """
    if expr in [True, False]:
        res = str(expr)
        renderer.render(res)
    else:
        res = sp.simplify(expr)
        renderer.render(f'${sp.latex(expr)} = {sp.latex(res)}$')


def evaluate(expr: sp_obj) -> sp_obj:
    """ Evaluates the expression. """
    return expr if expr in [True, False] else expr.evalf()


def average(nums: str) -> float:
    """ Calculates the average. """
    nums = [float(num) for num in nums.split(' ')]
    return round(sum(nums) / len(nums), 4)
