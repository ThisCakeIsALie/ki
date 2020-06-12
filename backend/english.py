import util
import pronouncing
from typing import Tuple, List, Optional
from functools import lru_cache
from math import floor
from dictionary import words, pronounciations


"""
An alternative here would be to use a VP Tree for more efficient NNS.
However testing has shown that the overhead is only worth it for incredibly long queries...

from vptree import VPTree

word_tree = VPTree(list(words), util.word_distance)

...

match = word_tree.get_nearest_neighbor(text)

return match[1]
"""


def syntactically_similar_word(text: str) -> str:
    return min(words, key=lambda w: util.word_distance(w, text))


def phonetically_similar_word(phonemes):
    pronounciation = ' '.join(phonemes)
    if not pronounciations.has_keys_with_prefix(pronounciation):
        return None

    matching_pairs = pronounciations.items(pronounciation)

    best_word = None
    best_overshoot = None
    for phones, word in matching_pairs:
        overshoot = phones.count(' ')
        if best_overshoot is None or overshoot < best_overshoot:
            best_word = word
            best_overshoot = overshoot

    return (best_word.decode('ascii'), best_overshoot - pronounciation.count(' '))
