import dawg
import re
import os
import os.path
import pronouncing
pronouncing.init_cmu()

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_WORD_FILE = os.path.join(_THIS_FOLDER, '5000_words.txt')

_PRONOUNCIATION_TRIE_FILE = os.path.join(_THIS_FOLDER, 'pronounciation.dawg')

words = None
pronounciations = {}

with open(_WORD_FILE, encoding='utf-8') as file:
    english_words = file.read().split('\n')
    english_words = set(filter(lambda s: len(s) > 0 and not s.startswith('#'), english_words))
    words = english_words

words = frozenset(words)

def _remove_stresses(pronounciation):
    return re.sub(r"\d", "", pronounciation)

for word, pronounciation in pronouncing.pronunciations:
    simplified_pronounciation = _remove_stresses(pronounciation)
    if word in words:
        pronounciations[tuple(simplified_pronounciation.split(' '))] = word

