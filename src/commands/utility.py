import re
import random
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
        desc=menu_desc["help"].format(name=ctx.bot.name, prefix=ctx.bot.command_prefix[0])
    )

    # Show privileged commands only to privileged users.
    if ctx.author.id in ctx.bot.whitelist["users"]:
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


# Roll a dice.
# TODO: Implement a button that lets you reroll again, maybe?
@commands.command(name="roll")
async def roll(ctx, roll_str: str = ""):
    input_match = re.fullmatch(r"(\d*)d(\d+)", roll_str)
    if not input_match:
        # Show help menu that explains the roll command.
        embed = create_embed(
            ctx,
            title=f"Usage: `{ctx.bot.command_prefix[0]}roll <XdY>`",
            desc=f"Use `{ctx.bot.command_prefix[0]}roll <XdY>` where X is the number of dice and Y is the number of the sides.\n\nExample: `{ctx.bot.command_prefix[0]}roll 2d20`"
        )

        await ctx.send(embed=embed)
        return

    # Number of dice and sides we got from the command.
    num_dice = int(input_match.group(1)) if input_match.group(1) else 1 # Default to 1 die if not specified.
    num_sides = int(input_match.group(2))

    if num_dice < 1 or num_dice > 100:
        embed = create_embed(
            ctx,
            desc="You can't roll less than 1 die, or more than 100.",
            thumbnail_url=None,
            set_footer=False
        )

        await ctx.send(embed=embed)
        return
    
    if num_sides < 2:
        embed = create_embed(
            ctx,
            desc="Die can't have less than 2 sides.",
            thumbnail_url=None,
            set_footer=False
        )

        await ctx.send(embed=embed)
        return
    
    if num_sides > 1000000000:
        embed = create_embed(
            ctx,
            desc="Could you imagine if a die could have that many sides?",
            thumbnail_url=None,
            set_footer=False
        )

        await ctx.send(embed=embed)
        return

    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    
    embed = create_embed(
        ctx,
        desc=f"**Rolling {roll_str}:**\n{rolls}\n\n(Total: {sum(rolls)})",
        thumbnail_url=None
    )

    await ctx.send(embed=embed)


# The ping command, show the current latency of the bot.
# NOTE: I'm actually unsure how accurate this is.
@commands.command(name="ping")
async def ping(ctx):
    await ctx.send(
        embed=create_embed(
            ctx,
            title=f"Latency: `{int(ctx.bot.latency * 1000)}ms`",
            thumbnail_url=None,
            set_footer=False
        )
    )


# Chilly's secret feature.
@commands.command(name="bitch", aliases=["idiot"])
async def insult(ctx):
    await ctx.send("https://media.discordapp.net/attachments/622200209015046220/831832692835221554/bitch.gif")
