import os
import random
from typing import List

from discord.ext import commands
from dotenv import load_dotenv

if not os.getenv("DISCORD_TOKEN"):
    load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def get_prefix(bot, message):
    prefixes = ["!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix)

initial_extensions = ["cogs.simple", "cogs.nlp"]

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(
        f"Logged in as: {bot.user.name} - {bot.user.id}"
    )


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


bot.run(TOKEN, bot=True, reconnect=True)
