""" Code for handling Automatic Tex Recognition (ATR). """
import re
import discord
from discord import Message, Interaction, app_commands
from discord.ext import commands

from src.api import send_request
from src.config import info, SETTINGS_FILE
from src.views import TexRenderSuccess, TexRenderFail
from src.utils import read_data_from_json_file, write_data_to_json_file


class ATR(commands.Cog):
    """ Represents a collection of ATR commands and listeners """

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def atr(self, itx: Interaction):
        """ Toggles ATR. """
        settings = read_data_from_json_file(SETTINGS_FILE)
        key = str(itx.guild_id)
        # Perform toggle.
        try:
            settings[key]['atr'] = not settings[key]['atr']
        except KeyError:  # User's first time enabling.
            settings[key] = {'atr': True}
        # Update settings file.
        write_data_to_json_file(SETTINGS_FILE, settings)
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
        text = msg.content
        if not msg.author.bot and re.search(r'\$(.+)\$', text):
            settings = read_data_from_json_file(SETTINGS_FILE)
            try:
                if msg.guild and settings[str(msg.guild.id)]['atr']:
                    try:
                        res = await send_request('/display', {'text': text})
                    except Exception as error:
                        await TexRenderFail(msg, error).send()
                    else:
                        await TexRenderSuccess(msg, res['image']).send()
                else:
                    pass  # As server has disabled ATR
            except KeyError:
                pass  # As server has never enabled ATR
            except discord.Forbidden as error:
                # Triggers if the permission "Read Message History" is missing
                errMsg = (f"🚓 Oh no! I am missing some permissions, please "
                          f"re-invite me to the server.\n"
                          f"Otherwise, if you would like to disable Automatic "
                          f"TeX Recognition, type `/atr`.\n"
                          f"```{str(error)}```")
                await msg.channel.send(errMsg)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ATR())
