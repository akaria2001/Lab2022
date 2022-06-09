#!/bin/python3
import subprocess as cmd
import coloured_text


def display():
    cmd.call("clear", shell=False)
    coloured_text.print_yellow("Current Lab Status")
    cmd.call(["lxc", "list"], shell=False)
