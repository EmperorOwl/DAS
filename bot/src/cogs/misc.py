""" Code for miscellaneous commands. """
import time
import discord
from discord import app_commands
from discord.ext import commands

from src.config import info


class Misc(commands.Cog):
    """ Represents a collection of miscellaneous commands. """

    @app_commands.command()
    async def help(self, itx: discord.Interaction) -> None:
        """ Responds with a list of DAS' commands. """
        await itx.response.send_message(
            embed=discord.Embed(
                title="Help Page",
                url=info.DOCS,
                description=info.DESC,
                colour=discord.Colour.blue()
            ).set_thumbnail(
                url=itx.client.user.avatar.url  # type: ignore
            ).add_field(
                name="My Commands",
                value=(
                    """
                    `display` - Display math text as an image!
                    `graph` - Plot a graph!
                    `limit` - Find the limit of a function!
                    `derive` - Derive a function!
                    `integrate` - Integrate a function!
                    `solve` - Solve an equation!
                    `linsolve` - Solve a pair of linear equations!
                    `expand` - Expand an expression!
                    `factor` - Factor an expression!
                    `simplify` - Simplify an expression!
                    `calculate` - Evaluate an expression!
                    `average` - Find the average of a list of numbers!
                    `atr` - Toggle Automatic TeX Recognition (ATR)!
                    """
                ),
                inline=False
            ).add_field(
                name="Other Commands ",
                value="`about` `ping` `server` `vote`",
                inline=False
            ).set_footer(
                text=f"Developed by {info.DEV} • Version {info.VERSION}"
            )
        )

    @app_commands.command()
    async def about(self, itx: discord.Interaction) -> None:
        """ Responds with some facts about DAS. """
        bot = itx.client
        await itx.response.send_message(
            embed=discord.Embed(
                title="About Me",
                description=(
                    f"{info.DESC}\n"
                    '\n'
                    f"`      Developer:` {info.DEV}\n"
                    f"`        Servers:` {len(bot.guilds)}\n"
                    f"`          Users:` {info.users(bot.guilds)}\n"
                    f"`         Shards:` {bot.shard_count}\n"
                    f"`         Memory:` {info.memory_usage()}\n"
                    f"`      CPU Usage:` {info.cpu_usage()}\n"
                    f"`        Latency:` {int(bot.latency * 1000)}ms\n"
                    f"`    Bot Version:` {info.VERSION}\n"
                    f"` Python Version:` {info.PY_VERSION}\n"
                    f"`       Platform:` {info.OS}\n"
                    f"`         Uptime:` {bot.get_uptime()}\n"  # type: ignore
                    f"`           Host:` {info.HOST}\n"
                    '\n'
                    f"[Top.gg Site]({info.TOPGG}) ~ " +
                    f"[Server Invite]({info.SERVER}) ~ " +
                    f"[Gitbook Docs]({info.DOCS}) ~ " +
                    f"[Github Repository]({info.REPO})"
                ),
                color=discord.Color.blue()
            )
        )

    @app_commands.command()
    async def ping(self, itx: discord.Interaction) -> None:
        """ Responds with the time it takes to send one message. """
        start = time.perf_counter()
        await itx.response.send_message("Pinging...")
        end = time.perf_counter()
        ping = (end - start) * 1000
        await itx.edit_original_response(content="Pong! {:.2f}ms".format(ping))

    @app_commands.command()
    async def server(self, itx: discord.Interaction) -> None:
        """ Responds with the link to the DAS' official server. """
        content = f"Join my official server! {info.SERVER}"
        await itx.response.send_message(content)

    @app_commands.command()
    async def vote(self, itx: discord.Interaction) -> None:
        """ Responds with the link to vote for DAS on Top.gg. """
        content = f"Vote for DAS on [Top.gg]({info.TOPGG}/vote)!"
        await itx.response.send_message(content)


async def setup(bot: commands.Bot) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Misc())
