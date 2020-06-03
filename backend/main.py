import sys
from analyse import analyse
from display import print_word_info, print_error_message


if len(sys.argv) < 2:
    print_error_message('Ooops, something went wrong. Have you supplied a word to be approximated?')
    exit(1)

actual_arguments = sys.argv[1:]
word = ' '.join(actual_arguments)

try:
    info = analyse(word)
    print_word_info(info)
except:
    print_error_message('Ooops, something went wrong internally!')
