import discord
from discord.ext import commands
from commands.register_commands import register_commands
import console
import whitelist
from pins import PinsDB


class FreezerBot(commands.Bot):
    def __init__(self, prefix, name, color, intents, user_whitelist_path, server_whitelist_path, *args, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents, *args, **kwargs)

        # Our bot's name and color (used in embeds).
        self.name = name
        self.color = color

        # List of user IDs that can use privileged commands.
        self.user_whitelist = whitelist.read_wl_file(user_whitelist_path)

        # List of server IDs that can access bot's experimental features.
        self.server_whitelist = whitelist.read_wl_file(server_whitelist_path)

        # Flag we'll use to check whether the bot should use experimental features.
        self.experimental = True

        # Object we'll use to handle interactions with the pins database.
        self.pins = PinsDB(".data/pins.db")

        register_commands(self)
    
    # This method runs when the bot connects for the first time.
    async def on_ready(self):
        console.log(f"Logged in as {self.user} (ID: {self.user.id}).")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="WAAAAAHH"
            )
        )
