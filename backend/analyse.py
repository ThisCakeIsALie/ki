from dataclasses import dataclass
from typing import List
from functools import lru_cache

from japanese import to_romanji, to_roman_syllables
from approximate import approximate_word_phonetic, approximate_word_syntactical
from approximate import WordApproximation

from stopwatch import Stopwatch

from validation import detect_problems


@dataclass
class WordInfo:
    original: str
    pronounciation: str
    syllables: List[str]
    warnings: List[str]
    time: float # Time it took to process request
    phonetic_approx: WordApproximation
    syntactic_approx: WordApproximation

@lru_cache
def analyse(word: str) -> WordInfo:
    timer = Stopwatch()
    timer.start()

    pronounciation = to_romanji(word)
    syllables = to_roman_syllables(word)

    warnings = detect_problems(word) # Detect english characters etc.

    phonetic_approx = approximate_word_phonetic(word, alpha=0.1)

    syntactic_approx = approximate_word_syntactical(word, alpha=0.5)


    timer.stop()
    time = timer.elapsed()

    return WordInfo(word, pronounciation, syllables, warnings, time, phonetic_approx, syntactic_approx)
