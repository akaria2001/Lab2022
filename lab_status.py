#!/bin/python3
import subprocess as cmd
import format_text


def display():
    cmd.call("clear", shell=False)
    format_text.print_yellow("Current Lab Status")
    cmd.call(["lxc", "list"], shell=False)
