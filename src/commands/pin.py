import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands
from embed import create_embed
from buttons.pins_search_view import PinsSearchView
from difflib import SequenceMatcher
import random
import math
import re


# *** PIN COMMANDS ***

# Create a new pin.
@commands.command(name="pin")
async def pin(ctx: discord.ext.commands.Context, *, keyword: str = None):
    # Send help message.
    if not keyword or keyword.lower() == "help":
        embed = create_embed(
            ctx,
            title=f"Usage: `{ctx.bot.command_prefix}pin <keyword>`",
            desc=f"Reply to a message with this command to pin its attachments, so you can later access them with the keyword you've chosen.\n\nUse `{ctx.bot.command_prefix}search <keyword>` to look up saved pins.\n\nKeywords can contain spaces, emoji and special symbols, they can't be longer than 50 characters."
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


# Delete a saved pin.
@commands.command(name="delete", aliases=["unpin"])
async def delete(ctx, *, keyword: str = None):
    # Send help message.
    if not keyword or keyword.lower() == "help":
        await ctx.send(embed=create_embed(
                ctx,
                title=f"Usage: `{ctx.bot.command_prefix}delete <keyword>`",
                desc="Delete a saved pin."
            )
        )
        return
    
    # Check if the pin exists.
    if not ctx.bot.pins.get_pin_by_keyword(ctx.message.guild.id, keyword):
        await ctx.send(embed=create_embed(ctx, desc="That keyword doesn't exists.", thumbnail_url=None, set_footer=False))
        return
    
    ctx.bot.pins.delete_pin(ctx.message.guild.id, keyword)

    await ctx.send(embed=create_embed(
            ctx,
            desc=f"Successfully deleted '`{keyword}`'.",
            thumbnail_url=None,
            set_footer=False
        )
    )


# Search for a specific pin by keyword.
@commands.command(name="search", aliases=["lookup", "get", "show"])
async def search(ctx, *, keyword: str = None):
    # Send help message.
    if not keyword or keyword.lower() == "help":
        await ctx.send(embed=create_embed(
                ctx,
                title=f"Usage: `{ctx.bot.command_prefix}search <keyword>`",
                desc="Search for a saved pin by its keyword."
            )
        )
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
async def list(ctx: discord.ext.commands.Context, *, search_term: str = None):
    if search_term:
        search_term = search_term.lower()
    
    # Send help message.
    if search_term and search_term == "help":
        await ctx.send(embed=create_embed(
                ctx,
                title=f"Usage: `{ctx.bot.command_prefix}list <search-term (optional)>`",
                desc="List all of the pins, or narrow down the search by providing a search term."
            )
        )
        return
    
    pins = ctx.bot.pins.get_keywords_by_server_id(ctx.message.guild.id)
    if not pins:
        await ctx.send(embed=create_embed(
                ctx,
                desc="There are no pins. Go ahead and pin something with the `pin` command!",
                thumbnail_url=None,
                set_footer=False
            )
        )
        return
    
    filtered_pins = []
    title = "**Here's a list of all the pins!**"

    if not search_term:
        for pin in pins:
            filtered_pins.append(pin[0])
    else:
        # Search pins by keyword.
        title = f"**Pins that match '`{search_term}`':**"

        for pin in pins:
            pin_keyword = pin[0].lower()
            if search_term in pin_keyword:
                filtered_pins.append(pin[0])
            elif SequenceMatcher(None, search_term, pin_keyword).ratio() >= 0.75:
                filtered_pins.append(pin[0])
        
        if not filtered_pins:
            await ctx.send(embed=create_embed(
                    ctx,
                    desc=f"Haven't found any pins that match '`{search_term}`'.",
                    thumbnail_url=None,
                    set_footer=False
                )
            )
            return

    pins_per_page_limit = 10
    number_of_pages = math.ceil(len(filtered_pins) / pins_per_page_limit)
    desc_str = title

    # Show the first page of the pins.
    for index, pin in enumerate(filtered_pins):
        if index >= pins_per_page_limit:
            break

        desc_str += f"\n- {pin}"
    
    desc_str += f"\n\nPage 1/{number_of_pages}"

    # Create buttons.
    view = None
    if number_of_pages > 1:
        view = PinsSearchView(ctx, filtered_pins, 1, number_of_pages, pins_per_page_limit, title)

    await ctx.send(embed=create_embed(ctx, desc=desc_str), view=view)


# Send a random pin from the server.
@commands.command(name="random")
async def random_pin(ctx: discord.ext.commands.Context):
    pins = ctx.bot.pins.get_pins_by_server_id(ctx.message.guild.id)

    if not pins:
        await ctx.send(embed=create_embed(
                ctx,
                desc="There are no pins. Go ahead and pin something with the `pin` command!",
                thumbnail_url=None,
                set_footer=False
            )
        )
        return

    pin = random.choice(pins)

    channel_id = pin[0]
    message_id = pin[1]
    keyword = pin[2]
    urls = pin[3]

    await ctx.send(embed=create_embed(ctx, desc=f"**{keyword}**", thumbnail_url=None, set_footer=False))
    await ctx.send(urls)

    # If the channel and message IDs aren't null then we can create a link to the original message, quite fancy.
    if channel_id and message_id:
        await ctx.send(f"-# Found the original message: https://discord.com/channels/{ctx.message.guild.id}/{channel_id}/{message_id}")
