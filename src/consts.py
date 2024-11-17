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
        `pin` - Create a new pin.
        `search` - Search for a specific pin by keyword.
        `list` - List all of the existing pins, or narrow them down by keyword.

        **Chatbot Commands**
        `fact` - (Experimental) Generate an opossum fact.
        ''',

    "help_privileged" : '''
        **Privileged Commands**
        `shutdown` - Turn {name} off. :(
        `toggle_exp` - Toggle experimental features off or on globally.
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
