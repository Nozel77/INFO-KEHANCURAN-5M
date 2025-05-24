import discord

class PlayerListView(discord.ui.View):
    def __init__(self, players, page_size=15):
        super().__init__(timeout=120) 
        self.players = players
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = (len(players) - 1) // page_size + 1

        self.prev_button.disabled = True
        if self.total_pages <= 1:
            self.next_button.disabled = True

    def get_page_content(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_players = self.players[start:end]
        text = "\n".join(f"{i+1+start}. {p['name']} ({p['id']})" for i, p in enumerate(page_players))
        return text

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.prev_button.disabled = self.current_page == 0
            self.next_button.disabled = False

            embed = interaction.message.embeds[0]
            embed.set_field_at(
                2,
                name=f"**Player List (Page {self.current_page+1}/{self.total_pages})**",
                value=f"```{self.get_page_content()}```",
                inline=False
            )

            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.next_button.disabled = self.current_page == self.total_pages - 1
            self.prev_button.disabled = False

            embed = interaction.message.embeds[0]
            embed.set_field_at(
                2,
                name=f"**Player List (Page {self.current_page+1}/{self.total_pages})**",
                value=f"```{self.get_page_content()}```",
                inline=False
            )

            await interaction.response.edit_message(embed=embed, view=self)
