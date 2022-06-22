# NLP
from typing import List
from nltk.corpus import wordnet
from shared import session


def get_synonym(word: str, part_of_speech: str) -> List[str]:
    """Returns a list of synonyms for the word that match the part of speech.

    Args:
        part_of_speech (str): "a", "s", "r", "n", "v"

    Returns:
        List[str]
    """
    synonyms = []
    for syn in wordnet.synsets(word):
        if syn.pos() != part_of_speech:
            continue
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms


async def get_important(text: str, num_phrases_to_return: int):
    # Uses POST method to avoid GET method's url length limit when text is lengthy
    async with session.post(
        "https://ajh-getimportant.herokuapp.com/phrases",
        json={"text": text, "topn": num_phrases_to_return},
    ) as response:
        return await response.json()


async def get_similar(text: str, num_similar_words_to_return: int):
    # Uses POST method to avoid GET method's url length limit when text is lengthy
    async with session.post(
        "https://ajh-getsimilar.herokuapp.com/similar",
        json={"text": text, "topn": num_similar_words_to_return},
    ) as response:
        return await response.json()


async def get_filled_mask(text: str, num_suggestions_to_return: int):
    # Uses POST method to avoid GET method's url length limit when text is lengthy
    async with session.post(
        "https://ajh-fillmask.herokuapp.com/suggestions",
        json={"text": text, "topn": num_suggestions_to_return},
    ) as response:
        return await response.json()
