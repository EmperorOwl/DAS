""" Code for two helper functions that plot functions as a function can be
plotted via a command or button.
"""
import discord

from backend import plotter
from frontend.views import Answer
from .transform import CharLim1, CharLim25


async def graph_single_func(itx: discord.Interaction,
                            func: CharLim25,
                            var: CharLim1,
                            dom: CharLim25 = None,
                            ran: CharLim25 = None) -> None:
    """ Plots a single function and sends the answer. """
    output_str = plotter.plot_single_func(func, var, dom, ran)
    await Answer(itx, output_str).send()


async def graph_multiple_func(itx: discord.Interaction,
                              f1: CharLim25,
                              f2: CharLim25,
                              var: CharLim1,
                              dom: CharLim25 = None,
                              ran: CharLim25 = None) -> None:
    """ Plots two functions and sends the answer. """
    output_str = plotter.plot_multiple_func(f1, f2, var, dom, ran)
    await Answer(itx, output_str).send()
