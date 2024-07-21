""" Contains some constants for bot configuration. """
import discord

from frontend.utils import read_data_from_json_file

config = read_data_from_json_file('config/config.json')

IS_PRODUCTION = config['is_production']
BOT_TOKEN = config['bot_token']
TOPGG_TOKEN = config['topgg_token']
LOG_CHANNEL = config['log_channel']
STATS_CHANNEL = config['stats_channel']
TEST_GUILD = discord.Object(config['test_guild'])
