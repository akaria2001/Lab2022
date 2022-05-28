#!/bin/python3
import subprocess as cmd
import time
import getpass
import platform
import argparse
import print_colours

def generate_username():
    username = getpass.getuser()
    return username

def generate_menu():
    menu_items = [[1, 'OS Upgrade', '/home/akaria/bin/os_update.sh'],
                  [2, 'Show System Information', 'neofetch'],
                  [3, 'Show System Usage using bashtop', 'bashtop'],
                  [4, 'Show System Usage using glances', 'glances'],
                  [5, 'Show current lab (qemu vm and lxc container machines)', 'lxc list'],
                  [6, 'Spin Up Sample Lab', '/home/akaria/bin/spinUpSampleLab.py'],
                  [7, 'Destroy Lab', '/home/akaria/bin/destroyLab.py'],
                  [8, 'Show Hardware Information', 'sudo lshw'],
                  [9, 'Show Uptime and Load Average', 'uptime'],
                  [10, 'Show contents of current directory', 'ls -la']]
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
                    print_colours.print_blue(f"You have chosen : {choice[1]}")
                    print_colours.print_blue(f"Will run command : '{choice[2]}'")
                    cmd.call("clear", shell=False)
                    cmd.call(choice[2].split(), shell=False)
                    time.sleep(1)
                    input("Press any key to continue : ")
                    cmd.call("clear", shell=False)
                    break


if __name__ == '__main__':
    main()