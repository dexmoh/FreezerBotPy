import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands
from consts import menu_desc
from embed import create_embed
from buttons.menu_switcher_view import MenuSwitcherView


# *** UTILITY COMMANDS ***

# Help command that lists all of the bot's commands.
@commands.command(name="help", aliases=["commands", "info"])
async def help(ctx: discord.ext.commands.Context):
    embed = create_embed(
        ctx,
        title="Help menu!",
        desc=menu_desc["help"].format(name=ctx.bot.name, prefix=ctx.bot.command_prefix)
    )

    # Show privileged commands only to privileged users.
    if ctx.author.id in ctx.bot.user_whitelist:
        embed.description += menu_desc["help_privileged"].format(name=ctx.bot.name)

    # Create a button.
    view = MenuSwitcherView(ctx)
    for child in view.children:
        if isinstance(child, discord.ui.Button) and child.label == "Commands":
            child.style = discord.ButtonStyle.gray
            child.disabled = True
            break

    await ctx.send(embed=embed, view=view)


# Show bot's about page.
@commands.command(name="about", aliases=["aboutme", "github"])
async def about(ctx):
    embed = create_embed(
        ctx,
        title="About me!",
        desc=menu_desc["about"]
    )
    
    # Create a button.
    view = MenuSwitcherView(ctx)
    for child in view.children:
        if isinstance(child, discord.ui.Button) and child.label == "About":
            child.style = discord.ButtonStyle.gray
            child.disabled = True
            break

    await ctx.send(embed=embed, view=view)


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
