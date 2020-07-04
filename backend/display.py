import operator
import util
from rich.console import Console
from itertools import accumulate

console = Console()

COLORS = ['bright_cyan', 'bright_magenta',
          'bright_blue', 'bright_green', 'bright_yellow']


def color_wheel():
    while True:
        for color in COLORS:
            yield color


def display_approx(approx):
    words = approx.words

    colored_words = []
    for word, color in zip(words, color_wheel()):
        colored_words.append(f'[{color}]{word}[/{color}]')

    return '·'.join(colored_words)


def display_syllables(syllables, approx):
    joined_syll = ''.join(syllables)

    percentages = approx.word_matched_percentages
    accumulated_percentages = accumulate(percentages, func=operator.add)

    char_colors = []

    last_perc = 0
    for perc, color in zip(accumulated_percentages, color_wheel()):
        color_part = util.percentage_substring(joined_syll, last_perc, perc)

        part_length = len(color_part)
        char_colors.extend(part_length * [color])
        last_perc = perc

    char_colors_iter = iter(char_colors)
    colored_syllables = []
    for syllable in syllables:
        colored_syllable = ''

        for char in syllable:
            char_color = next(char_colors_iter)
            colored_char = f'[{char_color}]{char}[/{char_color}]'
            colored_syllable += colored_char

        colored_syllables.append(colored_syllable)

    return '·'.join(colored_syllables)


def print_word_info(info):
    original = '    '
    approximation = '    '

    console.print()

    original = info.original
    phonetic_approx = 'That sounds like... ' + \
        display_approx(info.phonetic_approx)
    syntactic_approx = 'That looks like... ' + \
        display_approx(info.syntactic_approx)
    syllables = display_syllables(info.syllables, info.phonetic_approx)

    console.print(original + ' (' + syllables + ')', justify='center')
    console.print(phonetic_approx, justify='center')
    console.print(syntactic_approx, justify='center')
    console.print()

def print_error_message(message):
    console.print(f'[bright_red]Error[/bright_red]: {message}')