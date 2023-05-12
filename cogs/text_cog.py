import discord
import os
import random
from discord.ext import commands, tasks, pages
from discord.interactions import Interaction

CATEGORIES = ["Love notes", "Vancouver Dinner Spots", "Misc"]


class CategoryDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        # Send the category options as a response with a dropdown menu
        options = [
            discord.SelectOption(label=category, value=category)
            for category in CATEGORIES
        ]
        super().__init__(placeholder="Choose a category", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Wait for user selection

        selected_category = self.values[0]
        file_path = f"text_files/{selected_category.lower().replace(' ', '_')}.txt"

        if not os.path.isfile(file_path):
            await interaction.response.send_message("Invalid file path")
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

            if not lines:
                await interaction.response.send_message(
                    "The category text file is empty."
                )
                return

            random_line = random.choice(lines)
            await interaction.response.send_message(random_line)


class TextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("TextCog go!")

    @commands.slash_command(
        name="text", description="Choose a category and send random text"
    )
    async def text(self, ctx: discord.ApplicationContext):
        view = discord.ui.View()
        view.add_item(CategoryDropdown(self.bot))
        await ctx.send_response(
            content="Choose a category to pick from", view=view, ephemeral=True
        )


def setup(bot):
    bot.add_cog(TextCog(bot))
