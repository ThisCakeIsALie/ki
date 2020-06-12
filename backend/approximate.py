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


def extend_solution(solution, word, cost, used_percentage, matched_percentage):
        new_cost = cost
        new_words = [word] + solution.words
        new_used_percentages = [used_percentage] + \
            solution.word_used_percentages
        new_matched_percentages = [
            matched_percentage] + solution.word_matched_percentages

        new_solution = WordApproximation(
            new_words, new_used_percentages, new_matched_percentages, new_cost)

        return new_solution

@lru_cache
def generate_best_approximation(syllables, approximate_prefix, alpha):
    if len(syllables) == 0:
        return WordApproximation([], [], [], 0)

    prefix_suffix_pairs = util.prefix_suffix_pairs(syllables)

    solutions = []
    for prefix, suffix in prefix_suffix_pairs:
        if len(prefix) == 0:
            continue

        prefix_approx = approximate_prefix(prefix)

        if prefix_approx is None:
            continue

        (word, prefix_cost, used_percentage, matched_percentage) = prefix_approx

        rest_solution = generate_best_approximation(suffix, approximate_prefix, alpha)

        cost = rest_solution.cost + alpha * 1 + (1 - alpha) * prefix_cost
        solution = extend_solution(rest_solution, word, cost, used_percentage, matched_percentage)

        solutions.append(solution)

    best_solution = min(solutions, key=lambda sol: sol.cost)

    return best_solution

def approximate_word_syntactical(word, alpha=0.75):
    syllables = to_roman_syllables(word)
    full_len = len(syllables)

    def approximator(prefix):
        candidate = ''.join(prefix)

        candidate_match = syntactically_similar_word(candidate)
        candidate_cost = util.word_distance(candidate_match, candidate)

        used_percentage = 1
        matched_percentage = len(candidate) / full_len

        return candidate_match, candidate_cost, used_percentage, matched_percentage

    return generate_best_approximation(tuple(syllables), approximator, alpha)

def approximate_word_phonetic(word, alpha=0.75):
    pronounciation = to_pronounciation(word)
    phonemes = pronounciation.split(' ')

    full_len = len(phonemes)

    def approximator(prefix):
        result = phonetically_similar_word(prefix)

        if result is None:
            return None

        (candidate_match, candidate_cost) = result

        used_percentage = len(prefix) / (len(prefix) + candidate_cost)
        matched_percentage = len(prefix) / full_len

        return candidate_match, candidate_cost, used_percentage, matched_percentage

    return generate_best_approximation(tuple(phonemes), approximator, alpha)

"""
@lru_cache
def generate_best_approximation_syntactical(syllables, full_phone_len, alpha):
    if len(syllables) == 0:
        return WordApproximation([], [], [], 0)

    best_solutions = []

    for i in range(1, len(syllables) + 1):
        prefix = syllables[:i]

        candidate_word = ''.join(prefix)

        word = syntactically_similar_word(candidate_word)
        cost = util.word_distance(word, candidate_word)

        used_percentage = 1
        matched_percentage = len(candidate_word) / full_phone_len

        suffix = syllables[i:]
        old_solution = generate_best_approximation_syntactical(
            suffix, full_phone_len, alpha)

        new_cost = old_solution.cost + alpha * 1 + (1 - alpha) * cost
        new_words = [word] + old_solution.words
        new_used_percentages = [used_percentage] + \
            old_solution.word_used_percentages
        new_matched_percentages = [
            matched_percentage] + old_solution.word_matched_percentages

        new_solution = WordApproximation(
            new_words, new_used_percentages, new_matched_percentages, new_cost)

        best_solutions.append(new_solution)


    return min(best_solutions, key=lambda sol: sol.cost)

@lru_cache
def generate_best_approximation_phonetic(phonemes, full_phone_len, alpha):
    if len(phonemes) == 0:
        return WordApproximation([], [], [], 0)

    best_solutions = []

    for i in range(1, len(phonemes) + 1):
        prefix = phonemes[:i]

        result = phonetically_similar_word(prefix)
        if result is None:
            continue

        (word, overshoot) = result

        used_percentage = len(prefix) / (len(prefix) + overshoot)
        matched_percentage = len(prefix) / full_phone_len

        suffix = phonemes[i:]
        old_solution = generate_best_approximation_phonetic(
            tuple(suffix), full_phone_len, alpha)

        new_cost = old_solution.cost + alpha * 1 + (1 - alpha) * overshoot
        new_words = [word] + old_solution.words
        new_used_percentages = [used_percentage] + \
            old_solution.word_used_percentages
        new_matched_percentages = [
            matched_percentage] + old_solution.word_matched_percentages

        new_solution = WordApproximation(
            new_words, new_used_percentages, new_matched_percentages, new_cost)

        best_solutions.append(new_solution)

    return min(best_solutions, key=lambda sol: sol.cost)

def approximate_word_phonetic(word: str, alpha=0.75) -> WordApproximation:
    pronounciation = to_pronounciation(word)
    phonemes = pronounciation.split(' ')

    return generate_best_approximation_phonetic(tuple(phonemes), len(phonemes), alpha)


def approximate_word_syntactical(word: str, alpha=0.75) -> WordApproximation:
    syl = to_roman_syllables(word)

    return generate_best_approximation_syntactical(tuple(syl), len(word), alpha)
"""