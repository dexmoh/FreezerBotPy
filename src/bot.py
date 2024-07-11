import discord
from discord.ext import commands


# Our bot's prefix (case sensitive).
prefix = 'poss '

# Setup intents.
intents = discord.Intents.default()
intents.message_content = True

# Create our bot object.
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Flag we'll use to check whether the bot should use experimental features.
experimental = False
