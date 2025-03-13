#!/bin/sh

TIMESTAMP=`date "+%Y-%m-%d-%H:%M:%S"`

for instance in $(lxc ls -c n -f csv) ; do lxc export $instance $instance-$TIMESTAMP-exported.tgz ; done
