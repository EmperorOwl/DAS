""" Code for handling errors. """
import sys
import traceback
import discord
from discord import app_commands
from discord.ext import commands

from frontend.config import LOG_CHANNEL, info
from frontend.views import ErrorView
from frontend.utils import pretty_inputs


class Error(commands.Cog):
    """ Represents the bot's error handler. """

    @staticmethod
    async def _handle_uncaught(itx: discord.Interaction,
                               error: app_commands.AppCommandError) -> None:
        """ [Helper] Handles an uncaught error.
        :param itx: the Discord interaction
        :param error: the error raised
        """
        # Send error message to user.
        err_title = '☹️ Oops! Something went wrong!'
        err_desc = (f"If you were unsure about the syntax of the command, "
                    f"check out the docs at {info.DOCS}/commands.\n"
                    f"If you believe you have found a bug, please report "
                    f"it on our official server at {info.SERVER}.")
        await ErrorView(itx, err_title, err_desc).send()
        # Display error message to terminal.
        print('Ignoring exception in command {}:'.format(itx.command),
              file=sys.stderr)
        traceback.print_exception(type(error),
                                  error,
                                  error.__traceback__,
                                  file=sys.stderr)
        # Send error message to log channel.
        if LOG_CHANNEL:
            log_channel = itx.client.get_channel(LOG_CHANNEL)
            inputs = pretty_inputs(itx)
            await log_channel.send(
                embed=discord.Embed(
                    title='Error Logged',
                    colour=discord.Colour.red(),
                ).add_field(
                    name='Information',
                    value='```'
                          f"Guild ID: {itx.guild.id}\n"
                          f"Interaction ID: {itx.id}\n"
                          f"User ID: {itx.user.id}\n"
                          '```'
                ).add_field(
                    name='Command',
                    value=f"```/{itx.command.qualified_name} {inputs}```",
                    inline=False
                ).add_field(
                    name='Exception',
                    value=f"```{error}```",
                    inline=False
                ).set_footer(
                    text=f"Bot Version: {info.VERSION}"
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
        # Command error
        if isinstance(error, app_commands.CommandInvokeError):
            err = error.original
            # User input incorrect
            if isinstance(err, ValueError | NotImplementedError | SyntaxError):
                err_title = "☹️ Uh oh! Something's not right!"
                err_desc = (f"Looks like there was `{type(err).__name__}`\n"
                            f"```{err}```")
                await ErrorView(itx, err_title, err_desc).send()
            else:
                await self._handle_uncaught(itx, error)
        # Command took too long.
        elif isinstance(error, discord.errors.NotFound):
            err_title = "☹️ Oof! Something's too big!"
            err_desc = ("For efficiency purposes, DAS can't handle requests "
                        "with super large or small numbers.")
            await ErrorView(itx, err_title, err_desc).send()
        # User does not have the required permissions
        elif isinstance(error, app_commands.MissingPermissions):
            err_title = "🚓 Oops! Permission denied!"
            err_desc = "Try asking a mod for help."
            await ErrorView(itx, err_title, err_desc).send()
        else:
            await self._handle_uncaught(itx, error)


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Error())
