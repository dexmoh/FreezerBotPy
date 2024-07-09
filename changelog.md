# Changelog
> List of all of the changes from the old C# implementation of the bot.

## General
- The bot is now completely rewritten in Python.
- Improved readability of menus.
- The bot invites are no longer public, but the bot won't leave the servers it's already been part of. You can ask `dexmoh` on discord for an invite link.
- Commands are now case sensitive.
- All of the tokens and API keys are now saved as environment variables.

## Pins
The pin feature seems to be the most used feature of the bot so it went through some improvements.

- Users can now search for specific pins by entering a search term, the bot will then find all of the pins with similar or matching names using REGEX.
- Users can now list through saved pins by reacting to the bot's message.
- Pins now get saved in an SQL database, instead of... *text files* \*sigh.

## [EXPERIMENTAL] OpenAI Text Generation
- The `poss facts` feature is now reworked to generate random, unhinged opossum facts using gpt-3.5. However, this feature is only available to the servers that have been whitelisted to use OpenAI text generation, otherwise, the old `poss facts` feature has been removed.

## Removals :(
Some of the old bot features were removed either due to user disinterest, or because they weren't implemented well and had issues.

- Removed Imgur image search feature.
- Removed the `poss translate/say` feature.
- **Partially** removed the old `poss facts` feature. (Read OpenAI section for more information.)
