#!/bin/python3
import subprocess as cmd
import print_colours


def lab_status():
    cmd.call("clear", shell=False)
    print_colours.print_yellow("Current Lab Status")
    cmd.call(["lxc", "list"], shell=False)
