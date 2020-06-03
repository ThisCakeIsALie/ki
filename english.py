import util
import pronouncing
from typing import Tuple, List, Optional
from functools import lru_cache
from math import floor

_WORD_LOCATION = '10000_words.txt'
words = None

with open(_WORD_LOCATION, encoding='utf-8') as file:
    english_words = file.read().split('\n')
    english_words = set(filter(lambda s: len(s) > 0 and not s.startswith('#'), english_words))
    words = english_words

def syntactically_similar_word(text: str) -> str:
    return min(words, key=lambda w: util.word_distance(w, text))

def phonetic_prefix(word, prefix_phones):
    word_pronounciation = pronouncing.phones_for_word(word)[0]
    word_phones = word_pronounciation.split(' ')

    percentage = len(prefix_phones) / len(word_phones)

    prefix_index = floor(len(word) * percentage)

    return word[:prefix_index]


def _phoneme_overshoot(word, match_length):
    word_pronounciations = pronouncing.phones_for_word(word)
    word_phonemes = map(lambda pronounciation: pronounciation.split(' '), word_pronounciations)

    phoneme_overshoots = map(lambda phones: len(phones) - match_length, word_phonemes)

    worst_overshoot = max(phoneme_overshoots)

    return worst_overshoot

@lru_cache
def _phonetically_similar_word_cached(phonemes: Tuple[str]) -> Optional[str]:
    any_stress_phonemes = list(map(lambda phone: phone + '(0|1|2)?', phonemes))

    search_pattern = '^' + ' '.join(any_stress_phonemes)

    matching_words = pronouncing.search(search_pattern)

    if len(matching_words) == 0:
        return None

    match_phone_len = len(phonemes)

    best_word = min(matching_words, key=lambda w: _phoneme_overshoot(w, match_phone_len))

    return (best_word, _phoneme_overshoot(best_word, match_phone_len))

def phonetically_similar_word(phonemes: List[str]) -> str:
    return _phonetically_similar_word_cached(tuple(phonemes))
