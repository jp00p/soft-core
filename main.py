import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# from cogs.file_cog import FileCog
# from cogs.text_cog import TextCog

load_dotenv()  # Load variables from .env file

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    auto_sync_commands=True,
)

bot.load_extensions("cogs.library")
bot.load_extensions("cogs.frog")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready!")


# Add more slash commands, regular commands, and event handlers here


# Read the token from the environment variable
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
