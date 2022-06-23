#!/bin/python3
import subprocess as cmd
import time
import getpass
import platform
import argparse
import lab_status
import spin_up_lab
import tear_down_lab
import format_text
import check_lxd_installed


def generate_username():
    username = getpass.getuser()
    return username


def generate_menu():
    menu_items = [[1, 'OS Upgrade', '/home/akaria/bin/os_update.sh', 'command'],
                  [2, 'Show System Information', 'neofetch', 'command'],
                  [3, 'Show System Usage using bashtop', 'bashtop', 'command'],
                  [4, 'Show System Usage using glances', 'glances', 'command'],
                  [5, 'Show current lab (qemu vm and lxc container machines)', 'lab_status.display()', 'module'],
                  [6, 'Spin Up Sample Lab', 'spin_up_lab.create()', 'module'],
                  [7, 'Destroy Lab', 'tear_down_lab.destroy()', 'module'],
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
        format_text.print_red("Unable to detect OS Version")
        next
    return osversion.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', required=False, help="Show debugging", action='store_true')
    args = parser.parse_args()
    debug = args.debug
    cmd.call("clear", shell=False)

    if(debug):
        format_text.print_blue("Debugging is enabled")
        format_text.print_blue(type(args))
        format_text.print_blue(args)
        format_text.print_blue(debug)
        time.sleep(3)
    else:
        format_text.print_yellow("Debugging is not enabled")
        time.sleep(1)

    cmd.call("clear", shell=False)
    time.sleep(1)

    if(check_lxd_installed.check_lxd_installed()):
        format_text.print_blue("Detected LXD Installed")
    else:
        format_text.print_red("LXD not installed - will exit")
        format_text.print_blue("Install LXD by running the following command")
        format_text.print_green("sudo snap install lxd")
        format_text.print_blue("Then configure lxd by running")
        format_text.print_green("lxd init")
        exit()

    while(True):
        welcome = f"Hello {generate_username()}, welcome to Lab Menu"
        format_text.print_yellow(welcome)
        format_text.print_green(r"""
    .--.
   |o_o |
   |:_/ |
  //   \ \
 (|     | )
/'\_   _/`\
\___)=(___/

       """)
        if(debug):
            format_text.print_blue(f"OS Version: {grab_os()}")
            format_text.print_blue(f"Python Version: {platform.python_version()}\n")

        for menu_item in generate_menu():
            format_text.print_green(f"{menu_item[0]}:\t{menu_item[1]}")
        format_text.print_red("0:\tExit Application")
        user_choice = 99
        try:
            user_choice = int(input("Please select option : "))
        except ValueError:
            format_text.print_red("Please enter a valid choice")
        except UnboundLocalError:
            format_text.print_red("Please enter a valid choice")
        if user_choice == 0:
            cmd.call("clear", shell=False)
            exit()
        else:
            cmd.call("clear", shell=False)
            for choice in generate_menu():
                if(user_choice == choice[0]):
                    if(choice[3] == 'command'):
                        format_text.print_blue("Choice is Linux Command")
                        input("Press any key to continue : ")
                        format_text.print_blue(f"You have chosen : {choice[1]}")
                        format_text.print_blue(f"Will run command : '{choice[2]}'")
                        cmd.call("clear", shell=False)
                        cmd.call(choice[2].split(), shell=False)
                        time.sleep(1)
                    else:
                        format_text.print_blue("Choice is a Python Module")
                        input("Press any key to continue : ")
                        format_text.print_blue(f"You have chosen : {choice[1]}")
                        format_text.print_blue(f"Will run module : {choice[2]}")
                        time.sleep(2)
                        eval(choice[2])
                        time.sleep(1)
                    input("Press any key to continue : ")
                    cmd.call("clear", shell=False)
                    break


if __name__ == '__main__':
    main()
