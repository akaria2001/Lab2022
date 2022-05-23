#!/bin/sh
clear
printf "Checking current lab\n\n"
lxc list
printf "Lab is empty good\n\n"

printf "Creating Sample Lab\n\n"

for number in `seq 1 2` ;
    do
        printf "Creating QEMU Virtual Machines\n\n"
        lxc launch ubuntu:22.04 ubuntu-vm-$number --vm
        sleep 1
        printf "Creating LXC Containers\n\n"
        lxc launch ubuntu:22.04 ubuntu-container-$number
        sleep 1
    done
sleep 10
printf "\nSample lab is now created, printing the current status\n\n"
lxc list