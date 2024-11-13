import discord
from discord.ext import commands
import discord.ext.commands
import console
import discord.ext
from embed import create_embed
import re
from difflib import SequenceMatcher


# All of the command methods must be registered before the bot can use them.
def register_commands(bot: commands.Bot):
    # We want to override the default help command.
    bot.remove_command("help")

    # Pins.
    bot.add_command(_pin)
    bot.add_command(_search)
    bot.add_command(_list)

    # Chatbot.
    bot.add_command(_fact)

    # Utility.
    bot.add_command(_help)
    bot.add_command(_about)
    bot.add_command(_bitch)

    # Privileged.
    bot.add_command(_shutdown)
    bot.add_command(_toggle_experimental)


# *** PIN COMMANDS ***

# Create a new pin.
@commands.command(name="pin")
async def _pin(ctx: discord.ext.commands.Context, *, keyword: str = None):
    if not keyword or keyword == "help":
        # Send help message that explains the pin command.
        embed = create_embed(
            ctx,
            title="Usage: `poss pin <keyword>`",
            desc="Reply to a message with this command to pin its attachments, so you can later access them with the keyword you've chosen.\n\nUse `poss search <keyword>` to look up saved pins.\n\nKeywords can contain spaces, emoji and special symbols, they can't be longer than 50 characters."
        )

        await ctx.send(embed=embed)
        return
    
    msg = ctx.message

    # Check if message is a reply, if it is we'll search it for attachments and embeds, otherwise we'll search the message of whoever invoked this command.
    if ctx.message.reference:
        try:
            msg = await ctx.fetch_message(ctx.message.reference.message_id)
        except Exception as e:
            # TODO: Log this to console.
            embed = create_embed(
                ctx,
                desc="Uh oh, something went wrong. I couldn't fetch the message you were replying to.",
                thumbnail_url=None,
                set_footer=False
            )
            await ctx.send(embed=embed)
            return
    else:
        # If the message isn't a reply then we'll search the message of whoever invoked this command, but this is slightly tricky thought because the embed links
        # could be part of the keyword. So we'll have to sanitize the keyword first to make sure there aren't any links in it. We'll use regex for this.
        match = re.match(r'(.*?)(https?://.*)', keyword)
        if match:
            keyword = match.group(1).strip()

    if len(keyword) > 50:
        embed = create_embed(
            ctx,
            desc="The keyword can't be more than 50 characters long.",
            thumbnail_url=None,
            set_footer=False
        )

        await ctx.send(embed=embed)
        return

    # Check if the keyword already exists.
    if ctx.bot.pins.get_pin_by_keyword(ctx.message.guild.id, keyword):
        await ctx.send(embed=create_embed(ctx, desc="That keyword already exists.", thumbnail_url=None, set_footer=False))
        return
    
    urls = ""
    url_count = 0
    for embed in msg.embeds:
        if embed.url:
            urls += embed.url + " "
            url_count += 1
    
    for attachment in msg.attachments:
        if attachment.url:
            urls += attachment.url + " "
            url_count += 1
    
    if url_count < 1:
        await ctx.send(embed=create_embed(ctx, desc="The message has no attachments.", thumbnail_url=None, set_footer=False))
        return
    
    ctx.bot.pins.add_pin(
        keyword=keyword,
        urls=urls,
        url_count=url_count,
        server_id=ctx.guild.id,
        channel_id=ctx.channel.id,
        message_id=msg.id
    )

    await ctx.send(embed=create_embed(ctx, title="Pinned!", desc=f"You can type `poss search {keyword}` to look up the pinned files."))


# Search for a specific pin by keyword.
@commands.command(name="search", aliases=["lookup", "get", "show"])
async def _search(ctx, *, keyword: str = None):
    if not keyword or keyword == "help":
        # Send help message that explains the search command.
        embed = create_embed(
            ctx,
            title="Usage: `poss search <keyword>`",
            desc="Search for a saved pin by its keyword."
        )

        await ctx.send(embed=embed)
        return
    
    pin = ctx.bot.pins.get_pin_by_keyword(ctx.message.guild.id, keyword)
    if not pin:
        # TODO: Instead of just telling the user that there's no such keyword, implement some way to search for similar sounding pins.
        embed = create_embed(ctx, desc="That keyword doesn't exist.", thumbnail_url=None, set_footer=False)
        await ctx.send(embed=embed)
        return
    
    channel_id = pin[0][0]
    message_id = pin[0][1]
    urls = pin[0][2]

    await ctx.send(embed=create_embed(ctx, desc=f"**{keyword}**", thumbnail_url=None, set_footer=False))
    await ctx.send(urls)

    # If the channel and message IDs aren't null then we can create a link to the original message, quite fancy.
    if channel_id and message_id:
        await ctx.send(f"-# Found the original message: https://discord.com/channels/{ctx.message.guild.id}/{channel_id}/{message_id}")


# List all of the server pins. User can narrow down searches by entering a keyword.
@commands.command(name="list", aliases=["pins"])
async def _list(ctx: discord.ext.commands.Context, *, keyword: str = None):
    if keyword and keyword == "help":
        # Send help message that explains the search command.
        embed = create_embed(
            ctx,
            title="Usage: `poss list <search-term (optional)>`",
            desc="List all of the pins, or narrow down the search by providing a search term."
        )

        await ctx.send(embed=embed)
        return
    
    pins = ctx.bot.pins.get_pins_by_server_id(ctx.message.guild.id)
    if not pins:
        embed = create_embed(ctx, desc="There are no pins. Go ahead and pin something with the `pin` command!", thumbnail_url=None, set_footer=False)
        await ctx.send(embed=embed)
        return

    # TODO: Implement a way to list through pins by reacting to the message.
    if not keyword:
        desc_str = "**Here's a list of all the pins!**"

        for pin in pins:
            desc_str += f"\n- {pin[2]}"

        await ctx.send(embed=create_embed(ctx, desc=desc_str))
        return
    else:
        # Search pins by keyword.
        desc_str = f"**Pins that match '`{keyword}`':**"
        counter = 0
        for pin in pins:
            pin_keyword = pin[2]
            if keyword in pin_keyword:
                desc_str += f"\n- {pin_keyword}"
                counter += 1
            elif SequenceMatcher(None, keyword, pin_keyword).ratio() >= 0.8:
                desc_str += f"\n- {pin_keyword}"
                counter += 1
        
        if counter == 0:
            await ctx.send(embed=create_embed(ctx, desc=f"Haven't found any pins that match '`{keyword}`'.", thumbnail_url=None))
            return

        await ctx.send(embed=create_embed(ctx, desc=desc_str))


# *** CHATBOT COMMANDS ***

# [EXPERIMENTAL] Generate a silly opossum fact.
@commands.command(name="fact", aliases=["facts"])
async def _fact(ctx):
    if ctx.message.guild.id not in ctx.bot.server_whitelist:
        embed = create_embed(ctx, desc="This discord server doesn't have access to experimental features.", thumbnail_url=None)
        await ctx.send(embed=embed)
        return

    if not ctx.bot.experimental:
        embed = create_embed(ctx, desc="Experimental features are currently disabled.", thumbnail_url=None)
        await ctx.send(embed=embed)
        return

    embed = create_embed(
        ctx,
        title="COOL OPOSSUM FACT!",
        desc="This is a placeholder, you shouldn't be seeing this. If you're seeing this please don't. Thank you!" # TODO: Change this lol.
    )

    await ctx.send(embed=embed)


# *** UTILITY COMMANDS ***

# Help command that lists all of the bot's commands.
@commands.command(name="help", aliases=["commands", "info"])
async def _help(ctx: discord.ext.commands.Context):

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
async def _about(ctx):
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
@commands.command(name="bitch")
async def _bitch(ctx):
    embed = create_embed(
        ctx,
        title=f"Latency: `{int(ctx.bot.latency * 1000)}ms`",
        image_url="https://media.discordapp.net/attachments/622200209015046220/831832692835221554/bitch.gif"
    )
    
    await ctx.send(embed=embed)


# *** PRIVILEGED  COMMANDS ***

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
