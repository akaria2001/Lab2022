#!/bin/python3

"""
Useful Links I referenced when writing this script
Printing Coloured text
https://stackabuse.com/how-to-print-colored-text-in-python/
Sub Process to call external commands
https://docs.python.org/3/library/subprocess.html
www.it-howto.co.uk
For option detect OS and then run the correct command to update OS
rhel, zorin, ubuntu, rocky
"""


def print_yellow(text):
    print(f'\033[1;33m{text}\033[0;0m')


def print_red(text):
    print(f'\033[1;31m{text}\033[0;0m')


def print_green(text):
    print(f'\033[1;32m{text}\033[0;0m')


def print_blue(text):
    print(f'\033[1;34m{text}\033[0;0m')


def print_smiley(text):
    print(f'{text} \U0001F60F')


def print_folder():
    print('\U0001F4C1')


def print_tick(text):
    print(f'{text}\u2705')


def print_warning(text):
    print(f'\u274C\u274C\u274C\033[1;31m {text} \033[0;0m\u274C\u274C\u274C')
