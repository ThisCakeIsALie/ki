import util
import english
from japanese import to_roman_syllables, to_pronounciation
from english import similar_word, similar_phones, pronounciation_to_word
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

@lru_cache(maxsize=4096)
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

        candidate_match = similar_word(candidate)
        candidate_cost = util.syntax_distance(candidate_match, candidate)

        used_percentage = 1
        matched_percentage = len(candidate) / full_len

        return candidate_match, candidate_cost, used_percentage, matched_percentage

    return generate_best_approximation(tuple(syllables), approximator, alpha)

def approximate_word_phonetic(word, alpha=0.75):
    pronounciation = to_pronounciation(word)
    phonemes = pronounciation.split(' ')

    full_len = len(phonemes)

    def approximator(prefix):
        candidate_phones = similar_phones(prefix)
        candidate_word = pronounciation_to_word(candidate_phones)
        candidate_cost = util.phonetic_distance(candidate_phones, prefix)

        used_percentage = 1
        matched_percentage = len(prefix) / full_len

        return candidate_word, candidate_cost, used_percentage, matched_percentage

    return generate_best_approximation(tuple(phonemes), approximator, alpha)
