from functools import wraps
from discord import app_commands


def allow_anywhere(func):
    """ Enables an application command to be used anywhere in Discord. """

    @wraps(func)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
