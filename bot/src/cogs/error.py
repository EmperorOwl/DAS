""" Code for handling errors. """
import sys
import traceback
import discord
from discord import app_commands
from discord.ext import commands

from src.api import TimeoutException, InputException, ServerException
from src.config import LOG_CHANNEL, info
from src.views import ErrorView
from src.utils import pretty_inputs


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
        # print('Ignoring exception in command {}:'.format(itx.command),
        #       file=sys.stderr)
        # traceback.print_exception(type(error),
        #                           error,
        #                           error.__traceback__,
        #                           file=sys.stderr)
        # Send error message to log channel.
        if LOG_CHANNEL:
            log_channel = itx.client.get_channel(LOG_CHANNEL)
            if (isinstance(log_channel, discord.TextChannel)
                    and itx.guild
                    and itx.command):
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
            # Command took too long
            if isinstance(err, TimeoutException):
                err_title = "🤯 Oof! Something's too big!"
                err_desc = ("Your request timed out. For efficiency purposes, "
                            "DAS can't handle requests with super large or "
                            "super small numbers.")
                await ErrorView(itx, err_title, err_desc).send()
            # User input was incorrect
            elif isinstance(err, InputException):
                if err.name in ['ParsingError',
                                'SyntaxError',
                                'NotImplementedError']:
                    err_title = "☹️ Uh oh! Something's not right!"
                    err_desc = (f"Looks like there was a `{err.name}`.\n"
                                f"```{err.message}```")
                    await ErrorView(itx, err_title, err_desc).send()
                else:
                    await self._handle_uncaught(itx, error)
            # Server encountered an error
            elif isinstance(err, ServerException):
                err_title = "🚨 Oops! Something went wrong!"
                err_desc = ("Looks like there is an issue with the bot.\n"
                            "Please try again later.")
                await ErrorView(itx, err_title, err_desc).send()
            else:
                await self._handle_uncaught(itx, error)
        # User does not have the required permissions
        elif isinstance(error, app_commands.MissingPermissions):
            err_title = "🚓 Oh no! Permission denied!"
            err_desc = "Try asking a mod for help."
            await ErrorView(itx, err_title, err_desc).send()
        # Bot does not have the required permissions
        elif isinstance(error, discord.Forbidden):
            err_title = "🚓 Oh no! Bot is missing permissions!"
            err_desc = f"{str(error)}"
            err_desc += "Please re-invite the bot to the server."
            await ErrorView(itx, err_title, err_desc).send()
        else:
            await self._handle_uncaught(itx, error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Error())
