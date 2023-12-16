#!/bin/sh

sudo snap install neofetch ansible glances emacs-nox
sudo snap install lxd
lxd init
sudo apt install python3-pip and python3-virtualenv -y
cd $HOME/bin
virtualenv .
source bin/activate
pip3 install toml psutil flask
sudo addgroup editors
sudo adduser $USER
sudo chown :editors /etc/hosts
sudo chmod 664 /etc/hosts
sudo setfacl -m $USER:rw /etc/hosts
