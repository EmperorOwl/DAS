""" Bot information """
import discord
import psutil
import typing
import platform

VERSION = '6.0.0'
DEV = 'EmperorOwl'
DOCS = "https://emperorowl.gitbook.io/das"
TOPGG = "https://top.gg/bot/863295366023086090"
REPO = "https://github.com/EmperorOwl/DAS"
SERVER = "https://discord.gg/Q3BMHGa8Wj"
DESC = ("The Discord Algebra System (DAS) is a minimalistic, yet powerful "
        "tool that acts as a Scientific Calculator, Graph Plotter and TeX "
        "Renderer, to enhance the study of mathematics in Discord.")
HOST = "GalaxyGate"
PY_VERSION = platform.python_version()
OS = f"{platform.system()} {platform.release()}"


def users(guilds: typing.Sequence[discord.Guild]) -> int:
    """ Returns the number of users the bot can see. """
    return sum(guild.member_count or 0 for guild in guilds)


def memory_usage() -> str:
    """ Returns the bot's memory usage in GB. """
    total = psutil.virtual_memory().total / (1 * 10 ** 9)
    used = psutil.virtual_memory().used / (1 * 10 ** 9)
    percentage = psutil.virtual_memory().percent
    return f"{used:.2f}GB used out of {total:.2f}GB ({percentage}%)"


def cpu_usage() -> str:
    """ Returns the bot's CPU usage. """
    return f"{psutil.cpu_percent()}%"
