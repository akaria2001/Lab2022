#/bin/sh
cd $HOME/bin
sudo ls
pwd
time python3.10 linux_stack.py
for instance in $(lxc list -c n -f compact | tail -n +2) ; do lxc file push $HOME/bin/readme.lxc.md $instance/tmp/ ; done
sudo bash populate_hosts.sh
