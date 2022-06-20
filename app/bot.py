import os
import random
from typing import List

from discord.ext import commands
from dotenv import load_dotenv
from lib.text import get_important, get_similar, get_synonym

if not os.getenv("DISCORD_TOKEN"):
    load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


@bot.command(name="roll", aliases=["dice", "🎲"], help="Simulates rolling dice.")
async def cmd_roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)
    ]
    await ctx.send(", ".join(dice))


@bot.command(
    name="get_important",
    aliases=["gimp"],
    help="Returns the most important phrases in your text in descending importance.",
)
async def cmd_get_important(ctx, text: str, num_phrases_to_return: int = 1):
    response_json = get_important(text, num_phrases_to_return)
    phrases = [phrase["text"] for phrase in response_json["data"]["phrases"]]
    await ctx.send("```{}```".format("\n".join(phrases)))


@bot.command(
    name="get_similar",
    aliases=["gsim"],
    help="Returns similar words to your text in descending similarity.",
)
async def cmd_get_similar(ctx, text: str, num_similar_words_to_return: int = 1):
    response_json = get_similar(text, num_similar_words_to_return)
    similar_words = [similar["text"] for similar in response_json["data"]["similar"]]
    await ctx.send("```{}```".format("\n".join(similar_words)))


@bot.command(
    name="get_synonym",
    aliases=["gsyn"],
    help='Returns synonyms to your text.\n\npart_of_speech options: "a", "s", "r", "n", "v"',
)
async def cmd_get_synonym(
    ctx, text: str, part_of_speech: str, num_synonyms_to_return: int = 1
):
    synonyms = [
        synonym.replace("_", " ")
        for synonym in get_synonym(text, part_of_speech)[:num_synonyms_to_return]
    ]
    print(synonyms)
    await ctx.send("```{}```".format("\n".join(synonyms)))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        possible_labels: List[str] = get_synonym("fool", "n")
        await ctx.send(
            "You're missing an argument, ya {}!".format(
                random.choice(possible_labels).replace("_", " ")
                if len(possible_labels)
                else "buffoon"
            )
        )


bot.run(TOKEN)
