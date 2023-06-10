import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    auto_sync_commands=True,
)

bot.load_extensions("cogs.library")
bot.load_extensions("cogs.frog")
bot.load_extensions("cogs.boggle")


@bot.event
async def on_ready():
    """when the bot is ready and everything is loaded, this will run!"""
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready!")


token = os.getenv("DISCORD_TOKEN")
bot.run(token)
