""" Contains code to restrict input lengths. """
from discord import app_commands

CharLim1 = app_commands.Range[str, 1, 1]
CharLim25 = app_commands.Range[str, 1, 25]
CharLim50 = app_commands.Range[str, 1, 50]
