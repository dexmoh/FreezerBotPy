import os
import console
import discord
import freezer_bot


# Entry point.
def main():
    # Configure logging.
    console.init()

    # Fetch env variables.
    if "FREEZER_BOT_DISCORD_TOKEN" not in os.environ:
        console.log("Couldn't find bot's Discord token, make sure the 'FREEZER_BOT_DISCORD_TOKEN' environment variable is set.", console.Level.CRITICAL)
        return
    
    discord_token_env = os.environ.get("FREEZER_BOT_DISCORD_TOKEN", "")

    # Setup and run the bot.
    intents = discord.Intents.default()
    intents.message_content = True

    bot = freezer_bot.FreezerBot(
        prefix="poss ",
        name="Chilly",
        color=0x1ABC9C,
        intents=intents
    )

    bot.run(token=discord_token_env) # (blocking call)


if __name__ == "__main__":
    main()
