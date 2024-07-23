import discord

from frontend.utils import silent_delete_ref_msg


class Confirm(discord.ui.Button):
    """ Represents a confirm button. """
    EMOJI = '✅'
    STYLE = discord.ButtonStyle.success

    def __init__(self, del_ref_msg: bool = False) -> None:
        """ Creates a button. """
        super().__init__(emoji=self.EMOJI, style=self.STYLE)
        self.del_ref_msg = del_ref_msg

    async def callback(self, itx: discord.Interaction) -> None:
        """ Handles a button press. """
        await itx.response.edit_message(view=self.view.clear_items())
        if self.del_ref_msg:
            await silent_delete_ref_msg(itx.channel, itx.message.reference)
        self.view.stop()
