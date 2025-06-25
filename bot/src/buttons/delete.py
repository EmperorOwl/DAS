""" Code for the delete button. """
import discord

from src.utils import silent_delete_msg, silent_delete_ref_msg


class Delete(discord.ui.Button):
    """ Represents a delete button. 
    When pressed, the message will be deleted.
    If del_ref_msg is True, the reference message will also be deleted.
    """
    EMOJI = '🗑️'
    STYLE = discord.ButtonStyle.secondary

    def __init__(self, del_ref_msg: bool = False) -> None:
        super().__init__(emoji=self.EMOJI, style=self.STYLE)
        self.del_ref_msg = del_ref_msg

    async def callback(self, itx: discord.Interaction) -> None:
        if self.view is None:
            raise ValueError("Button is not attached to a view")
        if itx.message:
            # Don't delete itx.message as it will raise 403 Forbidden in DMs
            # I think self.view.msg works because it is an InteractionMessage,
            # while itx.message is a Message
            # self.view.msg can be Message though, e.g. for ATR but
            # ATR is not applicable in DMs so we are fine for now
            await silent_delete_msg(self.view.msg)
            if (self.del_ref_msg and itx.channel and itx.message.reference):
                await silent_delete_ref_msg(itx.channel, itx.message.reference)
        self.view.stop()
