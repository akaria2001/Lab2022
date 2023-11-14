#!/bin/python3
import subprocess as cmd
import ipdb
import toml
import format_text
import re

def read_stack():
    process_dict = toml.load("kubernetes_vms.toml")
    return process_dict

# scrappy script - will improve on next iteration - will break if more than one controller defined in toml
def generate_ansible_configuration():
        file = 'ansible-hosts'
        linux_stack = read_stack()
        format_text.print_green("Loading Stack Configuraton from toml file")
        with open(file, 'w') as ansible_file:
             ansible_file.write("\n[k8sworkers]\n")
        for instance in linux_stack:
            with open(file, 'a') as ansible_file:
                instance_name = f"{instance}-{linux_stack[instance]['type']}"
                format_text.print_green(f"Checking {instance_name}")
                pattern = "k8sworker"
                # ipdb.set_trace()
                if re.match(pattern, instance_name):
                    ansible_file.write(f"{instance_name}\n")

        with open(file, 'a') as ansible_file:
             ansible_file.write("\n[k8scontroller]\n")
        for instance in linux_stack:
            with open(file, 'a') as ansible_file:
                instance_name = f"{instance}-{linux_stack[instance]['type']}"
                format_text.print_green(f"Checking {instance_name}")
                pattern = "k8scontroller"
                # ipdb.set_trace()
                if re.match(pattern, instance_name):
                    ansible_file.write(f"{instance_name}\n")


if __name__ == '__main__':
    generate_ansible_configuration()

