""" Code for running the Discord bot. """

from modules.bot import DAS

bot = DAS()
bot.run(token=bot['token'], reconnect=True)
