# Changelog
> List of all of the changes from the old C# implementation of the bot.

> [!IMPORTANT]
> This changelog still isn't fully written and is still being updated as the bot gets new updates!

## General
- The bot is now completely rewritten in Python.
- Improved readability of user menus.
- The bot invites are no longer public, but the bot won't leave the servers it's already been part of. You can ask `dexmoh` on discord for an invite link.
- Commands are now case sensitive.
- Bot's token is now saved as environment variable.
- Bot will no longer say hi back when you say `poss hi`, how impolite...
- (Hopefully) Removed all of the bad words out of the chatbot's vocabulary.

## New Commands
- New `roll` command that lets you roll dice.
- New `ping` command that lets you check latency.

## Pins
- The `loopkup` command got renamed to `show`, but you can still use the old alias to access the command.
- The `list` command now takes an extra optional parameter `search-term` that allows you to find all of the pins with similar, or matching names.
- Users can now list through saved pins by reacting to the bot's message.
- Pins now get saved in an SQLite database, instead of... *text files* \*sigh.

## Removals :(
Some of the old bot features were removed either due to user disinterest, or because they weren't implemented well and had issues.

- Removed Imgur image search feature.
- Removed the `translate/say` command.
- Removed the `facts` command.
