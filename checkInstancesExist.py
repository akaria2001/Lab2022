#!/bin/python3
import subprocess as cmd
import print_colours

def instancesExist():
    command = "lxc list -c n -f csv"
    output = cmd.check_output(command.split(), shell=False)
    output = output.decode('utf8')
    if(len(output) == 0):
        return False
    else:
        return True

def main():
    print_colours.print_green("Checking if any instances exist")
    print_colours.print_blue(f"{instancesExist()}")

if __name__ == '__main__':
    main()
