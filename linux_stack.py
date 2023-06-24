#!/bin/python3
from asyncio import subprocess
import json
import toml
import subprocess as cmd
import format_text
import time
import lab_status


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


def create_instance(instance, image):
    format_text.print_blue(f"Creating instance {instance} using image: {image}")
    lxc_init = f"lxc init {image} {instance}-qemu-vm --vm"
    cmd.call(lxc_init.split(), shell=False)
    time.sleep(3)


def configure_instance(instance, cpu, ram):
    format_text.print_blue(f"Reconfiguring {instance} - CPU : {cpu }, RAM : {ram}")
    stop_instance = f"lxc stop {instance}-qemu-vm"
    cpucfg = f"lxc config set {instance}-qemu-vm limits.cpu {cpu}"
    ramcfg = f"lxc config set {instance}-qemu-vm limits.memory {ram}"
    lxc_start = f"lxc start {instance}-qemu-vm"
    try:
        cmd.call(stop_instance.split(), shell=False, stderr=subprocess.DEVNULL, timeout=5)
    except subprocess.subprocess.TimeoutExpired:
        format_text.print_red(f"Timed out trying to shutdown {instance}-qemu-vm to be reconfigured")
    for command in [cpucfg, ramcfg, lxc_start]:
        cmd.call(command.split(), shell=False)
        time.sleep(10)


def check_instance_health(instance):
    format_text.print_blue(f"Checking Instance health : {instance}")
    check_cmd = f"lxc exec {instance}-qemu-vm -- ps aux"
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
            create_instance(instance, linux_stack[instance]['image'])
            configure_instance(instance, linux_stack[instance]['cpu'], linux_stack[instance]['ram'])
            time.sleep(15)
        if(check_instance_health(instance)):
            format_text.print_green(f"Instance {instance} is healthy")
        else:
            format_text.print_red(f"Instance {instance}-qemu-vm is not healthy")
            unhealthy_instances.append(f"{instance}-qemu-vm")
            del_instance_cmd = f"lxc delete --force {instance}-qemu-vm"
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
