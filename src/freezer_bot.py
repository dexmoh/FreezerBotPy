import discord
from discord.ext import commands
import command_handler as ch
import console


class FreezerBot(commands.Bot):
    def __init__(self, prefix, name, color, intents, *args, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents, *args, **kwargs)

        # Our bot's name and color (used in embeds).
        self.name = name
        self.color = color

        # Flag we'll use to check whether the bot should use experimental features.
        self.experimental = True

        ch.register_commands(self)
    
    # This method runs when the bot connects for the first time.
    async def on_ready(self):
        console.log(f"Logged in as {self.user} (ID: {self.user.id}).")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="WAAAAAHH"
            )
        )
