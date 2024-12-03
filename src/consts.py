# Descriptions used in help and about menus.
menu_desc: dict = {
    "help" : '''
        **Info**
        Prefix your message with `{prefix}` to access {name}'s commands.
        Type `{prefix}<command> help` to get more information about a specific command.

        **Utility Commands**
        `help` - Show this menu.
        `about` - Show about page.
        `roll <XdY>` - Roll a dice.
        `ping` - Check {name}'s latency.

        **Pin Commands**
        `pin <keyword>` - Create a new pin.
        `delete <keyword>` - Delete a pin.
        `search <keyword>` - Search for a specific pin by keyword.
        `list <search-term (optional)>` - List all of the existing pins, or narrow them down with a search term.
        `random` - Send a random pin.
        ''',

    "help_privileged" : '''
        **Privileged Commands**
        `shutdown` - Turn {name} off. :(
        ''',

    "about" : '''
        **Introduction**
        Hello? Is anybody there... ? I've been stuck in this freezer for years, it's really cold in here! What's that... you want to know more about me? Maybe this isn't the best time, how about you help me?

        ...

        Your favorite opossum bot, but maybe that's just because there's not that many opossum bots on discord in the first place.

        Written in [Python](https://www.python.org/) and [Discord.py](https://discordpy.readthedocs.io/en/stable/). Is generously being hosted by `affectedarc07` for years now (does he even know I live in his walls?). Developed by `dexmoh`, sadly.

        **GitHub**
        Check out my GitHub page by clicking [here](https://github.com/dexmoh/FreezerBotPy).
        You can suggest new features, changes and report bugs by opening a new issue, or you can contribute by opening a pull request!
        '''
}
