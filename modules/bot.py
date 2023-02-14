""" Code for defining the bot.

References:
    https://docs.top.gg/libraries/python/
    https://topggpy.readthedocs.io/en/stable/api.html

"""

import json
import platform

import psutil
import topgg
import discord
from discord.ext import commands


class DAS(commands.AutoShardedBot):
    """ Represents the bot DAS.

    constants:
        COGS: the locations of the bot's cogs
        CONFIG_FILE: the location of the bot's configuration file
        SETTINGS_FILE: the location of the settings file
        STATUS: the status text underneath the bot's name on Discord

    attributes:
        test_guild: the id of the test guild or None
        topggpy: the Topgg client

    """
    COGS = [
        'cogs.maths',
        'cogs.graph',
        'cogs.atr',
        'cogs.misc',
        'cogs.error',
        'cogs.dev'
    ]
    CONFIG_FILE = 'config.json'
    SETTINGS_FILE = 'settings.json'
    STATUS = '/help | 9+10=21!'

    def __init__(self) -> None:
        """ Creates an instance of DAS. """
        intents = discord.Intents.default()
        intents.message_content = True  # Enables bot to read Discord messages.
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            activity=discord.Game(name=DAS.STATUS)
        )
        self.test_guild = discord.Object(id=self['test_guild']) if self['test_guild'] else None
        self.topggpy = None
        self.start_time = discord.utils.utcnow()

    async def setup_hook(self) -> None:
        """ Enables asynchronous setup tasks to be run. """
        for cog in DAS.COGS:
            await self.load_extension(cog)
        # Initialise the Topgg client.
        self.topggpy = topgg.DBLClient(
            bot=self,
            token=self['topgg'],
            # Don't post guild and shard counts on development bot.
            autopost=False if self.test_guild else True,
            post_shard_count=False if self.test_guild else True
        )

    async def on_ready(self) -> None:
        """ Prints a message to indicate the bot is online. """
        print(f"Logged in as {self.user.name} - {self.user.id} - "
              f"{self.start_time.strftime('%H:%M')}")

    async def on_autopost_success(self) -> None:
        """ Prints a message to indicate bot has posted guild count. """
        print(f"Posted server count {self.topggpy.guild_count} guilds.")
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
        with open(DAS.CONFIG_FILE, 'r') as f:
            return json.load(f)[key]

    @staticmethod
    def get_atr_settings() -> dict:
        """ Returns the dictionary mapping guild id to ATR status. """
        with open(DAS.SETTINGS_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def edit_atr_settings(new_settings: dict) -> None:
        """ Updates the JSON file with the new ATR settings. """
        with open(DAS.SETTINGS_FILE, 'w') as f:
            json.dump(new_settings, f, indent=2)
