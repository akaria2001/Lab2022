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
printf "Setting up SSH Keys\n\n"
cd $HOME
rm -rfv $HOME/.ssh/id_ecdsa*
ssh-keygen -b 256 -t ecdsa -q -f $HOME/.ssh/id_ecdsa -N ""
KEY=$(cat $HOME/.ssh/id_ecdsa.pub)
sleep 2
cp -rfv $HOME/bin/cloud-init-test.yaml.template $HOME/bin/cloud-init-test.yaml
sed -i "s|TMPKEY|$KEY|g" $HOME/bin/cloud-init-test.yaml
cat $HOME/.ssh/id_ecdsa.pub
grep -i ecdsa $HOME/bin/cloud-init-test.yaml
for c in $(lxc ls -c n -f csv) ; do lxc file push ~/.ssh/id_ecdsa.pub $c/home/$USERNAME/.ssh/authorized_keys; done
for f in $(lxc ls -c n -f csv ) ; do ssh $f -- hostname ; cat /etc/os-release ; printf "\n" ; done
cd $HOME/bin
source /bin/activate
