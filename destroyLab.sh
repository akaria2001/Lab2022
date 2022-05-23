#!/bin/sh
clear
printf "Checking current lab\n\n"
lxc list
LAB=`lxc list | grep -E 'vm|container|machine' | awk '{print $2}'`
printf "Will now destroy these to clean up the environment\n\n"
for machine in $LAB ;
    do
    printf "destroying $machine\n\n"
    lxc delete -f $machine
    done
printf "Lab is now empty, printing the current status\n\n"
lxc list