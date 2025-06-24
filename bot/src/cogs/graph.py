""" Code for graph commands. """
from discord import app_commands, Interaction
from discord.ext import commands

from src.api import send_request
from src.views import Answer
from src.utils import graph_single_func, graph_multiple_func
from src.utils import CharLim1, CharLim25


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
class Graph(commands.GroupCog, group_name='graph'):
    """ Represents a collection of graph commands. """
    DEFAULT_DOMAIN = '-5,5'
    DEFAULT_RANGE = '-5,5'

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
                       dom: CharLim25 = DEFAULT_DOMAIN,
                       ran: CharLim25 | None = None) -> None:
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
                        func1: CharLim25,
                        func2: CharLim25,
                        var: CharLim1,
                        dom: CharLim25 = DEFAULT_DOMAIN,
                        ran: CharLim25 | None = None) -> None:
        """ Plots two functions.

        :param itx: the Discord interaction
        :param func1: the first function to plot, e.g. f(x)=e^x
        :param func2: the second function to plot, e.g. f^{-1}(x)=ln(x)
        :param var: the variable, e.g. x
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        await graph_multiple_func(itx, func1, func2, var, dom, ran)

    # RELATIONS ---------------------------------------------------------------

    @single.command()
    async def relation(self,
                       itx: Interaction,
                       relation: CharLim25,
                       domain: CharLim25 = DEFAULT_DOMAIN,
                       range: CharLim25 = DEFAULT_RANGE) -> None:
        """ Plots a relation.

        :param itx: the Discord interaction
        :param relation: the relation to plot, e.g.  x^2+y^2=9
        :param domain: the domain, e.g. -5,5
        :param range: the range, e.g. -5,5
        """
        res = await send_request('/graph-rel-single', {'rel': relation,
                                                       'dom': domain,
                                                       'ran': range})
        out = (f"Relation: "
               f"`{res['pretty']['rel']}`\n"
               f"Limits: "
               f"`x∈{res['pretty']['dom']}`, "
               f"`y∈{res['pretty']['ran']}`")
        await Answer(itx, out, res['image']).send()

    @multiple.command()
    async def relations(self,
                        itx: Interaction,
                        rel1: CharLim25,
                        rel2: CharLim25,
                        dom: CharLim25 = DEFAULT_DOMAIN,
                        ran: CharLim25 = DEFAULT_RANGE) -> None:
        """ Plots two relations.

        :param itx: the Discord interaction
        :param rel1: the first relation to plot, e.g. x^2+y^2=9
        :param rel2: the second relation to plot, e.g. x^2+y^2=16
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        res = await send_request('/graph-rel-multiple', {'rel1': rel1,
                                                         'rel2': rel2,
                                                         'dom': dom,
                                                         'ran': ran})
        out = (f"Relations: "
               f"`{res['pretty']['rel1']}`, "
               f"`{res['pretty']['rel2']}`\n"
               f"Limits: "
               f"`x∈{res['pretty']['dom']}`, "
               f"`y∈{res['pretty']['ran']}`")
        await Answer(itx, out, res['image']).send()

    # 3D ----------------------------------------------------------------------

    @single.command(name='3d')
    async def expression(self,
                         itx: Interaction,
                         expression: CharLim25,
                         domain: CharLim25 = DEFAULT_DOMAIN,
                         range: CharLim25 = DEFAULT_RANGE) -> None:
        """ Plots an expression in 3D.

        :param itx: the Discord interaction
        :param expression: the expression to plot, e.g. sin(x*y)
        :param domain: the domain, e.g. -5,5
        :param range: the range, e.g. -5,5
        """
        res = await send_request('/graph-expr-single', {'expr': expression,
                                                        'dom': domain,
                                                        'ran': range})
        out = (f"Expression: "
               f"`{res['pretty']['expr']}`\n"
               f"Limits: "
               f"`x∈{res['pretty']['dom']}`, "
               f"`y∈{res['pretty']['ran']}`")
        await Answer(itx, out, res['image']).send()

    @multiple.command(name='3d')
    async def expressions(self,
                          itx: Interaction,
                          expr1: CharLim25,
                          expr2: CharLim25,
                          dom: CharLim25 = DEFAULT_DOMAIN,
                          ran: CharLim25 = DEFAULT_RANGE) -> None:
        """ Plots two expressions in 3D.

        :param itx: the Discord interaction
        :param expr1: the first expression to plot, e.g. x*y
        :param expr2: the second expression to plot, e.g. -x*y
        :param dom: the domain, e.g. -5,5
        :param ran: the range, e.g. -5,5
        """
        res = await send_request('/graph-expr-multiple', {'expr1': expr1,
                                                          'expr2': expr2,
                                                          'dom': dom,
                                                          'ran': ran})
        out = (f"Expressions: "
               f"`{res['pretty']['expr1']}`, "
               f"`{res['pretty']['expr2']}`\n"
               f"Limits: "
               f"`x∈{res['pretty']['dom']}`, "
               f"`y∈{res['pretty']['ran']}`")
        await Answer(itx, out, res['image']).send()

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
        res = await send_request('/graph-parametric', {'xt': xt,
                                                       'yt': yt,
                                                       't_start': start,
                                                       't_end': end})
        out = (f"Equations: "
               f"`x(t)={res['pretty']['xt']}`, "
               f"`y(t)={res['pretty']['yt']}`\n"
               f"Restriction: "
               f"`t∈[{res['pretty']['t_start']},"
               f"{res['pretty']['t_end']}]`")
        await Answer(itx, out, res['image']).send()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Graph())
