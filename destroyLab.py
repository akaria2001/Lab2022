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

def lab_status():
    cmd.call("clear", shell=False)
    print_yellow("Current Lab Status")
    cmd.call(["lxc", "list"], shell=False)

def destroyLab(debug):
        print_red("Will destroy Lab!!!")
        confirmation = user_input()
        print_green(f"You entered {confirmation}")

        if(confirmation == "yes"):
            print_red("Destroying Lab")
            destroy_lab_kludge = "/home/akaria/bin/destroyLab.sh"
            cmd.call(destroy_lab_kludge.split(), shell=False)
        else:
            print_green("Will retain the Lab")
            cmd.call("clear", shell=False)
        lab_status()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', required=False, help="Show debugging", action='store_true')
    args = parser.parse_args()
    debug = args.debug
    cmd.call("clear", shell=False)

    if(debug):
       print_blue("DEBUG: Debugging is enabled")
       print_blue(f"DEBUG: {type(args)}")
       print_blue(f"DEBUG: {args}")
       print_blue(f"DEBUG: {debug}")
       time.sleep(3)
    else:
        print_yellow("Debugging is not enabled")
        time.sleep(1)
    
    cmd.call("clear", shell=False)
    time.sleep(1)
    lab_status()

    destroyLab(debug)


if __name__ == '__main__':
    main()
