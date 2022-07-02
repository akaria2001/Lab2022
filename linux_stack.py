#!/bin/python3
import json
import toml
import subprocess as cmd
import format_text


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
    format_text.print_green("Printing Stack Information")
    format_text.print_yellow(f"Stack Name : {linux_stack['Stack']}")
    for instance, config in linux_stack.items():
        if type(config) is dict:
            print(f"\n{instance}")
            for instance_nest, config_nest in config.items():
                format_text.print_blue(f"{instance_nest} -> {config_nest}")


if __name__ == '__main__':
    main()
