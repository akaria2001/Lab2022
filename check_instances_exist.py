#!/bin/python3
import subprocess as cmd
import format_text


def verify():
    command = "lxc list -c n -f csv"
    output = cmd.check_output(command.split(), shell=False)
    output = output.decode('utf8')
    if(len(output) == 0):
        return False
    else:
        return True


def main():
    format_text.print_green("Checking if any instances exist")
    format_text.print_blue(f"{verify()}")


if __name__ == '__main__':
    main()
