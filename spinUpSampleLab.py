#!/bin/python3
import subprocess as cmd
import time
import getpass
import argparse
import print_colours

def generate_username():
    username = getpass.getuser()
    return username

def user_input():
    confirmation = input("Are you sure you want to recreate the Lab, this will destroy the existing Lab? - type 'yes' if you want to proceed : ")
    return confirmation

def lab_status():
    cmd.call("clear", shell=False)
    print_colours.print_yellow("Current Lab Status")
    cmd.call(["lxc", "list"], shell=False)

def createLab(debug):
    if (debug):
        print_colours.print_blue("DEBUG: Debugging enabled")
    print_colours.print_yellow("Current Lab Status")
    lab_status()
    confirmation = user_input()
    print_colours.print_green(f"You entered {confirmation}")

    if(confirmation == "yes"):
        destroyCmd = "/home/akaria/bin/destroyLab.py"
        cmd.call(destroyCmd, shell=False)
        print_colours.print_red("Creating Lab")
        for instanceType in ("LXC Container", "QEMU Virtual Machine"):
            print_colours.print_green(f"Instance Type to be created is {instanceType}")
            for osType in ("Rocky 8 Linux", "Ubuntu 22.04 Server Linux"):
                print_colours.print_green(f"Will provision OS : {osType}")
                command = ""
                if(instanceType == "LXC Container"):
                    for number in (1, 2, 3, 4):
                        print_colours.print_yellow(f"Creating {instanceType}:{osType}:{number}")
                        if(osType == "Rocky 8 Linux"):
                            command = f"lxc launch images:rockylinux/8 rocky-container-{number}"
                            print_colours.print_blue(f"Command to be run : {command}")
                            cmd.call(command.split(), shell=False)
                            time.sleep(5)
                        else:
                            command = f"lxc launch ubuntu:22.04 ubuntu-container-{number}"
                            print_colours.print_blue(f"Command to be run : {command}")
                            cmd.call(command.split(), shell=False)
                            time.sleep(5)                           
                else:
                    for number in (1, 2):
                        print_colours.print_yellow(f"Creating {instanceType}:{osType}:{number}")
                        if(osType == "Rocky 8 Linux"):
                            command = f"lxc launch images:rockylinux/8 rocky-vm-{number} --vm"
                            print_colours.print_blue(f"Command to be run : {command}")
                            cmd.call(command.split(), shell=False)
                            time.sleep(10)
                        else:
                            command = f"lxc launch ubuntu:22.04 ubuntu-vm-{number} --vm"
                            print_colours.print_blue(f"Command to be run : {command}")
                            cmd.call(command.split(), shell=False)
                            time.sleep(10)                           

        time.sleep(5)
    else:
        print_colours.print_green("Will not create the Lab")
        cmd.call("clear", shell=False)
    lab_status()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', required=False, help="Show debugging", action='store_true')
    args = parser.parse_args()
    debug = args.debug
    cmd.call("clear", shell=False)

    if(debug):
       print_colours.print_blue("DEBUG: Debugging is enabled")
       print_colours.print_blue(f"DEBUG: {type(args)}")
       print_colours.print_blue(f"DEBUG: {args}")
       print_colours.print_blue(f"DEBUG: {debug}")
       time.sleep(3)
    else:
        print_colours.print_yellow("Debugging is not enabled")
        time.sleep(1)
    
    cmd.call("clear", shell=False)
    time.sleep(1)
    lab_status()

    createLab(debug)


if __name__ == '__main__':
    main()
