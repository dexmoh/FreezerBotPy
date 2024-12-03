import discord
from embed import create_embed
from consts import menu_desc


# This class implements buttons that appear in the help and
# about menus and they're used to switch between the two menus.
class MenuSwitcherView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(label="Commands", style=discord.ButtonStyle.blurple)
    async def show_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_embed(
            self.ctx,
            title="Help menu!",
            desc=menu_desc["help"].format(name=self.ctx.bot.name, prefix=self.ctx.bot.command_prefix)
        )

        # Show privileged commands only to privileged users.
        if self.ctx.author.id in self.ctx.bot.whitelist["users"]:
            embed.description += menu_desc["help_privileged"].format(name=self.ctx.bot.name)
        
        # Create a button.
        view = MenuSwitcherView(self.ctx)
        for child in view.children:
            if isinstance(child, discord.ui.Button) and child.label == "Commands":
                child.style = discord.ButtonStyle.gray
                child.disabled = True
                break
        
        # Update the current message with the new embed.
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="About", style=discord.ButtonStyle.blurple)
    async def show_about(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Create the about menu embed
        embed = create_embed(
            self.ctx,
            title="About me!",
            desc=menu_desc["about"]
        )

        # Create a button.
        view = MenuSwitcherView(self.ctx)
        for child in view.children:
            if isinstance(child, discord.ui.Button) and child.label == "About":
                child.style = discord.ButtonStyle.gray
                child.disabled = True
                break

        # Update the current message with the new embed
        await interaction.response.edit_message(embed=embed, view=view)
