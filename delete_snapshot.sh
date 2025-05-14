#!/bin/bash

# Replace <container-name> with the name of your container
container_name=$1

printf "Deleting snapshots for $1\n"

# List all snapshots and delete them
for snapshot in $(lxc info $container_name | grep -E 'container-backup|vm-backup' | awk -F\| '{ print $2 }' | sed s/' '//g) ; do
    echo "Deleting snapshot: $snapshot"
    lxc delete $container_name/$snapshot
done

echo "All snapshots deleted for container: $container_name"
