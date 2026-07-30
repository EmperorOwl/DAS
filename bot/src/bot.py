""" Code for the bot. """
import logging
import os
import aiohttp
import topgg
import discord
from discord.ext import commands

from src.api import init_session
from src.config import IS_PRODUCTION, BOT_TOKEN, TOPGG_TOKEN, COGS_DIR
from src.utils import pretty_uptime

log = logging.getLogger(__name__)

BotBase = commands.AutoShardedBot if IS_PRODUCTION else commands.Bot


class DAS(BotBase):  # type: ignore
    """ Represents the bot DAS. """
    ERR_COG = 'Error'

    def __init__(self) -> None:
        """ Creates an instance of DAS. """
        # Set up intents.
        intents = discord.Intents.default()
        intents.message_content = True  # Enables the bot to read messages.
        # Call super.
        super().__init__(command_prefix=commands.when_mentioned,
                         intents=intents)
        # Define some attributes to be initialised later.
        self.topgg_client = None
        self.start_time = None
        self.http_session = None

    async def setup_hook(self) -> None:
        """ Enables asynchronous setup tasks to be run. """
        # Set up shared HTTP session
        self.http_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
        )
        init_session(self.http_session)
        # Dynamically load all the cogs.
        for file in os.listdir(COGS_DIR):
            if not file.startswith('__'):
                cog = f"src.cogs.{file.replace('.py', '')}"
                await self.load_extension(cog)
        # Set up Topgg client
        if TOPGG_TOKEN:
            self.topgg_client = topgg.DBLClient(  # type: ignore
                bot=self,
                token=TOPGG_TOKEN,
                # Do not autopost server and shard count on dev bot.
                autopost=True if IS_PRODUCTION else False,
                post_shard_count=True if IS_PRODUCTION else False
            )

    async def on_ready(self) -> None:
        """ Logs a message to indicate the bot is online. """
        self.start_time = discord.utils.utcnow()
        log.info("Logged in as %s (%s) - %s - %s",
                 self.user.name, BotBase.__name__, self.user.id,
                 self.start_time.strftime('%H:%M'))
        # Attach the error handler to the bot
        self.tree.on_error = self.get_cog(self.ERR_COG).on_app_command_error

    async def on_autopost_success(self) -> None:
        """ Logs a message to indicate bot has posted guild count. """
        if not self.topgg_client:
            raise ValueError("Topgg client is not set")
        log.info("Posted server count %s guilds.", self.topgg_client.guild_count)
        log.info("Posted shard count %s shards.", self.shard_count)

    def get_uptime(self) -> str:
        """ Returns the time the bot has been up. """
        if not self.start_time:
            raise ValueError("Bot has not started")
        uptime = (discord.utils.utcnow() - self.start_time).total_seconds()
        return pretty_uptime(uptime)

    async def close(self) -> None:
        """ Closes the shared HTTP session and shuts down the bot. """
        if self.http_session:
            await self.http_session.close()
        await super().close()

    def run(self) -> None:
        """ Starts the bot. """
        if not BOT_TOKEN:
            raise ValueError("BOT_TOKEN is not set")
        # root_logger=True so src.* loggers (not just discord.*) are visible.
        super().run(BOT_TOKEN, root_logger=True)
