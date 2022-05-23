#!/bin/sh
clear
lxc list

for number in `seq 1 3` ;
    do
        lxc launch ubuntu:22.04 ubuntu-vm-$number --vm
        sleep 1
        lxc launch ubuntu:22.04 ubuntu-container-$number
        sleep 1
    done
sleep 10
lxc list