from dataclasses import dataclass
from typing import List
from functools import lru_cache

from japanese import to_romanji, to_roman_syllables
from approximate import approximate_word_phonetic, approximate_word_syntactical
from approximate import WordApproximation


@dataclass
class WordInfo:
    original: str
    pronounciation: str
    syllables: List[str]
    phonetic_approx: WordApproximation
    syntactic_approx: WordApproximation

@lru_cache
def analyse(word: str) -> WordInfo:
    pronounciation = to_romanji(word)
    syllables = to_roman_syllables(word)

    phonetic_approx = approximate_word_phonetic(word, alpha=0.75)

    syntactic_approx = approximate_word_syntactical(word, alpha=0.5)

    return WordInfo(word, pronounciation, syllables, phonetic_approx, syntactic_approx)
