#!/bin/python3
import os
import re
import ipdb

def write_hosts():
    # Read the contents of the hosts.seed file
    with open(os.path.expandvars("hosts.seed"), "r") as f:
        hosts_seed = f.read()

    # Write the contents of the hosts.seed file to /etc/hosts
    with open("/etc/hosts", "w") as f:
        f.write(hosts_seed)

    # Get the output of the lxc list command
    lxc_output = os.popen("lxc list -f compact -c 4,n").read()

    # Split the output into lines and remove the first line
    lxc_output_lines = lxc_output.split("\n")[1:]
    # ipdb.set_trace()
    lxc_output_lines = list(filter(None,lxc_output_lines))

    # Append the remaining lines to /etc/hosts
    pattern = "lab"
    with open("/etc/hosts", "a") as f:
        for line in lxc_output_lines:
            # ipdb.set_trace()
            if re.search(pattern, line):
                print(f"{line.split()[0]} {line.split()[2]} {line.split()[2]}")
                f.write(f"{line.split()[0]} {line.split()[2]} {line.split()[2]}\n")


if __name__ == '__main__':
    write_hosts()

