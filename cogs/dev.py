""" Code for development/maintenance commands. """

import datetime
import discord
from discord.ext import commands, tasks

from modules.bot import DAS, STATS_CHANNEL
from modules.utils import read_data_from_json_file, write_data_to_json_file

RESET_TIME = datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc)


class Dev(commands.Cog):
    """ Represents a collection of development commands. """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot
        self.yesterday_stats.start()  # Start the task.

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

    def _get_stats_embed(self, stats: dict) -> discord.Embed:
        """ Returns the embed containing stats about the bot. """
        embed = discord.Embed(
            title="DAS Stats",
            description="Stats only started being collected from 21/10/2023",
            colour=discord.Colour.green(),
            timestamp=discord.utils.utcnow()
        ).set_footer(
            text=f"Bot Version: {self.bot['version']}"
        )
        for time_period in ['all_time', 'today']:
            embed.add_field(
                name=time_period.replace('_', ' ').title(),
                value=(
                    '```'
                    f"Interactions Processed: {stats[time_period]['interactions']}\n"
                    f"Commands Processed: {stats[time_period]['commands']}\n"
                    f"Graphs Plotted: {stats[time_period]['graphs']}\n"
                    '```'
                ),
                inline=True
            )
        return embed

    @commands.command()
    async def stats(self, ctx: commands.Context) -> None:
        """ Returns some stats about the bot. """
        stats = read_data_from_json_file(self.bot.STATS_FILE)
        if not stats:
            await ctx.send("none available")
        else:
            await ctx.send(embed=self._get_stats_embed(stats))

    @commands.Cog.listener()
    async def on_interaction(self, itx: discord.Interaction):
        """ Listens for interactions, incrementing the stats.
        :param itx: the Discord interaction
        """
        stats = read_data_from_json_file(self.bot.STATS_FILE)
        if not stats:
            stats = {
                'all_time': {
                    'interactions': 0,
                    'commands': 0,
                    'graphs': 0
                },
                'today': {
                    'interactions': 0,
                    'commands': 0,
                    'graphs': 0
                }
            }
        for time_period in ['all_time', 'today']:
            stats[time_period]['interactions'] += 1
            if itx.command is not None:
                stats[time_period]['commands'] += 1
                if itx.command.qualified_name.startswith('graph'):
                    stats[time_period]['graphs'] += 1
        write_data_to_json_file(self.bot.STATS_FILE, stats)

    @tasks.loop(time=RESET_TIME)
    async def yesterday_stats(self) -> None:
        """ Logs the stats for yesterday before resetting them. """
        stats = read_data_from_json_file(self.bot.STATS_FILE)
        if stats:
            if STATS_CHANNEL:
                stats_channel = self.bot.get_channel(STATS_CHANNEL)
                await stats_channel.send(embed=self._get_stats_embed(stats))
            for category in stats['today']:
                stats['today'][category] = 0
            write_data_to_json_file(self.bot.STATS_FILE, stats)
            print(f"Reset yesterday's stats.")


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Dev(bot), guild=bot.test_guild)
