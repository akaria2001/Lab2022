#!/bin/python3
import subprocess as cmd
import ipdb
import toml
import format_text
import re
import shutil

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


def generate_playbook(user):
    source_file = "ansible-microk8s.yml.template"
    destination_file = "ansible-microk8s.yml"
    shutil.copy(source_file, destination_file)

    with open(destination_file, 'r') as file:
          file_data = file.read()

    file_data  = re.sub('USER_TMP', user, file_data)

    with open(destination_file, 'w') as file:
        file.write(file_data)


if __name__ == '__main__':
    generate_ansible_configuration()

