import os
import bot
import whitelist
import console

# Entry point.
def main():
    # Configure logging.
    console.init()

    # Fetch env variables.
    if 'FREEZER_BOT_DISCORD_TOKEN' not in os.environ:
        console.log('Couldn\'t find the Discord token, make sure the "FREEZER_BOT_DISCORD_TOKEN" environment variable is set.', console.Level.CRITICAL)
        return
    
    discord_token_env = os.environ.get('FREEZER_BOT_DISCORD_TOKEN', '')
    openai_api_key_env = os.environ.get('FREEZER_BOT_OPENAI_API_KEY', '')

    if openai_api_key_env == '':
        console.log('"FREEZER_BOT_OPENAI_API_KEY" isn\'t set in environment variables, the bot will only use legacy text generation.', console.Level.WARNING)
    
    # Initialize user and server whitelists.
    whitelist.init()

    # Run the bot.
    bot.bot.run(discord_token_env)
    del discord_token_env


if __name__ == '__main__':
    main()
