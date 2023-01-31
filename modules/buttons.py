""" Code for creating and handling Discord UI Views. """

from __future__ import annotations

import discord

from backend import plotter
from modules import answer
from modules import transform


async def _delete(msg: discord.Message) -> None:
    """ [Helper] Deletes a message without raising errors. """
    try:
        await msg.delete()
    except AttributeError:
        pass  # As message does not exist.
    except discord.errors.NotFound:
        pass  # As message may have already been deleted.


class Single(discord.ui.Button):
    """ Represents a graph button which plots a single function. """

    def __init__(self, function: transform.Function) -> None:
        """ Creates a button. """
        super().__init__(emoji='📈', style=discord.ButtonStyle.primary)
        self.function = function
        self.domain = transform.DEFAULT_LIMIT
        self.range = transform.DEFAULT_LIMIT

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        await self.view.msg.edit(view=self.view.clear_items())
        plotter.plot_single_function(self.function, self.domain, self.range)
        await answer.send(
            itx,
            inputs=f"Function: `{self.function}`\n"
                   f"Limits: `x∈{self.domain}`, `y∈{self.range}`",
            cmd_name='graph single function'
        )
        self.view.stop()


class Multiple(discord.ui.Button):
    """ Represents a graph button which plots two functions. """

    def __init__(self,
                 func1: transform.Function,
                 func2: transform.Function) -> None:
        """ Creates a button. """
        super().__init__(emoji='📈', style=discord.ButtonStyle.primary)
        self.f1 = func1
        self.f2 = func2
        self.dom = transform.DEFAULT_LIMIT
        self.ran = transform.DEFAULT_LIMIT

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        await self.view.msg.edit(view=self.view.clear_items())
        plotter.plot_multiple_functions(self.f1, self.f2, self.dom, self.ran)
        await answer.send(
            itx,
            inputs=f"Functions: `{self.f1}`, `{self.f2}`\n"
                   f"Limits: `x∈{self.dom}`, `y∈{self.ran}`",
            cmd_name='graph multiple functions'
        )
        self.view.stop()


class Delete(discord.ui.Button):
    """ Represents a graph button. """

    def __init__(self, delete_reference: bool = False) -> None:
        """ Creates a button. """
        super().__init__(emoji='🗑️', style=discord.ButtonStyle.secondary)
        self.delete_reference = delete_reference

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        msg = itx.message
        if self.delete_reference:
            ref = await msg.channel.fetch_message(msg.reference.message_id)
            await _delete(ref)
        await _delete(msg)
        self.view.stop()


class Confirm(discord.ui.Button):
    """ Represents a confirm button. """

    def __init__(self, delete_reference: bool = False) -> None:
        """ Creates a button. """
        super().__init__(emoji='✅', style=discord.ButtonStyle.success)
        self.delete_reference = delete_reference

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        msg = itx.message
        if self.delete_reference:
            ref = await msg.channel.fetch_message(msg.reference.message_id)
            await _delete(ref)
        await itx.response.edit_message(view=self.view.clear_items())
        self.view.stop()


class Buttons(discord.ui.View):
    """ Represents the interactive buttons on an embed or message.

    constants:
        TIMEOUT: the number in seconds before the buttons are removed\

    attributes:
        msg: the message the buttons are attached to

    """
    TIMEOUT = 120.0

    def __init__(self,
                 msg: discord.Message,
                 btns: list[discord.ui.Button] = None) -> None:
        """ Creates a view. """
        super().__init__(timeout=Buttons.TIMEOUT)
        # Add default buttons if no buttons are specified.
        if not btns:
            btns = [Delete(), Confirm()]
        # Add the buttons.
        for btn in btns:
            self.add_item(btn)
        # Create instance variables.
        self.msg = msg

    @classmethod
    async def with_msg(cls,
                       msg: discord.Message,
                       btns: list[discord.ui.Button]) -> Buttons:
        """ Adds the view to the message. """
        self = cls(msg, btns)
        await self.msg.edit(view=self)
        return self

    async def on_timeout(self) -> None:
        """ Removes buttons from message on timeout. """
        try:
            await self.msg.edit(view=self.clear_items())
        except discord.errors.NotFound:
            pass  # As message may have already been deleted.
        finally:
            self.stop()
