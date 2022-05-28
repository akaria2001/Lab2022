#!/bin/python3
import subprocess as cmd
import getpass
import print_colours
import labStatus
import cheeckInstancesExist

def generate_username():
    username = getpass.getuser()
    return username


def user_input():
    confirmation = input("You will delete any existing instances, Are you sure? - type 'yes' if you want to proceed : ")
    return confirmation


def destroyLab():
    if(cheeckInstancesExist.instancesExist()):
        print_colours.print_red("Instances found")
        labStatus.lab_status()
        confirmation = user_input()
        if(confirmation == 'yes'):
            print_colours.print_red(f"{generate_username()} has chosen {confirmation}: Instances will be deleted from the environment")
            command = "lxc list -c n -f csv"
            output = cmd.check_output(command.split(), shell=False)
            output = output.decode('utf8')
            for entry in output.split("\n"):
                if(len(entry) <= 1):
                    continue
                destroy_command = f"lxc delete -f {entry}"
                print_colours.print_red(f"Running command : {destroy_command}")
                cmd.call(destroy_command.split(), shell=False)
                labStatus.lab_status()
    else:
        print_colours.print_blue("No Instances found")
        

def main():
    cmd.call("clear", shell=False)
    destroyLab()

if __name__ == '__main__':
    main()