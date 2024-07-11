import discord
from discord.ext import commands
import console


# Our bot's prefix (case sensitive).
prefix = 'poss '

# The color and the name we'll use in bot's embeds.
color = 0x1ABC9C
name = 'Chilly'

# Setup intents.
intents = discord.Intents.default()
intents.message_content = True

# Create our bot object.
bot = commands.Bot(command_prefix=prefix, intents=intents)

# Flag we'll use to check whether the bot should use experimental features.
experimental = True


# This method runs when the bot connects for the first time.
@bot.event
async def on_ready():
    console.log(f'Logged in as {bot.user} (ID: {bot.user.id}).')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name='WAAAAAHH'
        )
    )
