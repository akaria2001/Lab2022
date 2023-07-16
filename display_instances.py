#!/bin/python3
import subprocess as cmd
import format_text


def return_instances():
    command = "lxc list -c n -f csv"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
    return instances


def main():
    format_text.print_green("Running Instances")
    format_text.print_blue(f"{return_instances()}")


if __name__ == '__main__':
    main()
