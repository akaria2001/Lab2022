#!/bin/python3
import subprocess as cmd
import coloured_text


def check_lxd_installed():
    status = ""
    try:
        cmd.run('lxd', shell=False)
    except FileNotFoundError:
        status = False
    return status

def main():
    coloured_text.print_green("Checking if LXD Installed")
    if (check_lxd_installed()):
        print("LXD Installed")
    else:
        print("LXD Not Installed")


if __name__ == '__main__':
    main()