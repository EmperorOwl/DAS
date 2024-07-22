""" Code for the bot. """
import os
import topgg
import discord
from discord.ext import commands

from frontend.config import IS_PRODUCTION, TEST_GUILD, BOT_TOKEN, TOPGG_TOKEN
from frontend.utils import pretty_uptime


class DAS(commands.AutoShardedBot if IS_PRODUCTION else commands.Bot):
    """ Represents the bot DAS. """
    COGS_DIR = 'frontend/cogs'
    ERR_COG = 'Error'

    def __init__(self) -> None:
        """ Creates an instance of DAS. """
        if not IS_PRODUCTION and TEST_GUILD is None:
            raise Exception("test_guild must be defined for dev bot")
        # Set up intents.
        intents = discord.Intents.default()
        intents.message_content = True  # Enables the bot to read messages.
        # Call super.
        super().__init__(command_prefix=commands.when_mentioned,
                         intents=intents)
        # Define some attributes to be initialised later.
        self.topgg_client = None
        self.start_time = None

    async def setup_hook(self) -> None:
        """ Enables asynchronous setup tasks to be run. """
        # Dynamically load all the cogs.
        for file in os.listdir(self.COGS_DIR):
            if not file.startswith('__'):
                cog = f"frontend.cogs.{file.replace('.py', '')}"
                await self.load_extension(cog)
        # Set up Topgg client
        if TOPGG_TOKEN:
            self.topgg_client = topgg.DBLClient(
                bot=self,
                token=TOPGG_TOKEN,
                # Do not autopost server and shard count on dev bot.
                autopost=True if IS_PRODUCTION else False,
                post_shard_count=True if IS_PRODUCTION else False
            )

    async def on_ready(self) -> None:
        """ Prints a message to indicate the bot is online. """
        self.start_time = discord.utils.utcnow()
        print(f"Logged in as {self.user.name} - {self.user.id} - "
              f"{self.start_time.strftime('%H:%M')}")
        # Attach the error handler to the bot
        self.tree.on_error = self.get_cog(self.ERR_COG).on_app_command_error

    async def on_autopost_success(self) -> None:
        """ Prints a message to indicate bot has posted guild count. """
        print(f"Posted server count {self.topgg_client.guild_count} guilds.")
        print(f"Posted shard count {self.shard_count} shards.")

    def get_uptime(self) -> str:
        """ Returns the time the bot has been up. """
        uptime = (discord.utils.utcnow() - self.start_time).total_seconds()
        return pretty_uptime(uptime)

    def run(self) -> None:
        """ Starts the bot. """
        super().run(BOT_TOKEN)
