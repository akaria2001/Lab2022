import os
import shutil
import subprocess
import time
from pathlib import Path

def regen_creds():
    HOME = Path.home()
    SSH_DIR = HOME / ".ssh"
    KEY_FILE = SSH_DIR / "id_ecdsa"
    PUB_KEY_FILE = SSH_DIR / "id_ecdsa.pub"
    TEMPLATE = HOME / "bin/cloud-init-test.yaml.template"
    YAML_FILE = HOME / "bin/cloud-init-test.yaml"

    # Remove old keys
    for f in SSH_DIR.glob("id_ecdsa*"):
        print(f"Removing {f}")
        f.unlink()

    # Generate new key
    subprocess.run([
        "ssh-keygen", "-b", "256", "-t", "ecdsa", "-q",
        "-f", str(KEY_FILE), "-N", ""
    ], check=True)

    # Read public key
    with PUB_KEY_FILE.open() as f:
        key = f.read().strip()

    time.sleep(2)

    # Copy template to yaml
    shutil.copy2(TEMPLATE, YAML_FILE)
    print(f"Copied {TEMPLATE} to {YAML_FILE}")

    # Replace TMPKEY with actual key
    with YAML_FILE.open() as f:
        content = f.read()
    content = content.replace("TMPKEY", key)
    with YAML_FILE.open("w") as f:
        f.write(content)
    print("Replaced TMPKEY in yaml file.")

    # Show public key
    print(key)

    # Grep for ecdsa in yaml file
    with YAML_FILE.open() as f:
        for line in f:
            if "ecdsa" in line.lower():
                print(line, end="")

    # Get LXC container names
    result = subprocess.run(
        ["lxc", "ls", "-c", "n", "-f", "csv"],
        capture_output=True, text=True, check=True
    )
    containers = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # Push public key to containers
    for c in containers:
        print(f"Pushing key to {c}")
        subprocess.run([
            "lxc", "file", "push", str(PUB_KEY_FILE),
            f"{c}/home/ubuntu/.ssh/authorized_keys"
        ], check=True)

    # SSH into containers and print hostname and os-release
    for c in containers:
        print(f"Connecting to {c}")
        try:
            subprocess.run([
                "ssh", c, "--", "hostname"
            ], check=True)
            subprocess.run([
                "ssh", c, "--", "cat /etc/os-release"
            ], check=True)
            print()
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to {c}: {e}")


if __name__ == "__main__":
    regen_creds()