""" Code for graph commands. """

import discord
from discord import app_commands
from discord.ext import commands

from backend import plotter
from modules import transform
from modules import answer
from modules.bot import DAS
from modules.transform import DEFAULT_LIMIT, DEFAULT_ORIGIN


class Graph(commands.GroupCog, group_name='graph'):
    """ Represents a collection of graph commands. """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot

    single = app_commands.Group(name='single',
                                description='Plot a graph.')

    @single.command()
    async def function(self,
                       itx: discord.Interaction,
                       func: transform.Function,
                       var: app_commands.Range[str, 1, 1],
                       dom: transform.Limit = DEFAULT_LIMIT,
                       ran: transform.Limit = None) -> None:
        """ Plots a function.

        :param itx: the Discord interaction
        :param func: the function to use, e.g. f(x)=x^3
        :param var: the variable to use, e.g. x
        :param dom: the domain to use, e.g. (-5, 5)
        :param ran: the range to use, e.g. (-5, 5)
        """
        plotter.plot_single_function(func, var, dom, ran)
        await answer.send(
            itx,
            inputs=f"Function: `{func}`\n" +
                   (f"Limits: `{var} ∈ {dom}`, `{func.name} ∈ {ran}`"
                    if ran else f"Domain: `{var} ∈ {dom}`")
        )

    @single.command()
    async def relation(self,
                       itx: discord.Interaction,
                       relation: transform.Relation,
                       domain: transform.Limit = DEFAULT_LIMIT,
                       range: transform.Limit = DEFAULT_LIMIT) -> None:
        """ Plots a relation.

        :param itx: the Discord interaction
        :param relation: the function to use, e.g.  x^2+y^2=3^2
        :param domain: the domain to use, e.g. (-5, 5)
        :param range: the range to use, e.g. (-5, 5)
        """
        plotter.plot_single_relation(relation, domain, range)
        await answer.send(
            itx,
            inputs=f"Relation: `{relation}`\n"
                   f"Limits: `x ∈ {domain}`, `y ∈ {range}`"
        )

    @single.command(name='3d')
    async def expression(self,
                         itx: discord.Interaction,
                         expression: transform.Expression,
                         domain: transform.Limit = DEFAULT_LIMIT,
                         range: transform.Limit = DEFAULT_LIMIT) -> None:
        """ Plots an expression in 3D.

        :param itx: the Discord interaction
        :param expression: the expression to use, e.g.  sin(x*y)
        :param domain: the domain to use, e.g. (-5, 5)
        :param range: the range to use, e.g. (-5, 5)
        """
        plotter.plot_single_3d(expression, domain, range)
        await answer.send(
            itx,
            inputs=f"Expression: `{expression}`\n"
                   f"Limits: `x ∈ {domain}`, `y ∈ {range}`"
        )

    @single.command()
    async def vector(self,
                     itx: discord.Interaction,
                     vector: transform.Vector,
                     origin: transform.Vector = DEFAULT_ORIGIN) -> None:
        """ Plots a vector.

        :param itx: the discord Interaction
        :param vector: the directional vector to use, e.g. (5, 1)
        :param origin: the original location of the vector, e.g. (0, 0)
        """
        plotter.plot_single_vector(vector, origin)
        await answer.send(
            itx,
            inputs=f"Vector: `{vector}`\n"
                   f"Origin: `{origin}`"
        )

    multiple = app_commands.Group(name='multiple',
                                  description='Plot two graphs.')

    @multiple.command()
    async def functions(self,
                        itx: discord.Interaction,
                        f1: transform.Function,
                        f2: transform.Function,
                        var: app_commands.Range[str, 1, 1],
                        dom: transform.Limit = DEFAULT_LIMIT,
                        ran: transform.Limit = None) -> None:
        """ Plots two functions.

        :param itx: the Discord interaction
        :param f1: the first function to use, e.g. f(x)=e^x
        :param f2: the second function to use, e.g. f^{-1}(x)=ln(x)
        :param var: the variable to use, e.g. x
        :param dom: the domain to use, e.g. (-5, 5)
        :param ran: the range to use, e.g. (-5, 5)
        """
        if f1.name == 'f(x)' and f2.name == 'f(x)':
            # Update function names if they are both the same default one.
            f1 = transform.Function(name='f1(x)', expr=f1.expr)
            f2 = transform.Function(name='f2(x)', expr=f2.expr)
        plotter.plot_multiple_functions(f1, f2, var, dom, ran)
        await answer.send(
            itx,
            inputs=f"Functions: `{f1}`, `{f2}`\n" +
                   (f"Limits: `{var} ∈ {dom}`, `{f1.name},{f2.name} ∈ {ran}`"
                    if ran else f"Domain: `{var} ∈ {dom}`")
        )

    @multiple.command()
    async def relations(self,
                        itx: discord.Interaction,
                        rel1: transform.Relation,
                        rel2: transform.Relation,
                        dom: transform.Limit = DEFAULT_LIMIT,
                        ran: transform.Limit = DEFAULT_LIMIT) -> None:
        """ Plots two relations.

        :param itx: the Discord interaction
        :param rel1: the first relation to use, e.g. x^2+y^2=9
        :param rel2: the second relation to use, e.g. x^2+y^2=16
        :param dom: the domain to use, e.g. (-5, 5)
        :param ran: the range to use, e.g. (-5, 5)
        """
        plotter.plot_multiple_relations(rel1, rel2, dom, ran)
        await answer.send(
            itx,
            inputs=f"Relations: `{rel1}`, `{rel2}`\n"
                   f"Limits: `x ∈ {dom}`, `y ∈ {ran}`"
        )

    @multiple.command(name='3d')
    async def expressions(self,
                          itx: discord.Interaction,
                          expr1: transform.Expression,
                          expr2: transform.Expression,
                          dom: transform.Limit = DEFAULT_LIMIT,
                          ran: transform.Limit = DEFAULT_LIMIT) -> None:
        """ Plots two expressions in 3D.

        :param itx: the Discord interaction
        :param expr1: the first expression to use, e.g. x*y
        :param expr2: the second expression to use, e.g. -x*y
        :param dom: the domain to use, e.g. (-5, 5)
        :param ran: the range to use, e.g. (-5, 5)
        """
        plotter.plot_multiple_3d(expr1, expr2, dom, ran)
        await answer.send(
            itx,
            inputs=f"Expressions: `{expr1}`, `{expr2}`\n"
                   f"Limits: `x ∈ {dom}`, `y ∈ {ran}`"
        )

    @multiple.command()
    async def vectors(self,
                      itx: discord.Interaction,
                      v1: transform.Vector,
                      v2: transform.Vector,
                      o1: transform.Vector = DEFAULT_ORIGIN,
                      o2: transform.Vector = DEFAULT_ORIGIN) -> None:
        """ Plots two vectors.

        :param itx: the discord Interaction
        :param v1: the first directional vector, e.g. (5, 1)
        :param v2: the second directional vector, e.g. (-3, 2)
        :param o1: the original location of the first vector, e.g. (0, 0)
        :param o2: the original location of the second vector, e.g. (0, 0)
        """

        plotter.plot_multiple_vectors(v1, v2, o1, o2)
        await answer.send(
            itx,
            inputs=f"Vectors: `{v1}`, `{v2}`\n"
                   f"Origins: `{o1}`, `{o2}`"
        )

    parametric = app_commands.Group(name='parametric',
                                    description='Plot a parametric graph.')

    @parametric.command()
    async def equations(self,
                        itx: discord.Interaction,
                        xt: transform.Function,
                        yt: transform.Function,
                        start: float,
                        end: float) -> None:
        """ Plot a pair of parametric equations.

        :param itx: the Discord interaction
        :param xt: the equation for x in terms of t, i.e. x(t)=...
        :param yt: the equation for y in terms of t, i.e. y(t)=...
        :param start: the start time, e.g. 0
        :param end: the end time, e.g. 5
        """
        plotter.plot_parametric_equations(xt, yt, start, end)
        await answer.send(
            itx,
            inputs=f"Equations: `x(t) = {xt.expr}`, `y(t) = {yt.expr}`\n"
                   f"Restriction: `t ∈ [{start}, {end}]`"
        )


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Graph(bot), guild=bot.test_guild)
