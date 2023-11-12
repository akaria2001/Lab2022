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
import populate_hosts

def read_stack():
    process_dict = toml.load("kubernetes_vms.toml")
    return process_dict


def read_user_data():
    # Read the user-data file
    with open('cloud-init-test.yaml', 'r') as file:
        user_data = file.read()
        return user_data


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
        lxc_init = f"lxc init {image} {instance}-{type}"
        format_text.print_blue(f"Running command : {lxc_init}")
        cmd.call(lxc_init.split(), shell=False)
    time.sleep(15)


# def configure_instance(instance, cpu, ram, tag, type):
#     check_instance_created = f"lxc info {instance}-{type}"
#     try:
#         cmd.check_output(check_instance_created.split(), shell=False)
#         format_text.print_blue(f"Reconfiguring {instance}-{type} - CPU : {cpu}, RAM : {ram}, Type : {type}")
#         stop_instance = f"lxc stop {instance}-{type}"
#         cpucfg = f"lxc config set {instance}-{type} limits.cpu {cpu}"
#         ramcfg = f"lxc config set {instance}-{type} limits.memory {ram}"
#         if(tag == 0):
#             protected = "no"
#         else:
#             protected = "yes"
#         tagcfg = f"lxc config set {instance}-{type} user.comment={protected}"
#         lxc_start = f"lxc start {instance}-{type}"
#         try:
#             cmd.call(stop_instance.split(), shell=False, stderr=subprocess.DEVNULL, timeout=5)
#         except subprocess.subprocess.TimeoutExpired:
#             format_text.print_red(f"Timed out trying to shutdown {instance}-{type} to be reconfigured")
#         for command in [cpucfg, ramcfg, tagcfg, lxc_start]:
#             cmd.call(command.split(), shell=False)
#             time.sleep(3.5)
#     except:
#         format_text.print_red(f"Instance {instance}-{type} doesn't exist will skip configuration")


def check_instance_health(instance, type):
    format_text.print_blue(f"Checking Instance health : {instance}")
    check_cmd = f"lxc exec {instance}-{type} -- ps aux"
    format_text.print_blue(f"Running Check : {check_cmd}")
    try:
        cmd.check_output(check_cmd.split(), shell=False, stderr=subprocess.DEVNULL)
        return True
    except subprocess.subprocess.CalledProcessError:
        return False


def main():
    unhealthy_instances = []
    cmd.call("clear", shell=False)
    format_text.print_green("Loading Stack Configuraton from toml file")
    linux_stack = read_stack()
    format_text.print_yellow("Will save configuration into json")
    with open('file.json', 'w') as json_export:
        json.dump(linux_stack, json_export)
    format_text.print_green("Configuring K8 QEMU VM Cluster Stack from toml file")
    format_text.print_green("If any existing instances exist they will be shutdown and reconfigured")
    for instance in linux_stack:
        if(check_instance_exists(instance)):
            print(f"{instance} already exists")
        else:
            create_instance(instance, linux_stack[instance]['image'], linux_stack[instance]['secureboot'], linux_stack[instance]['type'], linux_stack[instance]['cpu'], linux_stack[instance]['ram'], linux_stack[instance]['protected'])
            time.sleep(15)
        if(check_instance_health(instance, linux_stack[instance]['type'])):
            format_text.print_green(f"Instance {instance} is healthy will install MicroK8s via Ansible")
            time.sleep(60)
            # Short term work around to run this until I can cloud-init working to do this instead
            # script_push = f"lxc file push microk8s_install.sh {instance}-{linux_stack[instance]['type']}/tmp/"
            # time.sleep(15)
            # format_text.print_green(f"Instance {instance}-{linux_stack[instance]['type']} - running - {script_push}")
            # cmd.call(script_push.split(), shell=False)
            # time.sleep(15)
            # install_microk8s = f"lxc exec {instance}-{linux_stack[instance]['type']} -- bash /tmp/microk8s_install.sh"
            # format_text.print_green(f"Instance {instance} - running - {install_microk8s}")
            # cmd.call(install_microk8s.split(), shell=False)
        else:
            format_text.print_red(f"Instance {instance}-{linux_stack[instance]['type']} is not healthy")
            unhealthy_instances.append(f"{instance}-{instance}-{linux_stack[instance]['type']}")
            del_instance_cmd = f"lxc delete --force {instance}-{instance}-{linux_stack[instance]['type']}"
            cmd.call(del_instance_cmd.split(), shell=False)

    format_text.print_smiley("Lab has been setup, will display it shortly")
    time.sleep(15)
    populate_hosts.write_hosts()
    lab_status.display()
    unhealthy_instance_qty = len(unhealthy_instances)
    format_text.print_green(f"Qty of unhealthy instances : {unhealthy_instance_qty}")
    if unhealthy_instance_qty > 0:
        format_text.print_red("Following Instances were found to be unhealthy and were removed")
        for unhealthy_instance in unhealthy_instances:
            format_text.print_red(unhealthy_instance)



if __name__ == '__main__':
    main()
