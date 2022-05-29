#!/bin/python3
import subprocess as cmd
import time
import getpass
import platform
import argparse
import labStatus
import spinUpSampleLab
import destroyLab
import print_colours


def generate_username():
    username = getpass.getuser()
    return username


def generate_menu():
    menu_items = [[1, 'OS Upgrade', '/home/akaria/bin/os_update.sh', 'command'],
                  [2, 'Show System Information', 'neofetch', 'command'],
                  [3, 'Show System Usage using bashtop', 'bashtop', 'command'],
                  [4, 'Show System Usage using glances', 'glances', 'command'],
                  [5, 'Show current lab (qemu vm and lxc container machines)', 'labStatus.lab_status()', 'module'],
                  [6, 'Spin Up Sample Lab', 'spinUpSampleLab.createLab()', 'module'],
                  [7, 'Destroy Lab', 'destroyLab.destroyLab()', 'module'],
                  [8, 'Show Hardware Information', 'sudo lshw', 'command'],
                  [9, 'Show Uptime and Load Average', 'uptime', 'command'],
                  [10, 'Show contents of current directory', 'ls -la', 'command']]
    return menu_items


def grab_os():
    osversion = "Unknown"
    try:
        with open("/etc/lsb-release") as file:
            osversion = file.read()
    except FileNotFoundError:
        print_colours.print_red("Unable to detect OS Version")
        next
    return osversion.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', required=False, help="Show debugging", action='store_true')
    args = parser.parse_args()
    debug = args.debug
    cmd.call("clear", shell=False)

    if(debug):
        print_colours.print_blue("Debugging is enabled")
        print_colours.print_blue(type(args))
        print_colours.print_blue(args)
        print_colours.print_blue(debug)
        time.sleep(3)
    else:
        print_colours.print_yellow("Debugging is not enabled")
        time.sleep(1)

    cmd.call("clear", shell=False)
    time.sleep(1)

    while(True):
        print_colours.print_yellow(f"Hello {generate_username()}, welcome to Lab Menu")
        print_colours.print_green(r"""
    .--.
   |o_o |
   |:_/ |
  //   \ \
 (|     | )
/'\_   _/`\
\___)=(___/

       """)
        if(debug):
            print_colours.print_blue(f"OS Version: {grab_os()}")
            print_colours.print_blue(f"Python Version: {platform.python_version()}\n")

        for menu_item in generate_menu():
            print_colours.print_green(f"{menu_item[0]}:\t{menu_item[1]}")
        print_colours.print_red("0:\tExit Application")
        user_choice = 99
        try:
            user_choice = int(input("Please select option : "))
        except ValueError:
            print_colours.print_red("Please enter a valid choice")
        except UnboundLocalError:
            print_colours.print_red("Please enter a valid choice")
        if user_choice == 0:
            cmd.call("clear", shell=False)
            exit()
        else:
            cmd.call("clear", shell=False)
            for choice in generate_menu():
                if(user_choice == choice[0]):
                    if(choice[3] == 'command'):
                        print_colours.print_blue("Choice is Linux Command")
                        input("Press any key to continue : ")
                        print_colours.print_blue(f"You have chosen : {choice[1]}")
                        print_colours.print_blue(f"Will run command : '{choice[2]}'")
                        cmd.call("clear", shell=False)
                        cmd.call(choice[2].split(), shell=False)
                        time.sleep(1)
                    else:
                        print_colours.print_blue("Choice is a Python Module")
                        input("Press any key to continue : ")
                        print_colours.print_blue(f"You have chosen : {choice[1]}")
                        print_colours.print_blue(f"Will run module : {choice[2]}")
                        time.sleep(2)
                        eval(choice[2])
                        time.sleep(1)
                    input("Press any key to continue : ")
                    cmd.call("clear", shell=False)
                    break


if __name__ == '__main__':
    main()
