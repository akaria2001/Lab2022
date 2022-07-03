#!/bin/python3
import subprocess as cmd
import time
import getpass
import platform
import argparse
import lab_status
import tear_down_lab
import format_text
import check_lxd_installed


def generate_username():
    username = getpass.getuser()
    return username


def create_instances():
    format_text.print_green("Will create one instance for each OS")
    format_text.print_red("This will delete all running instances first")
    tear_down_lab.destroy()
    for OS in generate_menu():
        instance_name = OS[1].replace(' ', '-')
        print(f"Creating LXC Instance {OS[0]} : {instance_name}")
        print(f"Allocating 4CPU and 4GB RAM to {instance_name}")
        create = f"lxc init {OS[2]} {instance_name}"
        cpucfg = f"lxc config set {instance_name} limits.cpu 4"
        ramcfg = f"lxc config set {instance_name} limits.memory 4GB"
        start_instance = f"lxc start {instance_name}"
        cmd.call(create.split(), shell=False, stdout=None)
        cmd.call(cpucfg.split(), shell=False, stdout=None)
        cmd.call(ramcfg.split(), shell=False, stdout=None)
        cmd.call(start_instance.split(), shell=False, stdout=None)
        format_text.print_tick("Success")
        if(OS[0] >= 11):
            break
        time.sleep(10)
    lab_status.display()


def generate_menu():
    menu_items = [[1, 'Arch Linux', 'images:archlinux'],
                  [2, 'Fedora 36 Linux', 'images:fedora/36'],
                  [3, 'Debian 12 Linux', 'images:debian/12'],
                  [4, 'Rocky 8 Linux', 'images:rockylinux/8'],
                  [5, 'Alma 8 Linux', 'images:almalinux/8'],
                  [6, 'Alma 9 Linux', 'images:almalinux/9'],
                  [7, 'Ubuntu 22 Linux', 'ubuntu:22.04'],
                  [8, 'CentOS 9 Linux Stream', 'images:centos/9-Stream'],
                  [9, 'CentOS 8 Linux Stream', 'images:centos/8-Stream'],
                  [10, 'Alpine Linux', 'images:alpine/3.16'],
                  [11, 'Kali Linux', 'images:kali'],
                  [12, 'Create one instance of each types', 'all'],
                  [13, 'Delete all Instances', 'tear_down_lab.destroy()']]
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
        welcome = f"Hello {generate_username()}, welcome to Linux Lab"
        format_text.print_yellow(welcome)
        format_text.print_smiley("Lets have some fun ... ")
        format_text.print_green("In this Lab you can easily setup a test")
        format_text.print_green("Linux System Container Instance")
        format_text.print_green("Please select from the choice below")
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
                    if(choice[0] == 13):
                        format_text.print_red("Will delete running instances")
                        input("Press any key to continue : ")
                        cmd.call("clear", shell=False)
                        tear_down_lab.destroy()
                        time.sleep(1)
                        break
                    if(choice[0] == 12):
                        create_instances()
                    else:
                        format_text.print_blue("Will create LXC System Container Instance")
                        input("Press any key to continue : ")
                        format_text.print_blue(f"You have chosen to create : {choice[1]}")
                        instance_name = input("Please enter name off the Instance : ")
                        time.sleep(1)
                        spin_up = f"lxc launch {choice[2]} {instance_name.replace(' ', '-')}"
                        cmd.call(spin_up.split(), shell=False)
                        time.sleep(1)
                    input("Press any key to continue : ")
                    cmd.call("clear", shell=False)
                    break


if __name__ == '__main__':
    main()
