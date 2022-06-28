#!/bin/sh
for f in `lxc list -f csv -c n`; do printf "$f :\t" ; lxc exec $f -- sh -c "cat /etc/os-release | grep PRETTY_NAME" | awk -F= '{print $2}' ; done