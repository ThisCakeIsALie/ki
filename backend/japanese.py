import pykakasi
import re
import hiragana
from typing import List
from itertools import zip_longest

# Initialize space converter
wakati = pykakasi.wakati()
spacer = wakati.getConverter()

# Initialize kanji & katakana converter
kakasi_kanji = pykakasi.kakasi()
kakasi_kanji.setMode('K', 'H')
kakasi_kanji.setMode('J', 'H')
kanji_replacer = kakasi_kanji.getConverter()

# Initialize romanji converter
kakasi_romanji = pykakasi.kakasi()
kakasi_romanji.setMode('H', 'a')
kakasi_romanji.setMode('K', 'a')
kakasi_romanji.setMode('J', 'a')
kakasi_romanji.setMode('r', 'Hepburn')
kakasi_romanji.setMode('s', True)

romanjifier = kakasi_romanji.getConverter()

def to_hiragana(word: str) -> str:
    hiragana_word = kanji_replacer.do(word)

    return hiragana_word

def to_syllables(word: str) -> List[str]:
    hiragana_word = to_hiragana(word)
    syllables = []

    for char in hiragana_word:
        no_syllables_yet = len(syllables) == 0

        if no_syllables_yet:
            syllables.append(char)
            continue

        last_syllable = syllables[-1]
        was_last_syllable_hiragana = hiragana.is_hiragana_like(
            last_syllable[-1])

        is_like_hiragana = hiragana.is_hiragana_like(char)

        if not is_like_hiragana and not was_last_syllable_hiragana:
            syllables[-1] += char
            continue

        is_modifier = hiragana.is_hiragana_modifier(char)
        if is_modifier and was_last_syllable_hiragana:
            syllables[-1] += char
            continue

        syllables.append(char)

    return syllables


def to_pronounciation(word: str) -> str:
    syllables = to_syllables(word)

    # We ignore syllables we cannot pronounce
    pronounciations = list(
        filter(None, map(hiragana.to_pronounciation, syllables)))

    return ' '.join(pronounciations)


def to_roman_syllables(word: str) -> List[str]:
    syllables = to_syllables(word)

    return list(map(lambda syl: romanjifier.do(syl), syllables))


def to_romanji(word: str) -> str:
    return romanjifier.do(word)


def split_words(words: str) -> List[str]:
    tokens = re.split(r'\W+', spacer.do(words))

    return tokens
