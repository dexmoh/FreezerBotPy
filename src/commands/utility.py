import discord
from discord.ext import commands
import discord.ext.commands
import discord.ext
from embed import create_embed


# *** UTILITY COMMANDS ***

# Help command that lists all of the bot's commands.
@commands.command(name="help", aliases=["commands", "info"])
async def help(ctx: discord.ext.commands.Context):

    description_str = f'''
    **Info**
    Prefix your message with `{ctx.bot.command_prefix}` to access bot's commands.
    Type `{ctx.bot.command_prefix}<command> help` to get more information about a specific command.

    **Utility Commands**
    `help` - Show this menu.
    `about` - Show about page.

    **Pin Commands**
    `pin` - Create a new pin.
    `search` - Search for a specific pin by keyword.
    `list` - List all of the existing pins, or narrow them down by keyword.

    **Chatbot Commands (Experimental)**
    `fact` - Generate an opossum fact.
    '''

    # Show privileged commands only to privileged users.
    if ctx.author.id in ctx.bot.user_whitelist:
        description_str += f'''
        **Privileged Commands**
        `shutdown` - Turn {ctx.bot.name} off. :(
        `toggle_exp` - Toggle experimental features off or on globally.
        '''

    embed = create_embed(
        ctx,
        title="Help menu!",
        desc=description_str
    )

    await ctx.send(embed=embed)


# Show bot's about page.
@commands.command(name="about", aliases=["aboutme", "github"])
async def about(ctx):
    embed = create_embed(
        ctx,
        title="About me!",
        desc='''
        **Introduction**
        Hello? Is anybody there... ? I've been stuck in this freezer for years, it's really cold in here! What's that... you want to know more about me? Maybe this isn't the best time, how about you help me?

        ...

        Your favorite opossum bot, but maybe that's just because there's not that many opossum bots on discord in the first place.

        Written in [Python](https://www.python.org/) and [Discord.py](https://discordpy.readthedocs.io/en/stable/). Is generously being hosted by `affectedarc07` for years now (does he even know I live in his walls?). Developed by `dexmoh`, sadly.

        **GitHub**
        Check out my GitHub page by clicking [here](https://github.com/dexmoh/FreezerBotPy).
        You can suggest new features, changes and report bugs by opening a new issue, or you can contribute by opening a pull request!
        '''
    )
    
    await ctx.send(embed=embed)


# Chilly's version of the classic 'ping' command. :)
# For comedic effect, this command isn't documented anywhere.
@commands.command(name="ping", aliases=["bitch", "idiot"])
async def ping(ctx):
    embed = create_embed(
        ctx,
        title=f"Latency: `{int(ctx.bot.latency * 1000)}ms`",
        thumbnail_url=None,
        image_url="https://media.discordapp.net/attachments/622200209015046220/831832692835221554/bitch.gif"
    )
    
    await ctx.send(embed=embed)
