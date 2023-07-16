#!/bin/sh
for f in $(cat file.toml | grep -i image | awk -F\" '{print $2}') ; do lxc launch $f ; sleep 5 ; done
for f in `lxc list -c n -f compact | tail -n +2` ; do lxc file push $HOME/bin/readme.lxc.md $f/tmp/ ; done
sleep 10
$HOME/bin/populate_hosts.sh
