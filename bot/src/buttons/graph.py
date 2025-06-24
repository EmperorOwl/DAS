""" Code for the graph buttons. """
import discord
from abc import ABC

from src.utils import graph_single_func, graph_multiple_func


class Graph(ABC, discord.ui.Button):
    """ Represents a graph button. """
    EMOJI = '📈'
    STYLE = discord.ButtonStyle.primary
    DEFAULT_DOMAIN = '-5,5'

    def __init__(self) -> None:
        super().__init__(emoji=self.EMOJI, style=self.STYLE)
        self.dom = Graph.DEFAULT_DOMAIN
        self.ran = None

    async def callback(self, itx: discord.Interaction) -> None:
        if self.view is None:
            raise ValueError("Button is not attached to a view")
        itx.extras = {'is_graph': True}  # For stat collecting
        await self.view.msg.edit(view=self.view.clear_items())


class SingleGraph(Graph):
    """ Represents a button that plots a single function. """

    def __init__(self, func: str, var: str) -> None:
        super().__init__()
        self.func = func
        self.var = var

    async def callback(self, itx: discord.Interaction) -> None:
        await super().callback(itx)
        await graph_single_func(itx, self.func, self.var, self.dom, self.ran)
        if self.view:
            self.view.stop()


class MultipleGraph(Graph):
    """ Represents a button that plots two functions. """

    def __init__(self, func1: str, func2: str, var: str) -> None:
        super().__init__()
        self.func1 = func1
        self.func2 = func2
        self.var = var

    async def callback(self, itx: discord.Interaction) -> None:
        await super().callback(itx)
        await graph_multiple_func(itx,
                                  self.func1,
                                  self.func2,
                                  self.var,
                                  self.dom,
                                  self.ran)
        if self.view:
            self.view.stop()
