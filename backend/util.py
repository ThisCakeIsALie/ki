from Levenshtein import distance
from lcs import lcs_distance
from math import ceil, floor

def prefix_suffix_pairs(lst):
    pairs = []

    for i in range(0, len(lst) + 1):
        prefix = lst[:i]
        suffix = lst[i:]

        pairs.append((prefix, suffix))

    return pairs

def syntax_distance(word1, word2):
    return distance(word1, word2)

def phonetic_distance(phones1, phones2):
    return lcs_distance(phones1, phones2)

def almost_floor(number):
    decimal_part = number % 1
    floored = floor(number)

    if decimal_part > 0.95:
        return floored + 1
    else:
        return floored

def percentage_substring(string, start_perc, end_perc):
    start_idx = almost_floor(len(string) * start_perc)
    end_idx = almost_floor(len(string) * end_perc)

    return string[start_idx:end_idx]
