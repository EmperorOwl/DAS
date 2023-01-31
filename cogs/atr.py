""" Code for handling Automatic Tex Recognition (ATR). """

import re
import discord
from discord import app_commands
from discord.ext import commands

from modules.bot import DAS
from backend.renderer import render
from modules.buttons import Buttons, Delete, Confirm


class ATR(commands.Cog):
    """ Represents a collection of ATR commands and listeners """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot

    @app_commands.command()
    async def atr(self, itx: discord.Interaction):
        """ Toggles Automatic TeX Recognition (ATR). """
        settings = self.bot.get_atr_settings()
        try:  # User has toggled before.
            atr = settings[str(itx.guild_id)]['atr']
            if atr:
                settings[str(itx.guild_id)]['atr'] = False
                content = f"⚙**  |  {itx.user.display_name}** has disabled " \
                          f"Automatic Tex Recognition."
            else:
                settings[str(itx.guild_id)]['atr'] = True
                content = f"⚙**  |  {itx.user.display_name}** has enabled " \
                          f"Automatic Tex Recognition! Try typing `$x^2$`.\n" \
                          f"To learn more, check out " \
                          f"<{self.bot['docs']}/tex-tutorial>"
        except KeyError:  # User's first time.
            settings[str(itx.guild_id)] = {'atr': True}
            content = f"⚙**  |  {itx.user.display_name}** has enabled " \
                      f"Automatic Tex Recognition! Try typing `$x^2$`.\n" \
                      f"To learn more, check out " \
                      f"<{self.bot['docs']}/tex-tutorial>"
        self.bot.edit_atr_settings(settings)
        await itx.response.send_message(content)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        """ Listens for new messages that may trigger ATR. """
        await self.manage_atr(msg)

    @commands.Cog.listener()
    async def on_message_edit(self,
                              _,
                              after: discord.Message) -> None:
        """ Listens for message edits that may trigger ATR. """
        await self.manage_atr(after)

    async def manage_atr(self, msg: discord.Message) -> None:
        """ Performs Automatic Tex Recognition (ATR). """
        if not msg.author.bot and re.search(r'\$(.+)\$', msg.content):
            settings = self.bot.get_atr_settings()
            try:
                if settings[str(msg.guild.id)]['atr']:
                    try:
                        render(msg.content)
                    except ValueError as error:
                        await Buttons.with_msg(
                            msg=await msg.reply(
                                content=(
                                    f"**☹  |  {msg.author.display_name}**, your "
                                    f"input has led to a `TeXParsingError`.\n"
                                    f"*You may edit your message to generate a "
                                    f"new image and then delete this one.*\n"
                                    f"```{error}```"
                                ),
                                mention_author=False
                            ),
                            btns=[Delete(delete_reference=True)]
                        )
                    else:
                        await Buttons.with_msg(
                            msg=await msg.reply(
                                content=f"**{msg.author.display_name}**",
                                file=discord.File('renders/tex.png'),
                                mention_author=False,
                            ),
                            btns=[Delete(delete_reference=True),
                                  Confirm(delete_reference=True)]
                        )
                else:
                    pass  # As user has disabled ATR.
            except KeyError:
                pass  # As user has never enabled ATR.


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(ATR(bot), guild=bot.test_guild)
