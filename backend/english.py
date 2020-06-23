import util
import pronouncing
from typing import Tuple, List, Optional
from functools import lru_cache
from math import floor
from dictionary import words, pronounciations


"""
An alternative here would be to use a VP Tree for more efficient NNS.
However testing has shown that the overhead is only worth it for incredibly long queries...

Also it wouldn't work at all since VP Trees require a metric distance measure, which LCS distance is not.
(There is a metric version of it but empirically it provided bad results)

from vptree import VPTree

word_tree = VPTree(list(words), util.word_distance)

...

match = word_tree.get_nearest_neighbor(text)

return match[1]
"""


def similar_word(text: str) -> str:
    return min(words, key=lambda w: util.syntax_distance(w, text))

def similar_phones(phonemes: List[str]) -> str:
    return min(pronounciations.keys(), key=lambda p: util.phonetic_distance(p, phonemes))

def pronounciation_to_word(phonemes):
    if not phonemes in pronounciations:
        return None

    return pronounciations[phonemes]
