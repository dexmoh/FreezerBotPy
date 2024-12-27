import discord
from discord.ext import commands
from commands.register_commands import register_commands
import console
from pins import PinsDB
from chatbot import ChatBot
import random
import json


class FreezerBot(commands.Bot):
    def __init__(self, prefix, name, color, intents, *args, **kwargs):
        super().__init__(command_prefix=prefix, intents=intents, *args, **kwargs)

        # Our bot's name and color (used in embeds).
        self.name = name
        self.color = color

        # Dictionary containing lists of user and server IDs.
        # Users on this list can use privileged commands.
        # Servers on this list will included in chatbot training.
        self.whitelist: dict[str, list[int]] = {}
        try:
            with open(".data/whitelist.json", "r") as json_file:
                self.whitelist = json.load(json_file)
        except Exception:
            console.log(f"The '.data/whitelist.json' file doesn't exist, or it isn't formatted correctly. The user and server whitelists will be empty.", console.Level.WARNING)
            self.whitelist = {
                "servers": [],
                "users": []
            }

        # Object we'll use to handle interactions with the pins database.
        self.pins = PinsDB(".data/pins.db")

        # Markov chain text generation.
        self.chatbot = ChatBot()

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
        # There is 1 in 600 chance for the bot to say something at random.
        if random.randint(1, 600) == 1:
            reply = self.chatbot.generate_line()
            if reply:
                await message.channel.send(reply)

        # Ignore bots.
        if message.author.bot:
            return await super().on_message(message)

        # Reply to bot mentions with a randomly generated line.
        if self.user.mentioned_in(message):
            reply = self.chatbot.generate_line()
            if not reply:
                reply = "hi!"
            await message.channel.send(reply, reference=message, mention_author=False)
        # Try to train the chatbot if the message is from a whitelisted server.
        elif message.guild.id in self.whitelist["servers"]:
            self.chatbot.learn(message.content)
        
        return await super().on_message(message)
