""" Code for development/maintenance commands. """

import discord
from discord.ext import commands

from modules.bot import DAS


class Dev(commands.Cog):
    """ Represents a collection of development commands. """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        """ Syncs the bot's slash commands with the Discord API. """
        synced = await ctx.bot.tree.sync(guild=self.bot.test_guild)
        if synced:
            await ctx.send(f"Synced the following commands:\n" +
                           ', '.join([f"`{cmd.name}`" for cmd in synced]))
        else:
            await ctx.send(f"Failed to sync any commands.")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def clear(self, ctx: commands.Context) -> None:
        """ Clears the bot's slash commands with the Discord API. """
        ctx.bot.tree.clear_commands(guild=self.bot.test_guild)
        synced = await ctx.bot.tree.sync(guild=self.bot.test_guild)
        if synced:
            await ctx.send(f"Failed to clear the following commands: \n" +
                           ', '.join([f"`{cmd.name}`" for cmd in synced]))
        else:
            await ctx.send(f"Cleared all commands.")

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx: commands.Context, guild_id: str) -> None:
        """ Removes the bot from the specified guild. """
        guild = ctx.bot.get_guild(int(guild_id))
        if guild:
            try:
                await guild.leave()
            except discord.HTTPException:
                await ctx.send(f"Failed to leave {guild.name}.")
            else:
                await ctx.send(f"DAS has left {guild.name}.")
        else:
            await ctx.send("Failed to find guild.")


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Dev(bot), guild=bot.test_guild)
