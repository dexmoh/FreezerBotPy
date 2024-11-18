import discord
from embed import create_embed


# This class is responsible for creating and handling buttons for listing though
# pages of pins with the `list` command.
class PinsSearchView(discord.ui.View):
    def __init__(self, ctx, pins, current_page, number_of_pages, pins_per_page_limit, title):
        super().__init__()
        self.ctx = ctx
        self.pins = pins
        self.current_page = current_page
        self.number_of_pages = number_of_pages
        self.pins_per_page_limit = pins_per_page_limit
        self.title = title
    
    # Previous page button.
    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="⬅")
    async def show_previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        (desc_str, view) = self._list_page(is_next=False)
        await interaction.response.edit_message(embed=create_embed(self.ctx, desc=desc_str), view=view)

    # Next page button.
    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="➡")
    async def show_next(self, interaction: discord.Interaction, button: discord.ui.Button):
        (desc_str, view) = self._list_page(is_next=True)
        await interaction.response.edit_message(embed=create_embed(self.ctx, desc=desc_str), view=view)
    
    # Util function to list the next or the previous page of pins.
    def _list_page(self, is_next: bool):
        if is_next:
            self.current_page += 1
            if self.current_page > self.number_of_pages:
                self.current_page = 1
        else:
            self.current_page -= 1
            if self.current_page < 1:
                self.current_page = self.number_of_pages

        list_start = (self.current_page - 1) * self.pins_per_page_limit
        list_end = list_start + self.pins_per_page_limit

        desc_str = self.title

        for pin in self.pins[list_start:list_end]:
            desc_str += f"\n- {pin}"
        
        desc_str += f"\n\nPage {self.current_page}/{self.number_of_pages}"

        # Create buttons.
        view = PinsSearchView(self.ctx, self.pins, self.current_page, self.number_of_pages, self.pins_per_page_limit, self.title)
        return (desc_str, view)
