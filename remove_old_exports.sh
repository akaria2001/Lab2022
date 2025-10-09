#!/bin/bash
# This script removes directories named "lxc-exports*" that are older than 7 days
find . -maxdepth 1 -type d -name "lxc-exports*" -mtime +4 -exec rm -rfv {} +
