#!/bin/python3
import subprocess as cmd
import time
import getpass
import platform
import argparse

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

def generate_username():
    username = getpass.getuser()
    return username

def print_yellow(text):
    print(f'\033[1;33m{text}\033[0;0m')

def print_red(text):
    print(f'\033[1;31m{text}\033[0;0m')

def print_green(text):
    print(f'\033[1;32m{text}\033[0;0m')

def print_blue(text):
    print(f'\033[1;34m{text}\033[0;0m')

def user_input():
    confirmation = input("Are you sure? - type 'yes' if you want to proceed : ")
    return confirmation

def main():
    cmd.call("clear", shell=False)
    print_green("Parsing LXD Lab")
    command = "lxc list -f csv"
    output = cmd.check_output(command.split(), shell=False)
    output = output.decode('utf-8')
    for entry in output.split("\n"):
        processed = entry.split(",")
        print(type(processed[0]))
        destroy_command = f"lxc delete -f {processed[0]}"
        print_red(f"Running command : {destroy_command}")
        cmd.call(destroy_command.split(), shell=False)

if __name__ == '__main__':
    main()