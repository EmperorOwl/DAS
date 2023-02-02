""" Code for handling errors. """

import sys
import traceback
import discord
from discord import app_commands
from discord.ext import commands

from modules.bot import DAS
from modules.buttons import Buttons, Delete
from modules.transform import CTR


class Error(commands.Cog):
    """ Represents the bot's error handler. """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot

    def cog_load(self) -> None:
        """ Attaches the error handler to the bot. """
        self.bot.tree.on_error = self.on_app_command_error

    async def _handle_uncaught(self,
                               itx: discord.Interaction,
                               error: app_commands.AppCommandError) -> None:
        """ [Helper] Handles an uncaught error.
        :param itx: the Discord interaction
        :param error: the error raised
        """
        # Send error message to user.
        await itx.response.send_message(
            embed=discord.Embed(
                title='☹️ Oops! Something went wrong!',
                description=f"If you were unsure about the syntax of the command, "
                            f"check out the docs at {self.bot['docs']}/commands.\n"
                            f"If you believe you have found a bug, please report "
                            f"it on our official server at {self.bot['server']}."
            )
        )
        # Display error message to terminal.
        print('Ignoring exception in command {}:'.format(itx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        # Send error message to log channel.
        log_channel = self.bot.get_channel(int(self.bot['log_channel']))
        kwargs = " ".join(f"{name}: {value}" for name, value in
                          list(DAS.get_original_inputs(itx).items()))
        await log_channel.send(
            embed=discord.Embed(
                title='Error Logged',
                colour=discord.Colour.red(),
                timestamp=discord.utils.utcnow()
            ).add_field(
                name='Information',
                value='```'
                      f"Guild ID: {itx.guild.id}\n"
                      f"Interaction ID: {itx.id}\n"
                      f"User ID: {itx.user.id}\n"
                      '```'
            ).add_field(
                name='Command',
                value=f"```/{itx.command.qualified_name} {kwargs}```",
                inline=False
            ).add_field(
                name='Exception',
                value=f"```{error}```",
                inline=False
            ).set_footer(
                text=f"Bot Version: {self.bot['version']}"
            )
        )

    @commands.Cog.listener()
    async def on_app_command_error(self,
                                   itx: discord.Interaction,
                                   error: app_commands.AppCommandError):
        """ Listens for errors raised when invoking a slash command.
        :param itx: the Discord interaction
        :param error: the error raised
        """
        # Handle errors that occur while processing the command.
        if isinstance(error, app_commands.CommandInvokeError):
            if itx.command.name == 'limit':
                await itx.response.send_message(
                    f"**☹️  |  {itx.user.display_name}**, the coordinate "
                    f"has to be a number or `oo` for infinity."
                )
            elif itx.command.name == 'linsolve':
                await itx.response.send_message(
                    f"**☹️  |  {itx.user.display_name}**, the equations "
                    f"have to be linear."
                )
            elif itx.command.name == 'average':
                await itx.response.send_message(
                    f"**☹️  |  {itx.user.display_name}**, your input "
                    f"was not a list of numbers separated by a space."
                )
            else:
                await self._handle_uncaught(itx, error)
        # Handle errors that occur when trying to transform an argument.
        elif isinstance(error, app_commands.TransformerError):
            # Check if error should be updated to original one.
            if isinstance(error.__cause__, CTR):
                error = error.__cause__
            await itx.response.send_message(
                embed=discord.Embed(
                    title='☹️ Uh oh! Something not right!',
                    description=(
                        f"Your input has led to a `TransformerError`.\n"
                        f"```{error}```"
                    )
                )
            )
        # Handle errors that occur when command takes too long.
        elif isinstance(error, discord.errors.NotFound):
            await itx.response.send_message(
                embed=discord.Embed(
                    title='☹️ Oof! Something too big!',
                    description="For efficiency purposes, DAS will not process "
                                "any requests with super large or small numbers."
                )
            )
        # Handle all other errors.
        else:
            await self._handle_uncaught(itx, error)
        # Finally attach buttons to error message.
        await Buttons.with_msg(await itx.original_response(), btns=[Delete()])


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Error(bot), guild=bot.test_guild)
