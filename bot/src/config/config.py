""" Bot configuration """
import os

import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
IS_PRODUCTION = os.getenv('IS_PRODUCTION')
BOT_TOKEN = os.getenv('BOT_TOKEN')
TOPGG_TOKEN = os.getenv('TOPGG_TOKEN')
LOG_CHANNEL = os.getenv('LOG_CHANNEL')
STATS_CHANNEL = os.getenv('STATS_CHANNEL')
TEST_GUILD = os.getenv('TEST_GUILD')
API_URL = os.getenv('API_URL')

# Convert environment variables to the correct type
LOG_CHANNEL = int(LOG_CHANNEL) if LOG_CHANNEL else None
STATS_CHANNEL = int(STATS_CHANNEL) if STATS_CHANNEL else None
TEST_GUILD = discord.Object(TEST_GUILD) if TEST_GUILD else None

# Directory paths
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_DIR = os.path.abspath(os.path.join(CURR_DIR, '../..'))
COGS_DIR = os.path.abspath(os.path.join(BOT_DIR, 'src/cogs'))
SETTINGS_FILE = os.path.abspath(os.path.join(BOT_DIR, 'data/settings.json'))
STATS_FILE = os.path.abspath(os.path.join(BOT_DIR, 'data/stats.json'))
