from discord.ext import commands
from lib.nlp import get_filled_mask, get_important, get_similar, get_synonym


class NLP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="get_important",
        aliases=["gimp"],
        help="Returns the most important phrases in your text in descending importance.\nExample: !gimp \"Avocados are a fruit, not a vegetable. They're technically considered a single-seeded berry, believe it or not.\"",
    )
    async def cmd_get_important(self, ctx, text: str, num_phrases_to_return: int = 1):
        response_json = await get_important(text, num_phrases_to_return)
        phrases = [phrase["text"] for phrase in response_json["data"]["phrases"]]

        if len(phrases) > 0:
            response_message = "```\n{}\n```".format("\n".join(phrases))
        else:
            response_message = "Nothing important found"
        await ctx.send(response_message)

    @commands.command(
        name="get_similar",
        aliases=["gsim"],
        help="Returns similar words to your text in descending similarity.\nExample: !gsim whatever",
    )
    async def cmd_get_similar(
        self, ctx, text: str, num_similar_words_to_return: int = 1
    ):
        response_json = await get_similar(text, num_similar_words_to_return)
        similar_words = [
            similar["text"] for similar in response_json["data"]["similar"]
        ]

        if len(similar_words) > 0:
            response_message = "```\n{}\n```".format("\n".join(similar_words))
        else:
            response_message = "No similar words found"
        await ctx.send(response_message)

    @commands.command(
        name="get_suggestion",
        aliases=["gsug"],
        help="Returns suggestions for the [MASK] in your text.\nExample: !gsug \"You are such a [MASK].\"",
    )
    async def cmd_get_suggestions(self, ctx, text: str, num_suggestions_to_return: int = 1, use_in_sentence: bool = True):
        response_json = await get_filled_mask(text, num_suggestions_to_return)
        suggested_words = []
        for suggestion_group in response_json["data"]["suggestions"]:
            grouped_words = []
            for filled_mask in suggestion_group:
                grouped_words.append(filled_mask["text"])
            suggested_words.append(grouped_words)

        if len(suggested_words) > 0:
            if use_in_sentence:
                # TODO: To fix. Inefficient, but works for now
                response_message = "```"
                for word_group in suggested_words:
                    current_line = text
                    for replacement in word_group:
                        current_line = current_line.replace("[MASK]", replacement, 1)
                    response_message += f"\n{current_line}"
                response_message += "\n```"
            else:
                response_message = "```\n{}\n```".format("\n".join([(', ').join(grouped_words) for grouped_words in suggested_words]))
        else:
            response_message = "No suggestions found"
        await ctx.send(response_message)

    @commands.command(
        name="get_synonym",
        aliases=["gsyn"],
        help='Returns synonyms to your text.\n\npart_of_speech options: "a", "s", "r", "n", "v"\nExample: !gsyn buffoon n',
    )
    async def cmd_get_synonym(
        self, ctx, text: str, part_of_speech: str, num_synonyms_to_return: int = 1
    ):
        synonyms = [
            synonym.replace("_", " ")
            for synonym in get_synonym(text, part_of_speech)[:num_synonyms_to_return]
        ]

        if len(synonyms) > 0:
            response_message = "```\n{}\n```".format("\n".join(synonyms))
        else:
            response_message = "No synonyms found"
        await ctx.send(response_message)


def setup(bot):
    bot.add_cog(NLP(bot))
