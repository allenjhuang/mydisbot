from typing import List
from nltk.corpus import wordnet
import requests


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


def get_important(text: str, num_phrases_to_return: int):
    # Uses POST method to avoid GET method's url length limit when text is lengthy
    return requests.post(
        "https://ajh-getimportant.herokuapp.com/phrases",
        json={"text": text, "topn": num_phrases_to_return},
    ).json()


def get_similar(text: str, num_similar_words_to_return: int):
    # Uses POST method to avoid GET method's url length limit when text is lengthy
    return requests.post(
        "https://ajh-getsimilar.herokuapp.com/similar",
        json={"text": text, "topn": num_similar_words_to_return},
    ).json()
