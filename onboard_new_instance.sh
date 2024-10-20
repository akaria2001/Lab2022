#!/bin/sh
ansible-playbook ansible-lab.yml -K -i ansible-proxmox32  -l new
ansible-playbook ansible-patch-glibc.yml -K -i ansible-proxmox32  -l new
ansible-playbook dns_configure_proxmox_lab.yml -K -i ansible-proxmox32  -l new
ansible-playbook update_os_proxmox_lab.yml -K -i ansible-proxmox32  -l new