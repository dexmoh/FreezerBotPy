from discord.ext import commands
import console
from embed import create_embed


# *** PRIVILEGED  COMMANDS ***

# Shut down the bot (you'll have to manually turn it back on).
@commands.command(name="shutdown")
async def shutdown(ctx):
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
        ctx.bot.pins.close()
    else:
        embed = create_embed(
            ctx,
            title="ACCESS DENIED",
            image_url="https://cdn.discordapp.com/attachments/764946979977297980/1261361149056778362/no-power.gif"
        )
        await ctx.send(embed=embed)


# Toggle experimental features off and on.
@commands.command(name="toggle_exp")
async def toggle_experimental(ctx):
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
