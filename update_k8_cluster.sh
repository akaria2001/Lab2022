#!/bin/sh
bash snapshot_lab.sh
ansible-playbook update_k8_cluster.yml -i ansible-hosts
bash snapshot_lab.sh
