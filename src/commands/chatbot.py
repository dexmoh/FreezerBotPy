from discord.ext import commands
from embed import create_embed


# *** CHATBOT COMMANDS ***

# [EXPERIMENTAL] Generate a silly opossum fact.
@commands.command(name="fact", aliases=["facts"])
async def fact(ctx):
    if ctx.message.guild.id not in ctx.bot.server_whitelist:
        await ctx.send(
            embed=create_embed(
                ctx,
                desc="This discord server doesn't have access to experimental features.",
                thumbnail_url=None,
                set_footer=False
            )
        )
        return

    if not ctx.bot.experimental:
        await ctx.send(
            embed=create_embed(
                ctx,
                desc="Experimental features are currently disabled.",
                thumbnail_url=None,
                set_footer=False
            )
        )
        return

    embed = create_embed(
        ctx,
        title="COOL OPOSSUM FACT!",
        desc="This is a placeholder, you shouldn't be seeing this. If you're seeing this please don't. Thank you!" # TODO: Change this lol.
    )

    await ctx.send(embed=embed)
