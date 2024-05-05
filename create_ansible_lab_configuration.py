#!/bin/python3
import subprocess as cmd
import ipdb
import toml
import format_text


def read_stack():
    process_dict = toml.load("rocky-test-lab.toml")
    return process_dict


def generate_ansible_configuration():
        file = 'ansible-lab'
        linux_stack = read_stack()
        with open(file, 'w') as ansible_file:
            ansible_file.write('[lab]\n')
        format_text.print_green("Loading Stack Configuraton from toml file")
        for instance in linux_stack:
            with open(file, 'a') as ansible_file:
                instance_name = f"{instance}-{linux_stack[instance]['type']}"
                format_text.print_green(f"Checking {instance_name}")
                ansible_file.write(f"{instance_name}\n")


if __name__ == '__main__':
    generate_ansible_configuration()
