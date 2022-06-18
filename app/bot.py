import os
import random
from typing import List

from discord.ext import commands
from dotenv import load_dotenv
from lib.synonym import get_synonym

if not os.getenv('DISCORD_TOKEN'):
  load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='🎲', aliases=['roll'], help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        possible_labels: List[str] = get_synonym('fool', 'n')
        await ctx.send("You're missing an argument, ya {}!".format(
            random.choice(possible_labels).replace('_', ' ')
            if len(possible_labels)
            else 'buffoon'
        ))


bot.run(TOKEN)
