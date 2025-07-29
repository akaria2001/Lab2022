#!/bin/sh

# Create timestamp and folder
TIMESTAMP=$(date "+%Y-%m-%d-%H-%M-%S")
EXPORT_DIR="lxc-exports-$TIMESTAMP"
mkdir -p "$EXPORT_DIR"

# Loop through LXC containers and export each to the new folder
for instance in $(lxc ls -c n -f csv); do
    EXPORT_FILE="${EXPORT_DIR}/${instance}-${TIMESTAMP}-exported.tgz"
    lxc export "$instance" "$EXPORT_FILE"
    echo "Exported $instance to $EXPORT_FILE"
done

