#!/bin/sh

cd $HOME
sudo apt-get update -y
sudo snap remove lxd --purge
sudo apt-get install openssh-server -y
sudo apt-get install neofetch ansible glances vim emacs-nox acl -y
ansible-galaxy collection install ansible.posix
sudo snap install lxd
sudo snap install helm --classic
cat $HOME/bin/lxd_preseed.yaml | lxd init --preseed
wget https://raw.githubusercontent.com/ubuntu/microk8s/master/tests/lxc/microk8s.profile -O $HOME/bin/microk8s.profile
lxc profile create microk8s
cat $HOME/bin/microk8s.profile | lxc profile edit microk8s
sudo apt install python3-pip and python3-virtualenv -y
cd $HOME/bin
virtualenv .
source bin/activate
pip3 install toml psutil flask ipdb
cat /etc/hosts > $HOME/bin/hosts.seed
sudo addgroup editors
sudo usermod -a -G lxd $USER
sudo adduser $USER editors
sudo chown :editors /etc/hosts
sudo chmod 664 /etc/hosts
sudo setfacl -m $USER:rw /etc/hosts
printf "You can now create your MicroK8s cluster by running the following\n\n"
printf "ssh-keygen -b 256 -t ecdsa\n"
printf "Enter the default options\n"
printf "Copy the contens off $HOME/.ssh/id_ecdsa.pub to the cloud-init-test.yaml file line 15\n"
printf "\n"
printf "cd $HOME/bin\n"
printf "source/bin/activate\n"
printf "time python3 k8_cluster.py\n"
