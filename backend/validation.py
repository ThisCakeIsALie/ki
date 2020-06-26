import hiragana
from japanese import to_syllables, to_hiragana

MAX_INPUT_LENGTH = 20

def is_usable(word):
    if not word:
        return False

    syllable_count = len(to_syllables(word))

    return 0 < syllable_count < MAX_INPUT_LENGTH

def detect_problems(word):
    warnings = []

    syllables = to_syllables(word)
    fully_pronouncable = all(map(hiragana.to_pronounciation, syllables))

    if not fully_pronouncable:
        warnings.append("Some parts couldn't be pronounced and were ignored (Only Kana and Kanji are supported)")

    has_small_tsu = 'っ' in to_hiragana(word)

    if has_small_tsu:
        warnings.append('Small っ are ignored.')

    return warnings
