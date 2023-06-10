import discord
from discord.ext import commands, tasks
from discord.interactions import Interaction
import random
import asyncio

BOGGLE_CHANNEL = 1117135398020337766


def load_english_words(file_path):
    with open(file_path, "r") as file:
        english_words = set(file.read().splitlines())
    return english_words


english_words = load_english_words("text_files/english_words.txt")


class BoggleCog(commands.Cog):
    """a handcrafted Boggle game just for me & jenna!"""

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.grid: list = []
        self.players: dict = {}
        self.game_started = False

    @commands.slash_command(name="boggle", description="Start a game of Boggle")
    async def begin(self, ctx: discord.ApplicationContext):
        self.game_started = True
        await self.boggle_loop.start()

    @tasks.loop(seconds=30, count=1)
    async def boggle_loop(self):
        # Initialize game variables
        self.grid = generate_grid()
        self.players = {}
        # Send the grid of letters to the channel
        grid_message = "```\n" + format_grid(self.grid) + "```"
        await self.bot.get_channel(BOGGLE_CHANNEL).send(
            content="Boggle game started! Type as many words as you can using the letters in the grid.",
            embed=discord.Embed(description=grid_message),
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if (
            not self.game_started
            or message.author == self.bot.user
            or message.channel.id != BOGGLE_CHANNEL
        ):
            return

        if message.author.id not in self.players.keys():
            print(f"Adding {message.author.id} to the list")
            self.players[message.author.id] = []

        word = message.content.lower()
        if word not in self.players[message.author.id]:
            if validate_word(word, self.grid):
                self.players[message.author.id].append(word)
        await message.delete()

    @boggle_loop.after_loop
    async def end_boggle(self):
        # Tally scores and generate result message
        self.game_started = False
        scores = {}
        for player_id, words in self.players.items():
            score = count_valid_words(words)
            scores[player_id] = score

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        result_message = "Boggle game has ended!\n\n**Scores:**\n"
        for position, (player_id, score) in enumerate(sorted_scores, start=1):
            player = await self.bot.fetch_user(player_id)
            player_name = player.display_name
            result_message += f"{position}. {player_name}: {score} points\n"

        result_message += "\n**Scoring words:**\n"
        for player_id, words in self.players.items():
            player = await self.bot.fetch_user(player_id)
            player_name = player.display_name
            result_message += f"{player_name}: {' | '.join(words)}\n"

        # Send the result message to the channel
        await self.bot.get_channel(BOGGLE_CHANNEL).send(result_message)

    def cog_unload(self) -> None:
        self.boggle_loop.cancel()


def generate_grid() -> list:
    """create a 2d list of letters, 5x5"""
    grid = []
    letters = "abcdefghijklmnopqrstuvwxyz"
    for _ in range(4):
        row = [random.choice(letters) for _ in range(4)]
        grid.append(row)
    return grid


def format_grid(grid: list) -> str:
    """output the grid in a string"""
    formatted_grid = ""
    for row in grid:
        formatted_grid += " ".join(row) + "\n"
    return formatted_grid


def validate_word(word: str, grid: list[str]) -> bool:
    flattened_letters = [letter.lower() for sublist in grid for letter in sublist]
    for letter in word:
        if letter.lower() not in flattened_letters:
            return False
        flattened_letters.remove(letter.lower())
    if word in english_words and len(word) >= 2:
        return True


def count_valid_words(words: list) -> int:
    return len(words)


def setup(bot: discord.Bot) -> None:
    bot.add_cog(BoggleCog(bot))
