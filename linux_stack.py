#!/bin/python3
import json
import toml
import subprocess as cmd
import format_text
import time
import tear_down_lab


def read_stack():
    process_dict = toml.load("file.toml")
    return process_dict


def main():
    cmd.call("clear", shell=False)
    format_text.print_green("Loading Stack Configuraton from toml file")
    linux_stack = read_stack()
    format_text.print_yellow("Will save configuration into json")
    with open('file.json', 'w') as json_export:
        json.dump(linux_stack, json_export)
    tear_down_lab.destroy()
    format_text.print_green("Creating Linux QEMU VM Server Stack")
    for instance in linux_stack:
        format_text.print_blue(f"{instance} : {linux_stack[instance]}")
        lxc_init = f"lxc init {linux_stack[instance]['image']} {instance} --vm"
        format_text.print_green(lxc_init)
        cpucfg = f"lxc config set {instance} limits.cpu 4"
        format_text.print_blue(cpucfg)
        ramcfg = f"lxc config set {instance} limits.memory 4GB"
        format_text.print_green(ramcfg)
        lxc_start = f"lxc start {instance}"
        format_text.print_blue(lxc_start)
        for command in [lxc_init, cpucfg, ramcfg, lxc_start]:
            cmd.call(command.split(), shell=False)
        time.sleep(10)


if __name__ == '__main__':
    main()
