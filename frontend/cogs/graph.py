""" Code for graph commands. """
from discord import app_commands, Interaction
from discord.ext import commands

from backend import plotter
from frontend.views import Answer
from frontend.utils import graph_single_func, graph_multiple_func
from frontend.utils import CharLim1, CharLim25


class Graph(commands.GroupCog, group_name='graph'):
    """ Represents a collection of graph commands. """

    single = app_commands.Group(name='single',
                                description='Plot a graph.')

    multiple = app_commands.Group(name='multiple',
                                  description='Plot two graphs.')

    parametric = app_commands.Group(name='parametric',
                                    description='Plot a parametric graph.')

    # FUNCTIONS ---------------------------------------------------------------

    @single.command()
    async def function(self,
                       itx: Interaction,
                       func: CharLim25,
                       var: CharLim1,
                       dom: CharLim25 = None,
                       ran: CharLim25 = None) -> None:
        """ Plots a function.

        :param itx: the Discord interaction
        :param func: the function to plot, e.g. f(x)=x^3
        :param var: the variable, e.g. x
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        await graph_single_func(itx, func, var, dom, ran)

    @multiple.command()
    async def functions(self,
                        itx: Interaction,
                        f1: CharLim25,
                        f2: CharLim25,
                        var: CharLim1,
                        dom: CharLim25 = None,
                        ran: CharLim25 = None) -> None:
        """ Plots two functions.

        :param itx: the Discord interaction
        :param f1: the first function to plot, e.g. f(x)=e^x
        :param f2: the second function to plot, e.g. f^{-1}(x)=ln(x)
        :param var: the variable, e.g. x
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        await graph_multiple_func(itx, f1, f2, var, dom, ran)

    # RELATIONS ---------------------------------------------------------------

    @single.command()
    async def relation(self,
                       itx: Interaction,
                       relation: CharLim25,
                       domain: CharLim25 = None,
                       range: CharLim25 = None) -> None:
        """ Plots a relation.

        :param itx: the Discord interaction
        :param relation: the relation to plot, e.g.  x^2+y^2=9
        :param domain: the domain, e.g. -5,5
        :param range: the range, e.g. -5,5
        """
        output_str = plotter.plot_single_rel(relation, domain, range)
        await Answer(itx, output_str).send()

    @multiple.command()
    async def relations(self,
                        itx: Interaction,
                        rel1: CharLim25,
                        rel2: CharLim25,
                        dom: CharLim25 = None,
                        ran: CharLim25 = None) -> None:
        """ Plots two relations.

        :param itx: the Discord interaction
        :param rel1: the first relation to plot, e.g. x^2+y^2=9
        :param rel2: the second relation to plot, e.g. x^2+y^2=16
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        output_str = plotter.plot_multiple_rel(rel1, rel2, dom, ran)
        await Answer(itx, output_str).send()

    # 3D ----------------------------------------------------------------------

    @single.command(name='3d')
    async def expression(self,
                         itx: Interaction,
                         expression: CharLim25,
                         domain: CharLim25 = None,
                         range: CharLim25 = None) -> None:
        """ Plots an expression in 3D.

        :param itx: the Discord interaction
        :param expression: the expression to plot, e.g.  sin(x*y)
        :param domain: the domain, e.g. -5,5
        :param range: the range, e.g. -5,5
        """
        output_str = plotter.plot_single_3d(expression, domain, range)
        await Answer(itx, output_str).send()

    @multiple.command(name='3d')
    async def expressions(self,
                          itx: Interaction,
                          expr1: CharLim25,
                          expr2: CharLim25,
                          dom: CharLim25 = None,
                          ran: CharLim25 = None) -> None:
        """ Plots two expressions in 3D.

        :param itx: the Discord interaction
        :param expr1: the first expression to plot, e.g. x*y
        :param expr2: the second expression to plot, e.g. -x*y
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        output_str = plotter.plot_multiple_3d(expr1, expr2, dom, ran)
        await Answer(itx, output_str).send()

    # PARAMETRIC --------------------------------------------------------------

    @parametric.command()
    async def equations(self,
                        itx: Interaction,
                        xt: CharLim25,
                        yt: CharLim25,
                        start: CharLim25,
                        end: CharLim25) -> None:
        """ Plot a pair of parametric equations.

        :param itx: the Discord interaction
        :param xt: the equation for x in terms of t, e.g. sin(t)
        :param yt: the equation for y in terms of t, e.g. cos(t)
        :param start: the start time, e.g. 0
        :param end: the end time, e.g. 5
        """
        output_str = plotter.plot_parametric(xt, yt, start, end)
        await Answer(itx, output_str).send()


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Graph())
