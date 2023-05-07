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
    lxc_init = f"lxc init {image} {instance}-lxc-container"
    cmd.call(lxc_init.split(), shell=False)


def configure_instance(instance, cpu, ram):
    format_text.print_blue(f"Reconfiguring {instance} - CPU : {cpu }, RAM : {ram}")
    stop_instance = f"lxc stop {instance}-lxc-container"
    cpucfg = f"lxc config set {instance}-lxc-container limits.cpu {cpu}"
    ramcfg = f"lxc config set {instance}-lxc-container limits.memory {ram}"
    lxc_start = f"lxc start {instance}-lxc-container"
    cmd.call(stop_instance.split(), shell=False, stderr=subprocess.DEVNULL)
    for command in [cpucfg, ramcfg, lxc_start]:
        cmd.call(command.split(), shell=False)
        time.sleep(10)


def main():
    cmd.call("clear", shell=False)
    format_text.print_green("Loading Stack Configuraton from toml file")
    linux_stack = read_stack()
    format_text.print_yellow("Will save configuration into json")
    with open('file.json', 'w') as json_export:
        json.dump(linux_stack, json_export)
    format_text.print_green("Configuring Linux LXC VM Server Stack from toml file")
    format_text.print_green("If any existing instances exist they will be shutdown and reconfigured")
    for instance in linux_stack:
        if(check_instance_exists(instance)):
            print(f"{instance} already exists")
        else:
            create_instance(instance, linux_stack[instance]['image'])
        configure_instance(instance, linux_stack[instance]['cpu'], linux_stack[instance]['ram'])
    format_text.print_smiley("Lab has been setup, will display it shortly")
    time.sleep(15)
    lab_status.display()


if __name__ == '__main__':
    main()
