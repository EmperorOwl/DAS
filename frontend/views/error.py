import discord
from discord import Interaction

from .view import View


class ErrorView(View):
    """ Represents an error response to a user's request. """

    def __init__(self, itx: Interaction, err_title: str, err_msg: str) -> None:
        """ Creates an error message for the interaction itx. """
        from frontend.buttons import Delete
        super().__init__(btns=[Delete()])
        self.itx = itx
        self.err_title = err_title
        self.err_msg = err_msg

    def _get_embed(self) -> discord.Embed:
        embed = discord.Embed(title=self.err_title, description=self.err_msg)
        return embed

    async def send(self) -> None:
        """ Responds to the user with this view. """
        embed = self._get_embed()
        await self.itx.response.send_message(embed=embed, view=self)
        self.msg = await self.itx.original_response()
