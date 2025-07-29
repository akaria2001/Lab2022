#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime

# Create timestamp and folder
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
export_dir = f"lxc-exports-{timestamp}"
os.makedirs(export_dir, exist_ok=True)

# Get list of LXC container names
try:
    result = subprocess.run(
        ["lxc", "ls", "-c", "n", "-f", "csv"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    containers = result.stdout.strip().splitlines()
except subprocess.CalledProcessError as e:
    print("Error listing containers:", e.stderr)
    exit(1)

# Export each container
for container in containers:
    export_file = os.path.join(export_dir, f"{container}-{timestamp}-exported.tgz")
    print(f"Exporting {container} to {export_file}...")
    try:
        subprocess.run(
            ["lxc", "export", container, export_file],
            check=True
        )
        print(f"Exported {container} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to export {container}: {e.stderr}")
