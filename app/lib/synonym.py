from typing import List
from nltk.corpus import wordnet


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
