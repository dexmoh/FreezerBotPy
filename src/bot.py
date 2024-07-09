import time
import discord
from discord.ext import commands
import whitelist
import console

# Our bot's prefix (case sensitive).
BOT_PREFIX = 'poss '

# Setup intents.
intents = discord.Intents.default()
intents.message_content = True

# Create our bot object.
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


# *** COMMANDS ***

# Chilly's version of the classic 'ping' command. :)
# For comedic effect, this command isn't documented anywhere.
@bot.command()
async def bitch(ctx):
    await ctx.send('https://media.discordapp.net/attachments/622200209015046220/831832692835221554/bitch.gif')


# Privileged command that lets whitelisted users shutdown the bot.
@bot.command()
async def shutdown(ctx):
    async with ctx.channel.typing():
        time.sleep(0.8)

        # Check if the user has access to this command.
        if ctx.author.id in whitelist.user_whitelist:
            console.log(f'User {ctx.author.name} (ID: {ctx.author.id}) invoked the shutdown command.')
            await ctx.send('Shutting down... :(')
            await ctx.send('https://cdn.discordapp.com/attachments/805603157484503046/1260199089686056971/yes-power.gif')
            await ctx.bot.close()
        else:
            await ctx.send('https://tenor.com/view/lotr-lord-of-the-rings-theoden-king-of-rohan-you-have-no-power-here-gif-4952489')
