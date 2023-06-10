import os
import random
import discord
from discord.ext import commands, tasks
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

SEND_TO = 1117134823266463776


class Library(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.last_dir = None
        self.last_file = None
        self.autolibrary.start()

    def pick_file(self):
        random_pick = random.choice(IMAGE_DIRECTORIES)
        while random_pick == self.last_dir:
            random_pick = random.choice(IMAGE_DIRECTORIES)
        self.last_dir = random_pick

        selected_directory = random_pick[1]
        directory_name = random_pick[0]

        files = os.listdir(selected_directory)
        random_file = random.choice(files)
        while random_file == self.last_file:
            random_file = random.choice(files)
        self.last_file = random_file
        file_path = os.path.join(selected_directory, random_file)
        with open(file_path, "rb") as file:
            file_data = discord.File(file)
        return directory_name, file_data

    @tasks.loop(minutes=5)
    async def autolibrary(self):
        channel = await self.bot.fetch_channel(SEND_TO)
        dir_name, random_file = self.pick_file()
        await channel.send(file=random_file, content=dir_name)


def setup(bot: discord.Bot):
    """attaches cog to bot when ready"""
    bot.add_cog(Library(bot))
