#!/bin/python3
import subprocess as cmd
import coloured_text


def instancesExist():
    command = "lxc list -c n -f csv"
    output = cmd.check_output(command.split(), shell=False)
    output = output.decode('utf8')
    if(len(output) == 0):
        return False
    else:
        return True


def main():
    coloured_text.print_green("Checking if any instances exist")
    coloured_text.print_blue(f"{instancesExist()}")


if __name__ == '__main__':
    main()