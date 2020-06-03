from Levenshtein import ratio
from math import ceil, floor

def partitions(lst):
    if len(lst) == 0:
        return [[]]

    parts = []
    for i in range(1, len(lst) + 1):
        start = lst[:i]
        rest = lst[i:]
        for rest_partition in partitions(rest):
            parts.append([start] + rest_partition)

    return parts

def word_distance(word1, word2):
    return 1 - ratio(word1, word2)

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
