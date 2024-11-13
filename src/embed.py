import discord
import discord.ext.commands

# A small function that creates a discord embed with most things we need.
# Saves us from writing a few extra lines of code in the command handler.
def create_embed(
        ctx: discord.ext.commands.Context,
        title: str = None,
        desc: str = None,
        thumbnail_url: str = "https://imgur.com/dRLQcoP.png",
        image_url: str = None,
        set_footer: bool = True
    ) -> discord.Embed:
    
    embed = discord.Embed(
        color=ctx.bot.color,
        title=title,
        description=desc
    )

    embed.set_thumbnail(url=thumbnail_url)
    embed.set_image(url=image_url)

    if set_footer:
        embed.set_footer(text=f'Requested by {ctx.author.name}.', icon_url=ctx.author.avatar.url)
    
    return embed
