#!/bin/python3
import subprocess as cmd
import time
import getpass
import argparse
import print_colours
import labStatus
import destroyLab
import cheeckInstancesExist


def generate_username():
    username = getpass.getuser()
    return username


def user_input():
    message = """
Are you sure you want to recreate the Lab?
this will destroy any existing instaces?

type 'yes' if you want to proceed : """

    confirmation = input(message)
    print_colours.print_blue(f"Confirmation : {confirmation}")
    time.sleep(1)
    return confirmation


def create_instance(osType, instanceType, template):
    for number in (1, 2, 3):
        if(instanceType == "vm"):
            command = f"lxc launch {template} {osType}-{instanceType}-{number} --vm"
        else:
            command = f"lxc launch {template} {osType}-{instanceType}-{number}"
        print_colours.print_blue(f"Command to be run : {command}")
        cmd.call(command.split(), shell=False)
        time.sleep(5)


def createLab():
    print_colours.print_blue("Checking if any existing instances exist, remove if any found")
    if(cheeckInstancesExist.instancesExist()):
        user_input()
        destroyLab.destroyLab()
    else:
        print_colours.print_blue("No instances found, will continue")
    print_colours.print_green("Creating Lab")
    for os in ("rocky", "ubuntu"):
        for type in ("container", "vm"):
            if(os == "rocky"):
                template = "images:rockylinux/8"
                create_instance(os, type, template)
            else:
                template = "ubuntu:22.04"
                create_instance(os, type, template)
    time.sleep(10)
    labStatus.lab_status()


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
    labStatus.lab_status()

    createLab()


if __name__ == '__main__':
    main()
