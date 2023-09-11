#!/bin/sh
# Refer to https://cloudinit.readthedocs.io/en/latest/tutorial/lxd.html

lxc launch ubuntu:jammy my-test -p lab --config=user.user-data="$(cat user-data)"
