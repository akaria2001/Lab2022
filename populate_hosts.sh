#!/bin/sh
sudo cat $HOME/bin/hosts.seed | sudo tee /etc/hosts
sudo lxc list -f compact -c 4,4,n | tail -n +2 2>&1 | sudo tee -a /etc/hosts