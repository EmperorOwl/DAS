""" Code for development/maintenance commands. """
import datetime
import discord
from discord.ext import commands, tasks

from frontend.config import STATS_CHANNEL
from frontend.utils import read_data_from_json_file, write_data_to_json_file


class Stats(commands.Cog):
    """ Represents a collection of development commands. """
    START_DATE = datetime.date(year=2023, month=10, day=21)
    RESET_TIME = datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc)
    STATS_FILE = 'frontend/config/stats.json'
    STATS_TEMPLATE = {
        'all_time': {
            'commands': 0,
            'buttons': 0,
            'graphs': {
                'commands': 0,
                'buttons': 0
            }
        },
        'today': {
            'commands': 0,
            'buttons': 0,
            'graphs': {
                'commands': 0,
                'buttons': 0
            }
        }
    }

    def __init__(self, bot: commands.Bot) -> None:
        """ Starts the task. """
        self.bot = bot
        self.yesterday_stats.start()

    def _get_stats_embed(self, stats: dict) -> discord.Embed:
        """ Returns the embed containing stats about the bot. """
        pretty_start_date = self.START_DATE.strftime('%d %B %Y')
        embed = discord.Embed(
            title="DAS Stats",
            description=f"Started collecting on the {pretty_start_date}",
            colour=discord.Colour.green(),
        )
        for time_period in stats:
            # Unpack figures
            cmds = stats[time_period]['commands']
            btns = stats[time_period]['buttons']
            graph_cmds = stats[time_period]['graphs']['commands']
            graph_btns = stats[time_period]['graphs']['buttons']
            # Compute totals
            graphs = graph_cmds + graph_btns
            total = cmds + btns + graphs
            # Compute percentages
            cmds_per = int(cmds / total * 100) if total != 0 else 0
            btns_per = int(btns / total * 100) if total != 0 else 0
            graphs_per = int(graphs / total * 100) if total != 0 else 0
            graph_cmds_per = int(graph_cmds / graphs * 100) if graphs != 0 else 0
            graph_btns_per = int(graph_btns / graphs * 100) if graphs != 0 else 0
            # Compute average
            if time_period == 'all_time':
                days = (datetime.date.today() - self.START_DATE).days
                average = int(total / days) if days != 0 else 0
                avg_graphs = int(graphs / days) if days != 0 else 0
                embed.description += '\n'
                embed.description += (f"Current average is {average} "
                                      f"interactions per day, "
                                      f"about {avg_graphs} are graphs")

            # Add embed field
            embed.add_field(
                name=time_period.replace('_', ' ').title(),
                value=(
                    '```'
                    f"Interactions: {total}\n"
                    f"|___Commands: {cmds}\n"
                    f"|____Buttons: {btns}\n"
                    f"|_____Graphs: {graphs}\n"
                    f"      |_Cmds: {graph_cmds}\n"
                    f"      |_Btns: {graph_btns}\n"
                    '```'
                    '\n'
                    f"**Summary**\n"
                    f"- {cmds_per}% via slash command\n"
                    f"- {btns_per}% via button press\n"
                    f"- {graphs_per}% were graphs\n"
                    f"  - {graph_cmds_per}% via command\n"
                    f"  - {graph_btns_per}% via button press"
                ),
                inline=True
            )
        return embed

    @commands.command()
    async def stats(self, ctx: commands.Context) -> None:
        """ Returns some stats about the bot. """
        stats = read_data_from_json_file(self.STATS_FILE)
        if not stats:
            await ctx.send("none available")
        else:
            await ctx.send(embed=self._get_stats_embed(stats))

    @commands.Cog.listener()
    async def on_interaction(self, itx: discord.Interaction):
        """ Listens for interactions, incrementing the stats.
        :param itx: the Discord interaction
        """
        stats = read_data_from_json_file(self.STATS_FILE)
        if not stats:
            stats = self.STATS_TEMPLATE
        for time_period in stats:
            # Check for slash command.
            if itx.command:
                # Check for graph slash command.
                if itx.command.qualified_name.startswith('graph'):
                    stats[time_period]['graphs']['commands'] += 1
                else:
                    stats[time_period]['commands'] += 1
            # Otherwise, button press.
            else:
                # Check for graph button press.
                if itx.extras.get('is_graph', False):
                    stats[time_period]['graphs']['buttons'] += 1
                else:
                    stats[time_period]['buttons'] += 1
        write_data_to_json_file(self.STATS_FILE, stats)

    @tasks.loop(time=RESET_TIME)
    async def yesterday_stats(self) -> None:
        """ Logs the stats for yesterday before resetting them. """
        stats = read_data_from_json_file(self.STATS_FILE)
        if stats:
            if STATS_CHANNEL:
                stats_channel = self.bot.get_channel(STATS_CHANNEL)
                await stats_channel.send(embed=self._get_stats_embed(stats))
            stats['today'] = self.STATS_TEMPLATE['today']
            write_data_to_json_file(self.STATS_FILE, stats)
            print(f"Reset yesterday's stats.")


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Stats(bot))
