""" Code for two helper functions that plot functions as a function can be
plotted via a command or button.
"""
import discord

from src.api import send_request
from src.views import Answer


async def graph_single_func(itx: discord.Interaction,
                            func: str,
                            var: str,
                            dom: str,
                            ran: str | None) -> None:
    """ Plots a single function and sends the answer. """
    # Check for bug with tan functions where automatic range fails.
    if 'tan' in func and ran is None:
        ran = '-5,5'
    res = await send_request('/graph-func-single', {'func': func,
                                                    'var': var,
                                                    'dom': dom,
                                                    'ran': ran})
    out = (f"Function: "
           f"`{res['pretty']['func']}`\n"
           f"Limits: "
           f"`{res['pretty']['var']}∈{res['pretty']['dom']}`")
    if ran:
        out += f", `y∈{res['pretty']['ran']}`"
    await Answer(itx, out, res['image']).send()


async def graph_multiple_func(itx: discord.Interaction,
                              func1: str,
                              func2: str,
                              var: str,
                              dom: str,
                              ran: str | None) -> None:
    """ Plots two functions and sends the answer. """
    # Check for bug with tan functions where automatic range doesn't work.
    if ('tan' in func1 or 'tan' in func2) and ran is None:
        ran = '-5,5'
    res = await send_request('/graph-func-multiple', {'func1': func1,
                                                      'func2': func2,
                                                      'var': var,
                                                      'dom': dom,
                                                      'ran': ran})
    out = (f"Functions: "
           f"`{res['pretty']['func1']}`,"
           f"`{res['pretty']['func2']}`\n"
           f"Limits: "
           f"`{res['pretty']['var']}∈{res['pretty']['dom']}`")
    if ran:
        out += f", `y∈{res['pretty']['ran']}`"
    await Answer(itx, out, res['image']).send()
