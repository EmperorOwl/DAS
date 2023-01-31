""" Code for miscellaneous commands. """

import sys
import time
import psutil
import discord
from discord import app_commands
from discord.ext import commands

from modules.bot import DAS


class Misc(commands.Cog):
    """ Represents a collection of miscellaneous commands. """

    def __init__(self, bot: DAS) -> None:
        """ Creates an instance of the cog. """
        self.bot = bot

    @app_commands.command()
    async def help(self, itx: discord.Interaction) -> None:
        """ Responds with a list of DAS' commands. """
        await itx.response.send_message(
            embed=discord.Embed(
                title="Help Page",
                url=self.bot['docs'],
                description=self.bot['description'],
                colour=discord.Colour.blue(),
                timestamp=discord.utils.utcnow()
            ).set_thumbnail(
                url=self.bot.user.avatar.url
            ).add_field(
                name="My Commands",
                value=(
                    """
                    `/display` - Display a function!
                    `/graph` - Plot a graph!
                    `/limit` - Find the limit of a function!
                    `/derive` - Derive a function!
                    `/integrate` - Integrate a function!
                    `/solve` - Solve an equation!
                    `/linsolve` - Solve a pair of linear equations!
                    `/expand` - Expand an expression!
                    `/factor` - Factor an expression!
                    `/simplify` - Simplify an expression!
                    `/calculate` - Evaluate an expression!
                    `/average` - Find the average of a list of numbers!
                    `/atr` - Toggle Automatic TeX Recognition (ATR)!
                    """
                ),
                inline=False
            ).add_field(
                name="Other Commands",
                value="`/about` `/invite` `/ping` `/server` `/vote`",
                inline=False
            ).set_footer(
                text=f"Developed by EmperorOwl • Version: {self.bot['version']}"
            )
        )

    @app_commands.command()
    async def about(self, itx: discord.Interaction) -> None:
        """ Responds with some facts about DAS. """
        await itx.response.send_message(
            embed=discord.Embed(
                title="About Me",
                description=(
                        f"{self.bot['description']}\n"
                        '\n'
                        f"`      Developer:` {self.bot['developer']}\n"
                        f"`        Servers:` {len(self.bot.guilds)}\n"
                        f"`          Users:` {self.bot.get_number_of_users()}\n"
                        f"`         Memory:` {psutil.virtual_memory().percent} %\n"
                        f"`      CPU Usage:` {psutil.cpu_percent(interval=1)} %\n"
                        f"`        Latency:` {int(self.bot.latency * 1000)} ms\n"
                        f"`    Bot Version:` {self.bot['version']}\n"
                        f"` Python Version:` {sys.version[:6]}\n"
                        f"`           Host:` {self.bot['host']}\n"
                        '\n'
                        f"[Top.gg Site]({self.bot['site']}) ~ " +
                        f"[Bot Invite]({self.bot['invite']}) ~ " +
                        f"[Server Invite]({self.bot['server']}) ~ " +
                        f"[Gitbook Docs]({self.bot['docs']}) ~ " +
                        f"[Github Repository]({self.bot['repo']})"
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
        await itx.edit_original_response(
            content="Pong! {:.2f}ms".format((end - start) * 1000)
        )

    @app_commands.command()
    async def invite(self, itx: discord.Interaction) -> None:
        """ Responds with the link to add DAS to another server. """
        await itx.response.send_message(
            embed=discord.Embed(
                title="Thanks for using DAS!",
                description=(
                    f"To add me to another server, click [here]({self.bot['invite']}).\n"
                    f"To join my official server, click [here]({self.bot['server']}).\n"
                    f"To support DAS on Top.gg, click [here]({self.bot['site']})."
                ),
                color=discord.Colour.blue()
            )
        )

    @app_commands.command()
    async def server(self, itx: discord.Interaction) -> None:
        """ Responds with the link to the DAS' official server. """
        await itx.response.send_message(f"Join my official server! {self.bot['server']}")

    @app_commands.command()
    async def vote(self, itx: discord.Interaction) -> None:
        """ Responds with the link to vote for DAS on Top.gg. """
        await itx.response.send_message(f"Vote for DAS on Top.gg! <{self.bot['site']}/vote>")


async def setup(bot: DAS) -> None:
    """ Adds the cog to the bot. """
    await bot.add_cog(Misc(bot), guild=bot.test_guild)
