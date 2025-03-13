#/bin/sh
clear
cd $HOME/bin
sudo ls
pwd
lxc ls
sleep 2
time python3 tear_down_lab.py
time python3.12 rocky-lab.py
bash snapshot.sh
ansible-playbook update_os_proxmox_lab.yml -i ansible-lab
bash /home/ubuntu/bin/snapshot_lab.sh
lxc ls
for f in $(lxc ls -c n -f csv); do lxc info $f ; done
