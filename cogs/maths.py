""" Code for math commands. """

import typing
import discord
from discord import app_commands
from discord.ext import commands

from backend import calculator, renderer
from modules import transform
from modules import answer
from modules.buttons import Single, Multiple, Delete, Confirm
from modules.bot import DAS


class Maths(commands.Cog):
    """ Represents a collection of math commands. """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot

    @app_commands.command()
    async def display(self,
                      itx: discord.Interaction,
                      text: app_commands.Range[str, 1, 100]) -> None:
        """ Displays math text as an image.

        :param itx: the Discord interaction
        :param text: the text to display, e.g. f(x)=2x+2
        """
        renderer.render(f"${text}$")
        await answer.send(
            itx,
            inputs=f"Input: `{text}`",
            btns=[Delete(), Confirm()]
        )

    @app_commands.command()
    async def limit(self,
                    itx: discord.Interaction,
                    function: transform.Function,
                    variable: app_commands.Range[str, 1, 1],
                    coordinate: transform.Value) -> None:
        """ Finds the limit of a function at a coordinate.

        :param itx: the Discord interaction
        :param function: the function to use, e.g. f(x)=x^3
        :param variable: the variable to use, e.g. x
        :param coordinate: the coordinate to use (type oo for infinity)
        """
        value = calculator.limit(function, variable, coordinate)
        await answer.send(
            itx,
            inputs=f"Function: `{function}`\n"
                   f"Limit: `{value}`",
            btns=[Single(function, variable), Delete(), Confirm()]
        )

    @app_commands.command()
    async def derive(self,
                     itx: discord.Interaction,
                     function: transform.Function,
                     variable: app_commands.Range[str, 1, 1]) -> None:
        """ Derives a function with respect to a variable.

        :param itx: the Discord interaction
        :param function: the function to use, e.g. f(x)=x^3
        :param variable: the variable to use, e.g. x
        """
        original = transform.Function(
            name=f"f({variable})",
            expr=function.expr
        )
        derivative = transform.Function(
            name=f"f'({variable})",
            expr=calculator.derive(function, variable)
        )
        await answer.send(
            itx,
            inputs=f"Function: `{original}`\n"
                   f"Derivative: `{derivative}`",
            btns=[Multiple(original, derivative, variable), Delete(), Confirm()]
        )

    @app_commands.command()
    async def integrate(self,
                        itx: discord.Interaction,
                        func: transform.Function,
                        var: app_commands.Range[str, 1, 1],
                        lt: transform.Value = None,
                        ut: transform.Value = None) -> None:
        """ Integrates a function with respect to a variable.

        :param itx: the Discord interaction
        :param func: the function to use, e.g. f(x)=x^3
        :param var: the variable to use, e.g. x
        :param lt: the lower terminal, e.g. 1
        :param ut: the upper terminal, e.g. 5
        """
        original = transform.Function(name=f"f({var})", expr=func.expr)
        indefinite, definite = calculator.integrate(func, var, lt, ut)
        integral = transform.Function(name=f"F({var})", expr=indefinite)
        await answer.send(
            itx,
            inputs=f"Function: `{original}`\n"
                   f"Integral: `{integral}`",
            btns=[Multiple(original, integral, var), Delete(), Confirm()]
        )

    @app_commands.command()
    async def solve(self,
                    itx: discord.Interaction,
                    equation: transform.Equation,
                    variable: app_commands.Range[str, 1, 1],
                    domain: typing.Literal['real', 'complex'] = 'real') -> None:
        """ Solves an equation with respect to a variable and domain.
        
        :param itx: the Discord interaction
        :param equation: the equation to use, e.g. x^2=4
        :param variable: the variable to solve for, e.g. x
        :param domain: the domain to solve over, e.g. real
        """
        calculator.solve(equation, variable, domain)
        await answer.send(itx, inputs=f"Equation: `{equation}`")

    @app_commands.command()
    async def linsolve(self,
                       itx: discord.Interaction,
                       eq1: transform.Equation,
                       eq2: transform.Equation,
                       var1: app_commands.Range[str, 1, 1],
                       var2: app_commands.Range[str, 1, 1]) -> None:
        """ Solves a pair of linear equations for two variables.

        :param itx: the Discord interaction
        :param eq1: the first equation to use, e.g. x + y = 2
        :param eq2: the second equation to use, e.g. 2x + y = 4
        :param var1: the first variable to solve for, e.g. x
        :param var2: the second variable to solve for, e.g y
        """
        calculator.linsolve(eq1, eq2, var1, var2)
        await answer.send(itx, inputs=f"Equations: `{eq1}`, `{eq2}`")

    @app_commands.command()
    async def expand(self,
                     itx: discord.Interaction,
                     expression: transform.Expression) -> None:
        """ Expands an expression.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g. 2(x+1)
        """
        calculator.expand(expression)
        await answer.send(itx, inputs=f"Expression: `{expression}`")

    @app_commands.command()
    async def factor(self,
                     itx: discord.Interaction,
                     expression: transform.Expression) -> None:
        """ Factors an expression.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g. 2x+2
        """
        calculator.factor(expression)
        await answer.send(itx, inputs=f"Expression: `{expression}`")

    @app_commands.command()
    async def simplify(self,
                       itx: discord.Interaction,
                       expression: transform.Expression) -> None:
        """ Simplifies an expression.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g. cos^2(x)+sin^2(x)
        """
        calculator.simplify(expression)
        await answer.send(itx, inputs=f"Expression: `{expression}`")

    @app_commands.command()
    async def calculate(self,
                        itx: discord.Interaction,
                        expression: transform.Expression) -> None:
        """ Evaluates an expression.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g. 1+1
        """
        await itx.response.send_message(
            f"🧮**  |  {itx.user.display_name}**, "
            f"answer is `{calculator.evaluate(expression)}`!"
        )

    @app_commands.command()
    async def average(self,
                      itx: discord.Interaction,
                      numbers: str) -> None:
        """ Calculates the average of a list of numbers.

        :param itx: the Discord interaction
        :param numbers: the list of numbers separated by spaces, e.g. 1 2 3 4
        """
        await itx.response.send_message(
            f"🧮**  |  {itx.user.display_name}**, "
            f"average is `{calculator.average(numbers)}`!"
        )


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Maths(bot), guild=bot.test_guild)
