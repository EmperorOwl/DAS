""" Code for defining the bot. """

import platform
import psutil
import topgg
import discord
from discord.ext import commands
from pathlib import Path

from modules.utils import read_data_from_json_file

CONFIG_FILE = 'config.json'
config = read_data_from_json_file(CONFIG_FILE)
IS_PRODUCTION = config['is_production']
BOT_TOKEN = config['bot_token']
TOPGG_TOKEN = config['topgg_token']
TEST_GUILD = config['test_guild']
RENDERS_PATH = Path(__file__).resolve().parent.parent / "renders"


class DAS(commands.AutoShardedBot if IS_PRODUCTION else commands.Bot):
    """ Represents the bot DAS.

    Attributes:
        COGS: the locations of the bot's cogs
        INFO_FILE: the location of the bot's info file
        SETTINGS_FILE: the location of the settings file
        STATS_FILE: the location of the bot's stats file
        test_guild: the id of the test guild or None
        topgg_client: the Topgg client or None
        start_time: the time the bot came online
    """
    COGS = [
        'cogs.maths',
        'cogs.graph',
        'cogs.atr',
        'cogs.misc',
        'cogs.error',
        'cogs.dev'
    ]
    INFO_FILE = 'info.json'
    SETTINGS_FILE = 'settings.json'
    STATS_FILE = 'stats.json'

    def __init__(self) -> None:
        """ Creates an instance of DAS. """
        intents = discord.Intents.default()
        intents.message_content = True  # Enables the bot to read messages.
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            activity=discord.Game(name=self['status'])
        )
        # Define some attributes to be initialised later.
        self.topgg_client = None
        self.start_time = None
        # Initialise test_guild.
        if IS_PRODUCTION:
            self.test_guild = None
        elif TEST_GUILD is None:
            raise ValueError("development bot must define test_guild in "
                             "configuration file")
        else:
            self.test_guild = discord.Object(id=TEST_GUILD)
        # Create /renders directory if not already there.
        if not RENDERS_PATH.exists():
            RENDERS_PATH.mkdir()

    async def setup_hook(self) -> None:
        """ Enables asynchronous setup tasks to be run. """
        for cog in DAS.COGS:
            await self.load_extension(cog)
        # Set up Topgg client.
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

    async def on_autopost_success(self) -> None:
        """ Prints a message to indicate bot has posted guild count. """
        print(f"Posted server count {self.topgg_client.guild_count} guilds.")
        print(f"Posted shard count {self.shard_count} shards.")

    def get_number_of_users(self) -> int:
        """ Returns the number of users the bot can see. """
        users = 0
        for guild in self.guilds:
            users += guild.member_count  # Likely results in double-counting.
        return users

    def get_uptime(self) -> str:
        """ Returns the bot's uptime. """
        seconds = (discord.utils.utcnow() - self.start_time).total_seconds()
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return f"{days:.0f}d, {hours:.0f}h, {minutes:.0f}m and {seconds:.0f}s"

    @staticmethod
    def get_memory_usage() -> str:
        """ Returns the bot's memory usage in GB. """
        total = psutil.virtual_memory().total / (1 * 10 ** 9)
        used = psutil.virtual_memory().used / (1 * 10 ** 9)
        percentage = psutil.virtual_memory().percent
        return f"{used:.2f}GB used out of {total:.2f}GB ({percentage}%)"

    @staticmethod
    def get_cpu_usage() -> str:
        """ Returns the bot's CPU usage. """
        return f"{psutil.cpu_percent()}%"

    @staticmethod
    def get_py_version() -> str:
        """ Returns the Python version. """
        return platform.python_version()

    @staticmethod
    def get_platform() -> str:
        """ Returns the bot's OS. """
        return f"{platform.system()} {platform.release()}"

    def get_app_command(self, name) -> commands.Command:
        """ Returns a standalone application command. """
        return self.tree.get_command(name, guild=self.test_guild)

    def get_nested_app_command(self, full_name: str) -> commands.Command:
        """ Returns a nested application command. """
        group, subgroup, name = full_name.split(' ')
        return self.tree.get_command(
            group, guild=self.test_guild
        ).get_command(subgroup).get_command(name)

    @staticmethod
    def get_original_inputs(itx: discord.Interaction) -> dict:
        """ Returns the original inputs of an application command. """
        if 'graph' in itx.command.qualified_name:
            data = itx.data['options'][0]['options'][0]['options']
        else:
            data = itx.data['options']
        return {arg['name']: arg['value'] for arg in data}

    def __getitem__(self, key: str) -> str:
        """ Returns information about the bot depending on a key.  """
        return read_data_from_json_file(DAS.INFO_FILE)[key]
