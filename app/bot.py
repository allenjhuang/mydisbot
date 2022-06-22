import os
import random
from typing import List
from discord.ext import commands
from dotenv import load_dotenv
from lib.nlp import get_synonym
from shared import session

if not os.getenv("DISCORD_TOKEN"):
    load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def get_prefix(discord_bot, message):
    prefixes = ["!"]
    return commands.when_mentioned_or(*prefixes)(discord_bot, message)


class BotWithCustomCleanup(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)


    async def async_cleanup(self):
        print("\nCleaning up before closing...")
        await session.close()
        print("done")


    async def close(self):
        await self.async_cleanup()
        await super().close()


bot = BotWithCustomCleanup(command_prefix=get_prefix)

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
                if len(possible_labels) > 0
                else "buffoon"
            )
        )


bot.run(TOKEN, bot=True, reconnect=True)
