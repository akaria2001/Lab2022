#!/bin/python3
import subprocess as cmd
import format_text


def check_lxd_installed():
    command = "lxc list -c n -f csv"
    try:
        cmd.check_output(command.split(), shell=False)
        return True
    except FileNotFoundError:
        return False


def main():
    format_text.print_green("Checking if any instances exist")
    format_text.print_blue(f"{check_lxd_installed()}")


if __name__ == '__main__':
    main()
