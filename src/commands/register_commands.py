from discord.ext import commands
from commands import utility
from commands import pin
from commands import privileged


# All of the command methods must be registered before the bot can use them.
def register_commands(bot: commands.Bot):
    # We want to override the default help command.
    bot.remove_command("help")

    # Utility.
    bot.add_command(utility.help)
    bot.add_command(utility.about)
    bot.add_command(utility.roll)
    bot.add_command(utility.ping)
    bot.add_command(utility.insult)

    # Pins.
    bot.add_command(pin.pin)
    bot.add_command(pin.delete)
    bot.add_command(pin.search)
    bot.add_command(pin.list)
    bot.add_command(pin.random_pin)

    # Privileged.
    bot.add_command(privileged.shutdown)
