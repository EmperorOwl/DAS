import discord

from backend.config import TEX_FNAME, PLOT_FNAME, TEX_PATH, PLOT_PATH
from .view import View


class Answer(View):
    """ Represents an answer response to a user's request. """

    def __init__(self,
                 itx: discord.Interaction,
                 output_str: str = None,
                 btns: list[discord.ui.Button] = None) -> None:
        """ Creates an answer for the interaction itx. """
        from frontend.buttons import Delete, Confirm
        super().__init__(btns=[Delete(), Confirm()] + (btns if btns else []))
        self.itx = itx
        self.cmd_name = itx.command.qualified_name if itx.command else 'graph'
        self.output_str = output_str if output_str else ""

    async def send(self) -> None:
        """ Responds to the user with this view. """
        embed, file, view = self._get_embed(), self._get_file(), self
        await self.itx.response.send_message(embed=embed,
                                             file=file,
                                             view=view)
        # Initialise the message for this view as the interaction response
        self.msg = await self.itx.original_response()

    def _get_embed(self) -> discord.Embed:
        """ Returns the answer embed. """
        embed = discord.Embed(description=self.output_str,
                              colour=discord.Color.blue())
        embed.set_image(url=self._get_image_url())
        embed.set_footer(text=self._get_footer_text())
        return embed

    def _get_footer_text(self) -> str:
        """ Returns the embed footer. """
        credit = 'Powered by Matplotlib'
        time_taken = discord.utils.utcnow() - self.itx.created_at
        time_taken_str = f"Processed in {time_taken.total_seconds():.2f}s"
        return f"{credit} • {time_taken_str}"

    def _get_image_url(self) -> str:
        """ Returns the correct image url. """
        if 'graph' in self.cmd_name:
            return f"attachment://{PLOT_FNAME}"
        return f"attachment://{TEX_FNAME}"

    def _get_file(self) -> discord.File:
        """ Returns the correct image. """
        if 'graph' in self.cmd_name:
            return discord.File(PLOT_PATH)
        return discord.File(TEX_PATH)
