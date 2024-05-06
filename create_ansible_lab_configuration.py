#!/bin/python3
import subprocess as cmd
import ipdb
import toml
import json
import format_text


def read_stack():
    process_dict = toml.load("rocky-test-lab.toml")
    return process_dict


def return_instances():
    command = "lxc list -f json"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
    lab_stack = json.loads(instances)
    return lab_stack


def generate_ansible_configuration():
        file = 'ansible-lab'
        with open(file, 'w') as ansible_file:
            ansible_file.write('[lab]\n')
        for instance in return_instances():
             format_text.print_green(f"Instance {instance['name']} found - adding to Ansible inventory")
             with open(file, 'a') as ansible_file:
                  ansible_file.write(f"{instance['name']}\n")


if __name__ == '__main__':
    generate_ansible_configuration()
