""" Code for math commands. """
from typing import Literal

from discord import app_commands, Interaction
from discord.ext import commands

from src.api import send_request
from src.views import Answer
from src.buttons import MultipleGraph, SingleGraph
from src.utils import CharLim1, CharLim50, allow_anywhere


class Maths(commands.Cog):
    """ Represents a collection of math commands. """

    @app_commands.command()
    @allow_anywhere
    async def display(self, itx: Interaction, text: CharLim50) -> None:
        """ Renders math text as an image.

        :param itx: the Discord interaction
        :param text: the text to render, e.g. How to solve $x^2=4$?
        """
        res = await send_request('/display', {'text': text})
        out = f"Input: `{text}`"
        await Answer(itx, out, res['image']).send()

    # ALGEBRA ------------------------------------------------------------------

    @app_commands.command()
    @allow_anywhere
    async def calculate(self, itx: Interaction, expression: CharLim50) -> None:
        """ Evaluates an expression.

        :param itx: the Discord interaction
        :param expression: the expression to evaluate, e.g. sin(90deg), cos(pi)
        """
        res = await send_request('/evaluate', {'expr': expression})
        out = (f"Expression: `{res['pretty']['expr']}`\n"
               f"Evaluated: `{res['answer']}`")
        await Answer(itx, out, res['image']).send()

    @app_commands.command()
    @allow_anywhere
    async def expand(self, itx: Interaction, expression: str) -> None:
        """ Expands an expression.

        :param itx: the Discord interaction
        :param expression: the expression to expand, e.g. 2(x+1)
        """
        res = await send_request('/expand', {'expr': expression})
        out = (f"Expression: `{res['pretty']['expr']}`\n"
               f"Expanded: `{res['answer']}`")
        await Answer(itx, out, res['image']).send()

    @app_commands.command()
    @allow_anywhere
    async def factor(self, itx: Interaction, expression: CharLim50) -> None:
        """ Factors an expression.

        :param itx: the Discord interaction
        :param expression: the expression to factor, e.g. 2x+2
        """
        res = await send_request('/factor', {'expr': expression})
        out = (f"Expression: `{res['pretty']['expr']}`\n"
               f"Factored: `{res['answer']}`")
        await Answer(itx, out, res['image']).send()

    @app_commands.command()
    @allow_anywhere
    async def simplify(self, itx: Interaction, expression: CharLim50) -> None:
        """ Simplifies an expression.

        :param itx: the Discord interaction
        :param expression: the expression to simplify, e.g. cos^2(x)+sin^2(x)
        """
        res = await send_request('/simplify', {'expr': expression})
        out = (f"Expression: `{res['pretty']['expr']}`\n"
               f"Simplified: `{res['answer']}`")
        await Answer(itx, out, res['image']).send()

    # # CALCULUS ----------------------------------------------------------------

    @app_commands.command()
    @allow_anywhere
    async def derive(self,
                     itx: Interaction,
                     expression: CharLim50,
                     variable: CharLim1) -> None:
        """ Derives an expression with respect to a variable.

        :param itx: the Discord interaction
        :param expression: the expression to derive, e.g. x^2
        :param variable: the variable to derive with respect to, e.g. x
        """
        res = await send_request('/derive', {'expr': expression,
                                             'var': variable})
        out = (f"Original: `{res['pretty']['expr']}`\n"
               f"Derivative: `{res['answer']}`")
        btn = MultipleGraph(f"f({variable})={res['pretty']['expr']}",
                            f"f'({variable})={res['answer']}",
                            variable)
        await Answer(itx, out, res['image'], btns=[btn]).send()

    @app_commands.command()
    @allow_anywhere
    async def integrate(self,
                        itx: Interaction,
                        expr: CharLim50,
                        var: CharLim1,
                        lt: CharLim50 | None = None,
                        ut: CharLim50 | None = None) -> None:
        """ Integrates an expression with respect to a variable.

        :param itx: the Discord interaction
        :param expr: the expression to integrate, e.g. x^2
        :param var: the variable to integrate with respect to, e.g. x
        :param lt: the lower terminal, e.g. 1
        :param ut: the upper terminal, e.g. 5
        """
        res = await send_request('/integrate-indefinite', {'expr': expr,
                                                           'var': var})
        out = (f"Original: `{res['pretty']['expr']}`\n"
               f"Indefinite Integral: `{res['answer']}`")
        image = res['image']
        if lt is not None and ut is not None:
            res2 = await send_request('/integrate-definite', {'expr': expr,
                                                              'var': var,
                                                              'lt': lt,
                                                              'ut': ut})
            out += f"\nDefinite Integral: `{res2['answer']}`"
            image = res2['image']
        btn = MultipleGraph(func1=f"f({var})={expr}",
                            func2=f"F({var})={res['answer']}",
                            var=var)
        await Answer(itx, out, image, btns=[btn]).send()

    @app_commands.command()
    @allow_anywhere
    async def limit(self,
                    itx: Interaction,
                    expression: CharLim50,
                    variable: CharLim1,
                    coordinate: CharLim50) -> None:
        """ Finds the limit of an expression at a coordinate.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g. e^x
        :param variable: the variable to use, e.g. x
        :param coordinate: the coordinate to use (type oo for infinity)
        """
        res = await send_request('/limit', {'expr': expression,
                                            'var': variable,
                                            'val': coordinate})
        out = f"Limit: `{res['answer']}`"
        btn = SingleGraph(expression, variable)
        await Answer(itx, out, res['image'], btns=[btn]).send()

    # SOLVERS -----------------------------------------------------------------

    @app_commands.command()
    @allow_anywhere
    async def solve(self,
                    itx: Interaction,
                    equation: CharLim50,
                    variable: CharLim1,
                    domain: Literal['real', 'complex'] = 'real') -> None:
        """ Solves an equation with respect to a variable and domain.

        :param itx: the Discord interaction
        :param equation: the equation to use, e.g. x^2=4
        :param variable: the variable to solve for, e.g. x
        :param domain: the domain to solve over, e.g. real
        """
        res = await send_request('/solve', {'eq': equation,
                                            'var': variable,
                                            'dom': domain})
        sols_str = ', '.join(f'`{sol}`' for sol in res['answer'])
        out = (f"Equation: `{res['pretty']['eq']}`\n"
               f"Solution: {sols_str}")
        await Answer(itx, out, res['image']).send()

    @app_commands.command()
    @allow_anywhere
    async def linsolve(self,
                       itx: Interaction,
                       eq1: CharLim50,
                       eq2: CharLim50,
                       var1: CharLim1,
                       var2: CharLim1,
                       eq3: CharLim50 | None = None,
                       var3: CharLim1 | None = None) -> None:
        """ Solves up to three linear equations for up to three variables.

        :param itx: the Discord interaction
        :param eq1: the first equation to use, e.g. x + y = 2
        :param eq2: the second equation to use, e.g. 2x + y = 4
        :param var1: the first variable to solve for, e.g. x
        :param var2: the second variable to solve for, e.g y
        :param var3: the third variable to solve for
        :param eq3: the third equation to solve for
        """
        eqs = [eq1, eq2] + ([eq3] if eq3 is not None else [])
        vars = [var1, var2] + ([var3] if var3 is not None else [])
        res = await send_request('/linsolve', {'eqs': eqs, 'vars': vars})
        eqs_str = ', '.join(f'`{eq}`' for eq in res['pretty']['eqs'])
        sols_str = ', '.join(f'`{var}={sol}`'
                             for var, sol in zip(vars, res['answer']))
        out = (f"Equations: {eqs_str}\nSolutions: {sols_str}")
        await Answer(itx, out, res['image']).send()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Maths())
