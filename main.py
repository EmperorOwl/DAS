""" Code for running the Discord bot. """

from modules.bot import DAS, BOT_TOKEN

bot = DAS()
bot.run(token=BOT_TOKEN, reconnect=True)
