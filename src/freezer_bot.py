import discord
from discord.ext import commands
from commands.register_commands import register_commands
import console
from pins import PinsDB
from chatbot import ChatBot


class FreezerBot(commands.Bot):
    def __init__(self, prefix, name, color, intents, user_whitelist_path, *args, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents, *args, **kwargs)

        # Our bot's name and color (used in embeds).
        self.name = name
        self.color = color

        # List of user IDs that can use privileged commands.
        self.user_whitelist = []
        try:
            with open(user_whitelist_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.split("#")[0].strip()

                    if line:
                        try:
                            id = int(line)
                            self.user_whitelist.append(id)
                        except ValueError:
                            console.log(f"Couldn't convert one of the IDs in '{user_whitelist_path}' file into a number. All of the IDs must be numbers.", console.Level.ERROR)
        except FileNotFoundError:
            console.log(f"The '{user_whitelist_path}' file doesn't exist. The user whitelist will be empty.", console.Level.WARNING)
            self.user_whitelist = []

        # Object we'll use to handle interactions with the pins database.
        self.pins = PinsDB(".data/pins.db")

        # Markov chain text generation.
        self.chatbot = ChatBot(".data/chatbot_data.json")

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
    
    # This method runs every time someone sends a message.
    async def on_message(self, message: discord.Message):
        # Reply to bot mentions with a randomly generated line.
        if self.user.mentioned_in(message) and not message.author.bot:
            reply = self.chatbot.generate_line()
            if reply:
                await message.channel.send(reply, reference=message, mention_author=False)
        
        return await super().on_message(message)
