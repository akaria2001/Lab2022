#!/bin/sh

TIMESTAMP=`date "+%Y-%m-%d-%H:%M:%S"`

for instance in $(lxc ls -c n -f csv) ; do lxc snapshot $instance $instance-backup-$TIMESTAMP ; done
