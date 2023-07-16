#!/bin/python3
import subprocess as cmd
import format_text
import ipdb


def return_instances():
    instance_list = []
    command = "lxc list -c n -f csv"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
    instance_list = instances.split()
    return instance_list


def main():
    format_text.print_green("Running Instances")
    return_instances()
    instances = return_instances()
    format_text.print_blue(f"{instances}")


if __name__ == '__main__':
    main()
