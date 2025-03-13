#!/bin/sh

for instance in $(lxc ls -c n -f csv) ; do lxc stop $instance ; done
