#!/bin/python3
from asyncio import subprocess
import json
import toml
import subprocess as cmd
import format_text
import time
import lab_status
import os.path
import os
import populate_hosts_lab
import create_ansible_lab_configuration as ansible_gen


def read_stack():
    process_dict = toml.load("rocky-test-lab.toml")
    return process_dict


def read_user_data():
    # Read the user-data file
    with open('cloud-init-test.yaml', 'r') as file:
        user_data = file.read()
        return user_data

def get_user():
    return os.environ.get('USER')


def check_instance_exists(instance):
    print(f"Will check {instance} exists")
    check_cmd = f"lxc info {instance}"
    try:
        cmd.check_output(check_cmd.split(), shell=False, stderr=subprocess.DEVNULL)
        return True
    except subprocess.subprocess.CalledProcessError:
        return False


def create_instance(instance, image, secureboot, type, cpu, ram, tag):
    user_data = read_user_data()
    if(secureboot == 0):
        securebootflag = "false"
    else:
        securebootflag = "true"
    if(tag == 0):
        protected = "no"
    else:
        protected = "yes"
    format_text.print_blue(f"Creating instance {instance}-{type} using image: {image} -> type {type}")
    if(check_instance_health(instance, type)):
        return "Instance already exists will carry on"
    else:
        if(type == "vm"):
            format_text.print_green("Checking if host is KVM")
            path = '/dev/kvm'
            if(os.path.exists(path)):
                format_text.print_blue("KVM is supported on host will create QEMU VM")
                lxc_init = f'lxc launch {image} {instance}-{type} --vm -c security.secureboot={securebootflag} -c limits.cpu={cpu} -c limits.memory={ram} -c user.comment={protected} -c user.user-data="{user_data}"'
                format_text.print_blue(f"Running command : {lxc_init}")
                # Work around as subprocess not playing nice with my lxc_init command when using user-data flag, commenting out the cmd.call to use os.system, will look for better solution in future.
                os.system(lxc_init)
                # cmd.call(lxc_init.split(), shell=False)
            else:
                format_text.print_red("KVM is not supported on host will not create QEMU VM")
        else:
            lxc_init = f'lxc launch -p default -p microk8s {image} {instance}-{type} -c limits.cpu={cpu} -c limits.memory={ram} -c user.comment={protected} -c user.user-data="{user_data}"'
            format_text.print_blue(f"Running command : {lxc_init}")
            # Work around as subprocess not playing nice with my lxc_init command when using user-data flag, commenting out the cmd.call to use os.system, will look for better solution in future.
            os.system(lxc_init)
            # cmd.call(lxc_init.split(), shell=False)


def check_instance_health(instance, type):
    format_text.print_blue(f"Checking Instance health : {instance}")
    check_cmd = f"lxc exec {instance}-{type} -- ps aux"
    format_text.print_blue(f"Running Check : {check_cmd}")
    try:
        cmd.check_output(check_cmd.split(), shell=False, stderr=subprocess.DEVNULL)
        for count in range(120, -1, -1):
            cmd.call("clear", shell=False)
            format_text.print_smiley(f"{instance}-{type} is healthy, will wait 120 seconds before proceeding")
            format_text.print_smiley(f"Countdown before proceeding: {count} seconds!!")
            time.sleep(1)
        return True
    except subprocess.subprocess.CalledProcessError:
        return False


def main():
    cmd.call('clear', shell=False)
    format_text.print_smiley(f"Welcome {get_user()} to the Rocky Lab creation tool")
    time.sleep(2)
    unhealthy_instances = []
    cmd.call("clear", shell=False)
    format_text.print_green("Loading Stack Configuraton from toml file")
    linux_stack = read_stack()
    format_text.print_yellow("Will save configuration into json")
    with open('file.json', 'w') as json_export:
        json.dump(linux_stack, json_export)
    format_text.print_green("Configuring QEMU VM Cluster Stack from toml file")
    format_text.print_green("If any existing instances exist they will be shutdown and reconfigured")
    for instance in linux_stack:
        if(check_instance_exists(instance)):
            print(f"{instance} already exists")
        else:
            create_instance(instance, linux_stack[instance]['image'], linux_stack[instance]['secureboot'], linux_stack[instance]['type'], linux_stack[instance]['cpu'], linux_stack[instance]['ram'], linux_stack[instance]['protected'])
            time.sleep(15)
        if(check_instance_health(instance, linux_stack[instance]['type'])):
            time.sleep(60)
        else:
            format_text.print_red(f"Instance {instance}-{linux_stack[instance]['type']} is not healthy")
            unhealthy_instances.append(f"{instance}-{instance}-{linux_stack[instance]['type']}")
            del_instance_cmd = f"lxc delete --force {instance}-{instance}-{linux_stack[instance]['type']}"
            cmd.call(del_instance_cmd.split(), shell=False)

    format_text.print_smiley("Lab has been setup, will display it shortly")
    time.sleep(15)
    populate_hosts_lab.write_hosts()
    with open(f'/home/{get_user()}/.ssh/known_hosts', 'w') as file:
        pass
    with open('ansible-hosts', 'w') as ansible_file:
        pass
    lab_status.display()
    for instance in linux_stack:
        format_text.print_green(f"Instance {instance}-{linux_stack[instance]['type']} setup SSH trust")
        setup_trust = f"ssh-copy-id -f -o StrictHostKeyChecking=accept-new {get_user()}@{instance}-{linux_stack[instance]['type']}"
        print(f"Running command - {setup_trust}")
        cmd.call(setup_trust.split(), shell=False)
        test_trust = f"ssh -o StrictHostKeyChecking=accept-new {get_user()}@{instance}-{linux_stack[instance]['type']} -- hostname"
        print(f"Running command - {test_trust}")
        cmd.call(test_trust.split(), shell=False)
        ansible_gen.generate_ansible_configuration()
        time.sleep(15)

    # format_text.print_green(f"Using Ansible to istall MicroK8s on the new VMs")
    # ansible_cmd = "ansible-playbook ansible-microk8s.yml -i ansible-hosts"
    # format_text.print_smiley(f"Running command {ansible_cmd}")
    # cmd.call(ansible_cmd.split(), shell=False)

    format_text.print_smiley(f"Running Ansible playbook to setup Lab Instances")
    time.sleep(5)
    ansible_cmd = "ansible-playbook ansible-lab.yml -i ansible-lab"
    cmd.call(ansible_cmd.split(), shell=False)

    format_text.print_smiley(f"Running Ansible playbook to setup NRPE Polling on Lab Instances")
    time.sleep(5)
    ansible_cmd = "ansible-playbook nrpe_client_polling.yml -i ansible-lab"
    cmd.call(ansible_cmd.split(), shell=False)

    unhealthy_instance_qty = len(unhealthy_instances)
    format_text.print_green(f"Qty of unhealthy instances : {unhealthy_instance_qty}")
    if unhealthy_instance_qty > 0:
        format_text.print_red("Following Instances were found to be unhealthy and were removed")
        for unhealthy_instance in unhealthy_instances:
            format_text.print_red(unhealthy_instance)



if __name__ == '__main__':
    main()
