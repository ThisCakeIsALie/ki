import util
import english
from japanese import to_roman_syllables, to_pronounciation
from english import syntactically_similar_word, phonetically_similar_word
from dataclasses import dataclass
from typing import List
from functools import lru_cache


@dataclass
class WordApproximation:
    words: List[str]
    # How much of the corresponding word is actually used
    word_used_percentages: List[float]
    # How much of the original word this word approximates
    word_matched_percentages: List[float]
    cost: float  # lower is better


def _is_useful_partition(partition):
    for segment in partition[:-1]:
        if len(segment) < 2:
            return False

    return True


def generate_approximation_syntactical(partition):
    avg_cost = 0
    total_length = 0
    words = []
    word_used_percentages = []
    word_matched_percentages = []

    for segment in partition:
        candidate_word = ''.join(segment)

        closest_word = syntactically_similar_word(candidate_word)
        cost = util.word_distance(closest_word, candidate_word)

        words.append(closest_word)
        word_used_percentages.append(1)
        word_matched_percentages.append(len(candidate_word))

        total_length += len(candidate_word)
        avg_cost += cost / len(partition)

    word_matched_percentages = list(
        map(lambda size: size / total_length, word_matched_percentages))

    return WordApproximation(words, word_used_percentages, word_matched_percentages, avg_cost)


def word_approximations_syntactical(word: str) -> List[WordApproximation]:
    syl = to_roman_syllables(word)
    partitions = util.partitions(syl)

    partitions = filter(_is_useful_partition, partitions)
    approximations = map(generate_approximation_syntactical, partitions)

    return list(approximations)


@lru_cache
def generate_approximations_phonetical(phonemes: str, full_phone_len, alpha, optimal) -> List[WordApproximation]:
    if len(phonemes) == 0:
        return [WordApproximation([], [], [], 0)]

    matches = []

    for i in range(len(phonemes), 0, -1):
        prefix = phonemes[:i]

        result = phonetically_similar_word(prefix)
        if result is None:
            continue

        (word, overshoot) = result

        used_percentage = len(prefix) / (len(prefix) + overshoot)
        matched_percentage = len(prefix) / full_phone_len

        suffix = phonemes[i:]
        rest_solutions = generate_approximations_phonetical(
            tuple(suffix), full_phone_len, alpha, optimal)

        for old_solution in rest_solutions:
            new_cost = old_solution.cost + alpha * 1 + (1 - alpha) * overshoot
            new_words = [word] + old_solution.words
            new_used_percentages = [used_percentage] + \
                old_solution.word_used_percentages
            new_matched_percentages = [
                matched_percentage] + old_solution.word_matched_percentages

            new_solution = WordApproximation(
                new_words, new_used_percentages, new_matched_percentages, new_cost)

            matches.append(new_solution)

            if not optimal:
                return matches

    return matches


def word_approximations_phonetical(word: str, alpha=0.75, optimal=True) -> List[WordApproximation]:
    pronounciation = to_pronounciation(word)
    phonemes = pronounciation.split(' ')

    return generate_approximations_phonetical(tuple(phonemes), len(phonemes), alpha, optimal)


def approximate_word(word: str, phonetic=True, **kwargs) -> WordApproximation:
    approximator = word_approximations_phonetical if phonetic else word_approximations_syntactical
    approximations = approximator(word, **kwargs)

    best_approx = min(approximations, key=lambda approx: approx.cost)

    return best_approx
