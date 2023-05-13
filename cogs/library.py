import os
import random
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import Select, View, Button


IMAGE_DIRECTORIES = [
    ("Pornography images", "G:\\Pornography images\\"),
    ("Funniez", "C:\\Users\\asimo\\Pictures\\funniez\\"),
    ("Art and Ecchi", "C:\\Users\\asimo\\Pictures\\art and ecchi"),
    ("Cool and aesthetic", "C:\\Users\\asimo\\Pictures\\cool and aesthetic"),
    ("Pixel art", "C:\\Users\\asimo\\Pictures\\pixels"),
    ("Photography inspo", "C:\\Users\\asimo\\Pictures\\photography ideas"),
    ("Drawing inspo", "C:\\Users\\asimo\\Pictures\\drawing inspo"),
    ("Tiny clips", "D:\\Pornography videos\\tiny clips"),
    ("Pics of Jeremy", "C:\\Users\\asimo\\Pictures\\personal\\me"),
    (
        "Misc photography by Jeremy",
        "C:\\Users\\asimo\\Pictures\\personal\\photography etc",
    ),
    ("Almost all of Zishy's photos", "D:\\bulk_image_downloader\\all of em maybe"),
    ("Retro sci-fi art", "D:\\bulk_image_downloader\\Sci-Fi"),
    ("Weird computer art", "D:\\Bulk Image Downloader\\weird computer art"),
    ("More weird art", "D:\\Bulk Image Downloader\\more weird art"),
    ("Vintage porn", "D:\\Bulk Image Downloader\\vintage porn pix"),
    ("Skullz", "D:\\Bulk Image Downloader\\skullz"),
    ("Missdeadlyred", "D:\\Bulk Image Downloader\\Miss Deadly Red_ Archive\\pics"),
    ("Red hair", "D:\\Bulk Image Downloader\\red"),
]

TEXT_CATEGORIES = ["Love notes", "Vancouver Dinner Ideas", "Links", "Misc", "Watchlist"]


class Library(commands.Cog):
    """the main cog class - the entrypoint to all the functionality here"""

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(
        name="library", description="Access the library on Jeremy's computer"
    )
    async def library_cmd(self, ctx: discord.ApplicationContext):
        """show the library View"""
        view = LibraryScreen(self.bot)
        await ctx.respond(view=view, embed=view.embed, ephemeral=True)


def setup(bot: discord.Bot):
    """attaches cog to bot when ready"""
    bot.add_cog(Library(bot))


class LibraryScreen(View):
    """Main Library View

    Lets the user choose which library they want to access, using buttons
    """

    def __init__(self, bot, **kwargs):
        self.bot = bot
        super().__init__(**kwargs)
        self.add_item(ImagesButton(self.bot))
        self.add_item(TextButton(self.bot))
        self.embed = discord.Embed(
            title="Soft Core: Library interface",
            description="Access the library of media on Jeremy's computer",
        )


class ImagesButton(Button):
    """Clicking this button attaches the images dropdown to the View"""

    def __init__(self, bot, **kwargs):
        self.bot = bot
        super().__init__(label="Images", **kwargs)

    async def callback(self, interaction: Interaction):
        view = LibraryScreen(self.bot)
        view.add_item(ImagesDropdown(self.bot))
        await interaction.response.edit_message(view=view)


class TextButton(Button):
    """Clicking this button attaches the text categories dropdown to the View"""

    def __init__(self, bot, **kwargs):
        self.bot = bot
        super().__init__(label="Texts", **kwargs)

    async def callback(self, interaction: Interaction):
        view = LibraryScreen(self.bot)
        view.add_item(TextDropdown(self.bot))
        await interaction.response.edit_message(view=view)


class ImagesDropdown(Select):
    """Selecting a category will send a random image from that category"""

    def __init__(self, bot):
        options = (
            discord.SelectOption(label=IMAGE_DIRECTORIES[i][0], value=str(i))
            for i in range(len(IMAGE_DIRECTORIES))
        )
        super().__init__(placeholder="Select a directory", options=options)

    async def callback(self, interaction: discord.Interaction):
        val = int(self.values[0])
        selected_directory = IMAGE_DIRECTORIES[val][1]
        directory_name = IMAGE_DIRECTORIES[val][0]
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
        with open(file_path, "rb") as file:
            file_data = discord.File(file)
            await interaction.response.send_message(
                file=file_data, ephemeral=False, content=f"**{directory_name}**"
            )


class TextDropdown(Select):
    """Selecting a category will send a random line of text from that text file"""

    def __init__(self, bot):
        self.bot = bot
        # Send the category options as a response with a dropdown menu
        options = [
            discord.SelectOption(label=category, value=category)
            for category in TEXT_CATEGORIES
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
