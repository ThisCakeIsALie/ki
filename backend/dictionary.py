import dawg
import re
import os.path

_WORD_FILE = '5000_words.txt'
_PRONOUNCIATION_TRIE_FILE = 'pronounciation.dawg'

words = None
pronounciations = None

with open(_WORD_FILE, encoding='utf-8') as file:
    english_words = file.read().split('\n')
    english_words = set(filter(lambda s: len(s) > 0 and not s.startswith('#'), english_words))
    words = english_words

def _init_pronounciations():
    global pronounciations
    if os.path.exists(_PRONOUNCIATION_TRIE_FILE):
        pronounciations = dawg.BytesDAWG().load(_PRONOUNCIATION_TRIE_FILE)
        return

    word_dict = {}

    import pronouncing
    pronouncing.init_cmu()

    def _remove_stresses(pronounciation):
        return re.sub(r"\d", "", pronounciation)


    for word, pronounciation in pronouncing.pronunciations:
        simplified_pronounciation = _remove_stresses(pronounciation)
        if word in words:
            word_dict[simplified_pronounciation] = word.encode('ascii')
        
    word_data = list(word_dict.items())

    pronounciations = dawg.BytesDAWG(word_data)
    pronounciations.save(_PRONOUNCIATION_TRIE_FILE)

_init_pronounciations()
