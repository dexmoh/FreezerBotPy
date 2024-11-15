from commands import utility
from commands import pin
from commands import chatbot
from commands import privileged
from discord.ext import commands


# All of the command methods must be registered before the bot can use them.
def register_commands(bot: commands.Bot):
    # We want to override the default help command.
    bot.remove_command("help")

    # Utility.
    bot.add_command(utility.help)
    bot.add_command(utility.about)
    bot.add_command(utility.bitch) # TODO: Rename to ping.

    # Pins.
    bot.add_command(pin.pin)
    bot.add_command(pin.search)
    bot.add_command(pin.list)

    # Chatbot.
    bot.add_command(chatbot.fact)

    # Privileged.
    bot.add_command(privileged.shutdown)
    bot.add_command(privileged.toggle_experimental)
