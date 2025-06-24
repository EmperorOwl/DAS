""" Code for the confirm button. """
import discord

from src.utils import silent_delete_ref_msg


class Confirm(discord.ui.Button):
    """ Represents a confirm button.
    When pressed all buttons will be removed from the view.
    If del_ref_msg is True, the button will also delete the reference message.
    """
    EMOJI = '✅'
    STYLE = discord.ButtonStyle.success

    def __init__(self, del_ref_msg: bool = False) -> None:
        super().__init__(emoji=self.EMOJI, style=self.STYLE)
        self.del_ref_msg = del_ref_msg

    async def callback(self, itx: discord.Interaction) -> None:
        if self.view is None:
            raise ValueError("Button is not attached to a view")
        await itx.response.edit_message(view=self.view.clear_items())
        if (self.del_ref_msg
                and itx.channel
                and itx.message
                and itx.message.reference):
            await silent_delete_ref_msg(itx.channel, itx.message.reference)
        self.view.stop()
