#!/bin/sh
for f in $(cat file.toml | grep -i image | awk -F\" '{print $2}') ; do lxc launch $f ; done