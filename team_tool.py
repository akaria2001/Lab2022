from itertools import cycle
from time import sleep
import subprocess as cmd
import random
from pyfiglet import Figlet


def spiner():
    count = 0
    for frame in cycle(r'-\|/'):
        count = count + 1
        print('\r', frame, sep='', end='', flush=True)
        sleep(0.1)
        if count > 35:
            break
    
def names():
    return ['leo',
            'cristan',
            'mo',
            'bobby',
            'luis']


def main():
    cmd.call("clear", shell=False)
    custom_fig = Figlet(font='starwars')
    print(custom_fig.renderText('Team Tool'))
    spiner()
    cmd.call("clear", shell=False)
    print(custom_fig.renderText("Today's session will be run by\n\n"))
    print(custom_fig.renderText(random.choice(names())))

if __name__ == '__main__':
    main()

# ToDo
# Use file with list off names
# Add arguments for return name, countdown timer in seconds or minutes
# Add Menu list invoked by argument to present different choices