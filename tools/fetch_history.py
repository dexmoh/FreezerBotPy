# Fetch message history from a guild. The bot has to be part of the guild.

import os
import json
import discord
from discord.ext import commands


GUILD_ID: int = 999999999999999999
OUTPUT_PATH: str = ".data/message_history.json"

discord_token_env = os.environ.get("FREEZER_BOT_DISCORD_TOKEN", "")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found.")
        return
    
    message_data = {}

    for channel in guild.channels:
        # Check if the channel is a TextChannel.
        if isinstance(channel, discord.TextChannel):
            message_data[channel.name] = []
            print(f"Fetching messages from #{channel.name}...")

            try:
                async for message in channel.history(limit=None):
                    if not message.author.bot:
                        message_data[channel.name].append((message.author.name, message.content))
            except discord.Forbidden:
                print(f"Cannot access messages in #{channel.name}.")
            except Exception as e:
                print(f"An error occurred in #{channel.name}: {e}")
    
    # Save this to a json file.
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(message_data, f)

    print("Done!")

bot.run("token")
