""" Code for math commands. """
from typing import Literal
from discord import app_commands, Interaction
from discord.ext import commands

from backend import calculator
from frontend.views import Answer
from frontend.buttons import MultipleGraph, SingleGraph
from frontend.utils import CharLim1, CharLim25, CharLim50, allow_anywhere


class Maths(commands.Cog):
    """ Represents a collection of math commands. """

    @app_commands.command()
    @allow_anywhere
    async def display(self, itx: Interaction, text: CharLim50) -> None:
        """ Renders math text as an image.

        :param itx: the Discord interaction
        :param text: the text to render, e.g. How to solve $x^2=4$?
        """
        _, output_str = calculator.display(text)
        await Answer(itx, output_str).send()

    # SIMPLIFICATION ----------------------------------------------------------

    @app_commands.command()
    @allow_anywhere
    async def expand(self, itx: Interaction, expression: str) -> None:
        """ Expands an expression.

        :param itx: the Discord interaction
        :param expression: the expression to expand, e.g. 2(x+1)
        """
        _, output_str = calculator.expand(expression)
        await Answer(itx, output_str).send()

    @app_commands.command()
    @allow_anywhere
    async def factor(self, itx: Interaction, expression: CharLim25) -> None:
        """ Factors an expression.

        :param itx: the Discord interaction
        :param expression: the expression to factor, e.g. 2x+2
        """
        _, output_str = calculator.factor(expression)
        await Answer(itx, output_str).send()

    @app_commands.command()
    @allow_anywhere
    async def simplify(self, itx: Interaction, expression: CharLim25) -> None:
        """ Simplifies an expression.

        :param itx: the Discord interaction
        :param expression: the expression to simplify, e.g. cos^2(x)+sin^2(x)
        """
        _, output_str = calculator.simplify(expression)
        await Answer(itx, output_str).send()

    @app_commands.command()
    @allow_anywhere
    async def calculate(self, itx: Interaction, expression: CharLim25) -> None:
        """ Evaluates an expression.

        :param itx: the Discord interaction
        :param expression: the expression to evaluate, e.g. sin(90deg), cos(pi)
        """
        _, output_str = calculator.evaluate(expression)
        await Answer(itx, output_str).send()

    # CALCULUS ----------------------------------------------------------------

    @app_commands.command()
    @allow_anywhere
    async def derive(self,
                     itx: Interaction,
                     expression: CharLim25,
                     variable: CharLim1) -> None:
        """ Derives an expression with respect to a variable.

        :param itx: the Discord interaction
        :param expression: the expression to derive, e.g. x^2
        :param variable: the variable to derive with respect to, e.g. x
        """
        derivative, output_str = calculator.derive(expression, variable)
        graph_btn = MultipleGraph(f1=f"f({variable})={expression}",
                                  f2=f"f'({variable})={derivative}",
                                  var=variable)
        await Answer(itx, output_str, btns=[graph_btn]).send()

    @app_commands.command()
    @allow_anywhere
    async def integrate(self,
                        itx: Interaction,
                        expr: CharLim25,
                        var: CharLim1,
                        lt: CharLim25 = None,
                        ut: CharLim25 = None) -> None:
        """ Integrates an expression with respect to a variable.

        :param itx: the Discord interaction
        :param expr: the expression to integrate, e.g. x^2
        :param var: the variable to integrate with respect to, e.g. x
        :param lt: the lower terminal, e.g. 1
        :param ut: the upper terminal, e.g. 5
        """
        indefinite, output_str = calculator.integrate_indefinite(expr, var)
        if lt is not None and ut is not None:
            _, output_str2 = calculator.integrate_definite(expr, var, lt, ut)
            output_str += '\n' + output_str2
        graph_btn = MultipleGraph(f1=f"f({var})={expr}",
                                  f2=f"F({var})={indefinite}",
                                  var=var)
        await Answer(itx, output_str, btns=[graph_btn]).send()

    @app_commands.command()
    @allow_anywhere
    async def limit(self,
                    itx: Interaction,
                    expression: CharLim25,
                    variable: CharLim1,
                    coordinate: CharLim25) -> None:
        """ Finds the limit of an expression at a coordinate.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g. e^x
        :param variable: the variable to use, e.g. x
        :param coordinate: the coordinate to use (type oo for infinity)
        """
        _, output_str = calculator.limit(expression, variable, coordinate)
        graph_btn = SingleGraph(expression, variable)
        await Answer(itx, output_str, btns=[graph_btn]).send()

    # SOLVERS -----------------------------------------------------------------

    @app_commands.command()
    @allow_anywhere
    async def solve(self,
                    itx: Interaction,
                    equation: CharLim25,
                    variable: CharLim1,
                    domain: Literal['real', 'complex'] = 'real') -> None:
        """ Solves an equation with respect to a variable and domain.

        :param itx: the Discord interaction
        :param equation: the equation to use, e.g. x^2=4
        :param variable: the variable to solve for, e.g. x
        :param domain: the domain to solve over, e.g. real
        """
        _, output_str = calculator.solve(equation, variable, domain)
        await Answer(itx, output_str).send()

    @app_commands.command()
    @allow_anywhere
    async def linsolve(self,
                       itx: Interaction,
                       eq1: CharLim25,
                       eq2: CharLim25,
                       var1: CharLim1,
                       var2: CharLim1,
                       eq3: CharLim25 = None,
                       var3: CharLim1 = None) -> None:
        """ Solves up to three linear equations for up to three variables.

        :param itx: the Discord interaction
        :param eq1: the first equation to use, e.g. x + y = 2
        :param eq2: the second equation to use, e.g. 2x + y = 4
        :param var1: the first variable to solve for, e.g. x
        :param var2: the second variable to solve for, e.g y
        :param var3: the third variable to solve for
        :param eq3: the third equation to solve for
        """
        _, output_str = calculator.linsolve([eq1, eq2, eq3], [var1, var2, var3])
        await Answer(itx, output_str).send()


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Maths())
