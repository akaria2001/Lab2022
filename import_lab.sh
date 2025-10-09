#!/bin
for instance in $(ls lab*exported.tgz) ; do printf "$instance\n" ; lxc import $instance ; sleep 60 ; done 