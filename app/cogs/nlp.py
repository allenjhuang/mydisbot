import discord
from discord.ext import commands
from lib.nlp import get_important, get_similar, get_synonym


class NLP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="get_important",
        aliases=["gimp"],
        help="Returns the most important phrases in your text in descending importance.",
    )
    async def cmd_get_important(self, ctx, text: str, num_phrases_to_return: int = 1):
        response_json = get_important(text, num_phrases_to_return)
        phrases = [phrase["text"] for phrase in response_json["data"]["phrases"]]
        await ctx.send("```{}```".format("\n".join(phrases)))

    @commands.command(
        name="get_similar",
        aliases=["gsim"],
        help="Returns similar words to your text in descending similarity.",
    )
    async def cmd_get_similar(
        self, ctx, text: str, num_similar_words_to_return: int = 1
    ):
        response_json = get_similar(text, num_similar_words_to_return)
        similar_words = [
            similar["text"] for similar in response_json["data"]["similar"]
        ]
        await ctx.send("```{}```".format("\n".join(similar_words)))

    @commands.command(
        name="get_synonym",
        aliases=["gsyn"],
        help='Returns synonyms to your text.\n\npart_of_speech options: "a", "s", "r", "n", "v"',
    )
    async def cmd_get_synonym(
        self, ctx, text: str, part_of_speech: str, num_synonyms_to_return: int = 1
    ):
        synonyms = [
            synonym.replace("_", " ")
            for synonym in get_synonym(text, part_of_speech)[:num_synonyms_to_return]
        ]
        await ctx.send("```{}```".format("\n".join(synonyms)))


def setup(bot):
    bot.add_cog(NLP(bot))
