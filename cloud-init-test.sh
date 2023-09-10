#!/bin/sh
# Refer to https://cloudinit.readthedocs.io/en/latest/tutorial/lxd.html

lxc launch ubuntu:jammy my-test --config=user.user-data="$(cat user-data)"
