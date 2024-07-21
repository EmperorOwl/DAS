""" Code for handling Automatic Tex Recognition (ATR). """
import re
from discord import Message, Interaction, app_commands
from discord.ext import commands

from backend import renderer
from frontend.config import info
from frontend.views import TexRenderSuccess, TexRenderFail
from frontend.utils import read_data_from_json_file, write_data_to_json_file


class ATR(commands.Cog):
    """ Represents a collection of ATR commands and listeners """
    SETTINGS_FILE = 'config/settings.json'

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def atr(self, itx: Interaction):
        """ Toggles ATR. """
        settings = read_data_from_json_file(self.SETTINGS_FILE)
        key = str(itx.guild_id)
        # Perform toggle.
        try:
            settings[key]['atr'] = not settings[key]['atr']
        except KeyError:  # User's first time enabling.
            settings[key] = {'atr': True}
        # Update settings file.
        write_data_to_json_file(self.SETTINGS_FILE, settings)
        # Respond back to user.
        if settings[key]['atr']:
            content = (f"⚙**  |  {itx.user.display_name}** has enabled "
                       f"Automatic Tex Recognition! (ATR). "
                       f"Try typing `$x^2$`.\n"
                       f"To learn more, check out "
                       f"<{info.DOCS}/tex-tutorial>")
        else:
            content = (f"⚙**  |  {itx.user.display_name}** has disabled "
                       f"Automatic Tex Recognition (ATR).")
        await itx.response.send_message(content)

    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        """ Listens for new messages that may trigger ATR. """
        await self.manage_atr(msg)

    @commands.Cog.listener()
    async def on_message_edit(self, _: Message, after: Message) -> None:
        """ Listens for message edits that may trigger ATR. """
        await self.manage_atr(after)

    async def manage_atr(self, msg: Message) -> None:
        """ Checks for and performs ATR if enabled. """
        if not msg.author.bot and re.search(r'\$(.+)\$', msg.content):
            settings = read_data_from_json_file(self.SETTINGS_FILE)
            try:
                if settings[str(msg.guild.id)]['atr']:
                    try:
                        renderer.render(msg.content)
                    except ValueError as error:
                        await TexRenderFail(msg, error).send()
                    else:
                        await TexRenderSuccess(msg).send()
                else:
                    pass  # As server has disabled ATR.
            except KeyError:
                pass  # As server has never enabled ATR.


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(ATR())
