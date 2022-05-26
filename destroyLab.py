#!/bin/python3
import subprocess as cmd
import getpass
import print_colours

def generate_username():
    username = getpass.getuser()
    return username

def lab_status():
    cmd.call("clear", shell=False)
    print_colours.print_yellow("Current Lab Status")
    cmd.call(["lxc", "list"], shell=False)


def user_input():
    confirmation = input("Are you sure? - type 'yes' if you want to proceed : ")
    return confirmation

def destroyLab():
        print_colours.print_red("Will destroy Lab!!!")
        confirmation = user_input()
        print_colours.print_green(f"You entered {confirmation}")

        if(confirmation == "yes"):
            print_colours.print_red("Destroying Lab")
        else:
            print_colours.print_green("Will retain the Lab")
            cmd.call("clear", shell=False)
        lab_status()

def main():
    cmd.call("clear", shell=False)
    command = "lxc list -f csv"
    output = cmd.check_output(command.split(), shell=False)
    output = output.decode('utf-8')
    if(len(output) == 0):
        print_colours.print_blue("No instances to remove")
        exit()
    lab_status()
    user_input()
    for entry in output.split("\n"):
        processed = entry.split(",")
        if(len(processed[0]) <= 1):
            continue
        destroy_command = f"lxc delete -f {processed[0]}"
        print_colours.print_red(f"Running command : {destroy_command}")
        cmd.call(destroy_command.split(), shell=False)
        lab_status()

if __name__ == '__main__':
    main()