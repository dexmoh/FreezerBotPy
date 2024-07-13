import discord
from discord.ext import commands
import console
from embed import create_embed


# All of the command methods must be registered before the bot can use them.
def register_commands(bot: commands.Bot):
    bot.add_command(_fact)
    bot.add_command(_bitch)
    bot.add_command(_shutdown)
    bot.add_command(_toggle_experimental)


# *** COMMANDS ***

# [EXPERIMENTAL] Generate a silly opossum fact.
@commands.command(name="fact", aliases=["facts"])
async def _fact(ctx):
    if ctx.message.guild.id not in ctx.bot.server_whitelist:
        embed = create_embed(ctx, desc="This discord server doesn't have access to experimental features.")
        await ctx.send(embed=embed)
        return

    if not ctx.bot.experimental:
        embed = create_embed(ctx, desc="Experimental features are currently disabled.")
        await ctx.send(embed=embed)
        return

    embed = create_embed(
        ctx,
        title="COOL OPOSSUM FACT!",
        desc="This is a placeholder, you shouldn't be seeing this. If you're seeing this please don't. Thank you!",
        thumbnail_url="https://imgur.com/dRLQcoP.png"
    )
    await ctx.send(embed=embed)


# Chilly's version of the classic 'ping' command. :)
# For comedic effect, this command isn't documented anywhere.
@commands.command(name="bitch")
async def _bitch(ctx):
    await ctx.send("https://media.discordapp.net/attachments/622200209015046220/831832692835221554/bitch.gif")


# *** PRIVILEGED COMMANDS ***

# Shut down the bot (you'll have to manually turn it back on).
@commands.command(name="shutdown")
async def _shutdown(ctx):
    # Check if the user has access to this command.
    if ctx.author.id in ctx.bot.user_whitelist:
        console.log(f"User {ctx.author.name} (ID: {ctx.author.id}) invoked the shutdown command.")

        embed = create_embed(
            ctx,
            title="Shutting down...",
            image_url="https://cdn.discordapp.com/attachments/805603157484503046/1260199089686056971/yes-power.gif"
        )
        await ctx.send(embed=embed)

        await ctx.bot.close()
    else:
        embed = create_embed(
            ctx,
            title="ACCESS DENIED",
            image_url="https://cdn.discordapp.com/attachments/764946979977297980/1261361149056778362/no-power.gif"
        )
        await ctx.send(embed=embed)


# Toggle experimental features off and on.
@commands.command(name="toggle_exp")
async def _toggle_experimental(ctx):
    embed = create_embed(ctx)

    if ctx.author.id in ctx.bot.user_whitelist:
        ctx.bot.experimental = not ctx.bot.experimental

        if ctx.bot.experimental:
            console.log(f"User {ctx.author.name} (ID: {ctx.author.id}) enabled experimental features.")
            embed.description = "Experimental features are now **enabled**."
        else:
            console.log(f"User {ctx.author.name} (ID: {ctx.author.id}) disabled experimental features.")
            embed.description = "Experimental features are now **disabled**."

        await ctx.send(embed=embed)
    else:
        embed.description = "You don't have access to this command."
        await ctx.send(embed=embed)
