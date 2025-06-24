import sympy as sp

from scripts.parser import parse_eq, parse_var
from scripts.renderer import render_tex
from scripts.printer import make_pretty
from scripts.utils import Result, Error, Response


def solve_linear_system(args: dict) -> Response:
    try:
        raw_eqs = args['eqs']
        raw_vars = args['vars']
        eqs = [parse_eq(eq) for eq in raw_eqs]
        vars = [parse_var(var) for var in raw_vars]
        res = sp.linsolve(eqs, vars)
        pretty = {
            "eqs": [make_pretty(eq) for eq in eqs],
            "vars": [make_pretty(var) for var in vars]
        }
        if res == sp.EmptySet:
            image = render_tex("$\\text{No solution}$")
            answer = [make_pretty(res)]
        else:
            sols = list(res.args[0])  # type: ignore
            tex = ""
            for i in range(len(sols)):
                tex += f"{vars[i]} = {sp.latex(sols[i])}"
                if i < len(sols)-1:
                    tex += '|'  # Will be converted to ", "
            image = render_tex(f"${tex}$")
            answer = [make_pretty(sol) for sol in sols]
        return Result(pretty, image, answer)
    except Exception as e:
        return Error(name=type(e).__name__, message=str(e))
