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