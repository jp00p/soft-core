import os
import random
import discord
import datetime
from discord.ext import tasks, commands

SEND_TO = 340697363129565195
FROGS_DIR = "D:\\bulk_image_downloader\\frogs"
TIMES_TO_SEND = [datetime.time(hour=8), datetime.time(hour=16)]


class FrogCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.user = bot.get_user(SEND_TO)
        self.send_frog.start()
        print("Croak!")

    def cog_unload(self):
        self.send_frog.cancel()

    def pick_file(self):
        files = os.listdir(FROGS_DIR)
        random_file = random.choice(files)
        file_path = os.path.join(FROGS_DIR, random_file)
        return file_path

    @tasks.loop(time=TIMES_TO_SEND)
    async def send_frog(self):
        user = await self.bot.fetch_user(SEND_TO)
        random_file = self.pick_file()
        with open(random_file, "rb") as file:
            file_data = discord.File(file)
            await user.send(file=file_data, content="Ribbit!")


def setup(bot: discord.Bot):
    """attaches cog to bot when ready"""
    bot.add_cog(FrogCog(bot))
