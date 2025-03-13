#!/bin/sh
bash snapshot_lab.sh
ansible-playbook update_os_proxmox_lab.yml -i ansible-lab
bash snapshot_lab.sh
