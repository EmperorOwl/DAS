import discord
from abc import ABC

from frontend.utils import graph_single_func, graph_multiple_func


class Graph(ABC, discord.ui.Button):
    """ Represents a graph button. """
    EMOJI = '📈'
    STYLE = discord.ButtonStyle.primary

    def __init__(self) -> None:
        """ Creates a button. """
        super().__init__(emoji=self.EMOJI, style=self.STYLE)

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        itx.extras = {'is_graph': True}  # For stat collecting
        await self.view.msg.edit(view=self.view.clear_items())


class SingleGraph(Graph):
    """ Represents a button that plots one graph. """

    def __init__(self, func: str, var: str) -> None:
        """ Creates a button. """
        super().__init__()
        self.func = func
        self.var = var

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        await super().callback(itx)
        await graph_single_func(itx,
                                self.func,
                                self.var,
                                dom=None,
                                ran=None)
        self.view.stop()


class MultipleGraph(Graph):
    """ Represents a button that plots two graphs. """

    def __init__(self, f1: str, f2: str, var: str) -> None:
        """ Creates a button. """
        super().__init__()
        self.f1 = f1
        self.f2 = f2
        self.var = var

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        await super().callback(itx)
        await graph_multiple_func(itx,
                                  self.f1,
                                  self.f2,
                                  self.var,
                                  dom=None,
                                  ran=None)
        self.view.stop()
