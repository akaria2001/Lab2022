from itertools import cycle
from time import sleep
import subprocess as cmd
import random
from pyfiglet import Figlet
import argparse

def print_yellow(text):
    print(f'\033[1;33m{text}\033[0;0m')


def print_red(text):
    print(f'\033[1;31m{text}\033[0;0m')


def print_green(text):
    print(f'\033[1;32m{text}\033[0;0m')


def print_debug(text):
    print(f'\033[1;34m{text}\033[0;0m')


def print_smiley(text):
    print(f'{text} \U0001F60F')


def print_folder():
    print('\U0001F4C1')


def print_tick(text):
    print(f'{text}\u2705')


def print_warning(text):
    print(f'\u274C\u274C\u274C\033[1;31m {text} \033[0;0m\u274C\u274C\u274C')

def spiner():
    count = 0
    for frame in cycle(r'-\|/'):
        count = count + 1
        print('\r', frame, sep='', end='', flush=True)
        sleep(0.1)
        if count > 35:
            break

def countdown_timer(timer_val_secs):
    custom_fig = Figlet(font='standard', width=130)
    for count in range(timer_val_secs, -1, -1):
        cmd.call("clear", shell=False)
        print_yellow(custom_fig.renderText('Team Tool'))
        print_red(custom_fig.renderText(f"Countdown\nSeconds left : {count} "))
        sleep(1)

    
def names(file):
    file_list = []
    try:
        with open(file, 'r') as f:
            for line in f:
                file_list.append(line.strip())
    except FileNotFoundError:
        print_warning(f"File '{file}' doesn't exist, will exit")
        exit()
    return file_list


def main():
    cmd.call("clear", shell=False)
    custom_fig = Figlet(font='standard', width=140)
    print_yellow(custom_fig.renderText('Team Tool'))
    sleep(2)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str , required=True, help="filename")
    parser.add_argument('-t', '--timeseconds', type=str , required=True, help="time in seconds")
    parser.add_argument('-d', '--debug', required=False, help="Show debugging", action='store_true')
    args = parser.parse_args()
    debug = args.debug
    filename = args.filename
    time = args.timeseconds
    cmd.call(['clear'], shell=False)

    if(debug):
        print_debug("Debugging is enabled")
        print_debug(type(args))
        print_debug(args)
        print_debug(debug)
    else:
        print_green("Debugging is not enabled")

    spiner()


    cmd.call("clear", shell=False)
    if filename:
        print_green("Choosing engineer to run the session from the following list")
        for name in names(filename):
            print_green(name)
        sleep(3)
        cmd.call("clear", shell=False)
        name = custom_fig.renderText(random.choice(names(filename)))
        print_yellow(custom_fig.renderText("Today's session will be run by"))
        print_green(name)
        print_smiley("Let's go!!!")
        print_tick(f"Will start a {time} seconds countdown timer ")
        sleep(5)
        countdown_timer(int(time))


if __name__ == '__main__':
    main()

# ToDo
# Add Menu list invoked by argument to present different choices
