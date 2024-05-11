#!/bin/sh
lxc launch images:ubuntu/22.04/desktop protected-ubuntu-desktop22 -c limits.cpu=4 -c limits.memory=8GiB -c boot.autostart=true --vm --console=vga
