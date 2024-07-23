""" Code for development/maintenance commands.

Notes:
    Since all the cogs do not specify the guild to sync to, by default
    all the commands are global. Thus, when calling "list" with TEST_GUILD
    defined, there will be no commands listed. Thus, in "sync" they are copied
    from global before being synced.

References:
    https://about.abstractumbra.dev/dpy
"""
from discord.ext import commands

from frontend.config import TEST_GUILD
from frontend.utils import pretty_cmds


class Dev(commands.Cog):
    """ Represents a collection of development commands. """

    @staticmethod
    async def _send(ctx: commands.Context) -> None:
        """ Returns two lists.
        1. The list of commands registered with the bot.
        2. The list of commands synced with the Discord API.
        """
        cmds = ctx.bot.tree.get_commands(guild=TEST_GUILD)
        synced_cmds = await ctx.bot.tree.fetch_commands(guild=TEST_GUILD)
        await ctx.send(f"Commands: [{pretty_cmds(cmds)}]\n"
                       f"Synced: [{pretty_cmds(synced_cmds)}]")

    @commands.command()
    @commands.is_owner()
    async def list(self, ctx: commands.Context) -> None:
        """ Returns the list of slash commands. """
        await self._send(ctx)

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        """ Syncs the bot's slash commands with the Discord API. """
        if TEST_GUILD:
            ctx.bot.tree.copy_global_to(guild=TEST_GUILD)
        _ = await ctx.bot.tree.sync(guild=TEST_GUILD)
        await self._send(ctx)

    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx: commands.Context) -> None:
        """ Clears the bot's slash commands with the Discord API. """
        ctx.bot.tree.clear_commands(guild=TEST_GUILD)
        _ = await ctx.bot.tree.sync(guild=TEST_GUILD)
        await self._send(ctx)

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx: commands.Context, guild_id: int) -> None:
        """ Removes the bot from a guild. """
        guild = ctx.bot.get_guild(guild_id)
        if guild:
            await guild.leave()
            await ctx.send(f"DAS has left {guild.name}.")
        else:
            await ctx.send(f"Failed to find guild with ID {guild_id}.")

    async def cog_command_error(self,
                                ctx: commands.Context,
                                error: commands.CommandError) -> None:
        """ Replies back with the error message if an error is encountered
        while trying to execute a command in this cog.
        """
        await ctx.send(f"{type(error).__name__}: {error}")


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Dev())
