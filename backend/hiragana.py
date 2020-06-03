from itertools import product
from typing import Optional

_hiragana_phonemics = {
    # Basic
    'あ': 'AH',
    'い': 'IY',
    'う': 'UW',
    'え': 'EH',
    'お': 'AA',
    # Begin with K
    'か': 'K AH',
    'き': 'K IY',
    'く': 'K UW',
    'け': 'K EH',
    'こ': 'K AA',
    # Begin with S
    'さ': 'S AH',
    'し': 'SH IY',
    'す': 'S UW',
    'せ': 'S EH',
    'そ': 'S AA',
    # Begin with T
    'た': 'T AH',
    'ち': 'CH IY',
    'つ': 'T S UW',
    'て': 'T EH',
    'と': 'T AA',
    # Begin with N
    'な': 'N AH',
    'に': 'N IY',
    'ぬ': 'N UW',
    'ね': 'N EH',
    'の': 'N AA',
    # Begin with H
    'は': 'HH AH',
    'ひ': 'HH IY',
    'ふ': 'F UW',
    'へ': 'HH EH',
    'ほ': 'HH AA',
    # Begin with M
    'ま': 'M AH',
    'み': 'M IY',
    'む': 'M UW',
    'め': 'M EH',
    'も': 'M AA',
    # Begin with Y
    'や': 'Y AH',
    'ゆ': 'Y UW',
    'よ': 'Y AA',
    # Begin with R
    'ら': 'R AH',
    'り': 'R IY',
    'る': 'R UW',
    'れ': 'R EH',
    'ろ': 'R AA',
    # Begin with W
    'わ': 'W AH',
    'を': 'W AA',
    # Begin with G
    'が': 'G AH',
    'ぎ': 'G IY',
    'ぐ': 'G UW',
    'げ': 'G EH',
    'ご': 'G AA',
    # Begin with Z
    'ざ': 'Z AH',
    'じ': 'JH IY',
    'ず': 'Z UW',
    'ぜ': 'Z EH',
    'ぞ': 'Z AA',
    # Begin with D
    'だ': 'D AH',
    'ぢ': 'D JH IY',
    'づ': 'D S UW',
    'で': 'D EH',
    'ど': 'D AA',
    # Begin with B
    'ば': 'B AH',
    'び': 'B IY',
    'ぶ': 'B UW',
    'べ': 'B EH',
    'ぼ': 'B AA',
    # Begin with P
    'ぱ': 'P AH',
    'ぴ': 'P IY',
    'ぷ': 'P UW',
    'ぺ': 'P EH',
    'ぽ': 'P AA',
    # Begin with N
    'ん': 'N'
}

_modifier_phonemics = {
    'ゃ': 'AH',
    'ゅ': 'UW',
    'ょ': 'AA'
}

_modifiable_hiragana = [
    'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ぎ', 'じ', 'び', 'ぴ'
]

# We need to add the two character combinations...
for (char, modifier) in product(_modifiable_hiragana, _modifier_phonemics):
    combined_hiragana = char + modifier

    original_sound = _hiragana_phonemics[char].split(' ')[0]
    modifier_sound = _modifier_phonemics[modifier]

    should_add_y = char not in ['し', 'ち', 'じ']

    if should_add_y:
        modified_sound = original_sound + ' Y ' + modifier_sound
    else:
        modified_sound = original_sound + ' ' + modifier_sound
        
    _hiragana_phonemics[combined_hiragana] = modified_sound


def is_hiragana(char):
    if char in _hiragana_phonemics:
        return True

    return False


def is_hiragana_modifier(char):
    if char in _modifier_phonemics:
        return True

    if char == 'っ':
        return True

    return False


def is_hiragana_like(char):
    return is_hiragana(char) or is_hiragana_modifier(char)


# IDEA: Add support for stress levels for vowels (this could help to speed up matching words)
def to_pronounciation(syllable: str) -> Optional[str]:
    # We remove those pesky little tsu's that don't really change pronounciation
    # This is not 100% accurate. I know. Fite me.
    syllable = syllable.replace('っ', '')

    syllable_length = len(syllable)

    if syllable_length not in (1, 2):
        return None

    if syllable not in _hiragana_phonemics:
        return None

    return _hiragana_phonemics[syllable]
