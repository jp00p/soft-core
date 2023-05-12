import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import Select, View

import discord
import os
import random

DIRECTORIES = [
    ("Pornography images", "G:\\Pornography images\\"),
    ("Funniez", "C:\\Users\\asimo\\Pictures\\funniez\\"),
    ("Art and Ecchi", "C:\\Users\\asimo\\Pictures\\art and ecchi"),
    ("Cool and aesthetic", "C:\\Users\\asimo\\Pictures\\cool and aesthetic"),
    ("Pixel art", "C:\\Users\\asimo\\Pictures\\pixels"),
    ("Photography inspo", "C:\\Users\\asimo\\Pictures\\photography ideas"),
    ("Drawing inspo", "C:\\Users\\asimo\\Pictures\\drawing inspo"),
    ("Tiny clips", "D:\\Pornography videos\\tiny clips"),
]


class FileDropdown(discord.ui.Select):
    def __init__(self, bot):
        options = (
            discord.SelectOption(label=dir_name, value=dir_path)
            for (dir_name, dir_path) in DIRECTORIES
        )
        super().__init__(placeholder="Select a directory", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_directory = self.values[0]
        if not os.path.isdir(selected_directory):
            print("Invalid directory")
            await interaction.response.edit_message("Invalid directory.")
            return

        files = os.listdir(selected_directory)
        if not files:
            print("Empty directory")
            await interaction.response.edit_message("The directory is empty.")
            return

        random_file = random.choice(files)
        file_path = os.path.join(selected_directory, random_file)
        print(file_path)

        with open(file_path, "rb") as file:
            file_data = discord.File(file)
            await interaction.response.send_message(file=file_data, ephemeral=False)


class FileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("FileCog go!")

    @commands.slash_command(
        name="image",
        description="Choose a directory and send a random file from it",
    )
    async def choose_directory(self, ctx: discord.ApplicationContext):
        view = View()
        dropdown = FileDropdown(self.bot)
        view.add_item(dropdown)
        await ctx.send_response(
            content="Choose which pool of images", view=view, ephemeral=True
        )


def setup(bot):
    bot.add_cog(FileCog(bot))
