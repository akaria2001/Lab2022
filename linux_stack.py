#!/bin/python3
from asyncio import subprocess
import json
import toml
import subprocess as cmd
import format_text
import time
import lab_status
import os.path


def read_stack():
    process_dict = toml.load("file.toml")
    return process_dict


def check_instance_exists(instance):
    print(f"Will check {instance} exists")
    check_cmd = f"lxc info {instance}"
    try:
        cmd.check_output(check_cmd.split(), shell=False, stderr=subprocess.DEVNULL)
        return True
    except subprocess.subprocess.CalledProcessError:
        return False


def create_instance(instance, image, secureboot, type, cpu, ram, tag):
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
            lxc_init = f"lxc launch {image} {instance}-{type} --vm -c security.secureboot={securebootflag} -c limits.cpu={cpu} -c limits.memory={ram} -c user.comment={protected}"
            format_text.print_blue(f"Running command : {lxc_init}")
            cmd.call(lxc_init.split(), shell=False)
        else:
            format_text.print_red("KVM is not supported on host will not create QEMU VM")
    else:
        lxc_init = f"lxc launch {image} {instance}-{type} -c limits.cpu={cpu} -c limits.memory={ram} -c user.comment={protected}"
        format_text.print_blue(f"Running command : {lxc_init}")
        cmd.call(lxc_init.split(), shell=False)
    time.sleep(3)


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
    format_text.print_green("Configuring Linux QEMU VM Server Stack from toml file")
    format_text.print_green("If any existing instances exist they will be shutdown and reconfigured")
    for instance in linux_stack:
        if(check_instance_exists(instance)):
            print(f"{instance} already exists")
        else:
            create_instance(instance, linux_stack[instance]['image'], linux_stack[instance]['secureboot'], linux_stack[instance]['type'], linux_stack[instance]['cpu'], linux_stack[instance]['ram'], linux_stack[instance]['protected'])
            time.sleep(10)
        if(check_instance_health(instance, linux_stack[instance]['type'])):
            format_text.print_green(f"Instance {instance} is healthy")
        else:
            format_text.print_red(f"Instance {instance}-{linux_stack[instance]['type']} is not healthy")
            unhealthy_instances.append(f"{instance}-{instance}-{linux_stack[instance]['type']}")
            del_instance_cmd = f"lxc delete --force {instance}-{instance}-{linux_stack[instance]['type']}"
            cmd.call(del_instance_cmd.split(), shell=False)

    format_text.print_smiley("Lab has been setup, will display it shortly")
    time.sleep(15)
    lab_status.display()
    unhealthy_instance_qty = len(unhealthy_instances)
    format_text.print_green(f"Qty of unhealthy instances : {unhealthy_instance_qty}")
    if unhealthy_instance_qty > 0:
        format_text.print_red("Following Instances were found to be unhealthy and were removed")
        for unhealthy_instance in unhealthy_instances:
            format_text.print_red(unhealthy_instance)



if __name__ == '__main__':
    main()
