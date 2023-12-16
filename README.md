# Lab2022
Amit Karia Lab 2022

Setup Lab (To help automate this, working on setup_host.sh which is currently a work in progress)

On New Ubuntu 22.04 Desktop Install

Open a terminal

Install git

sudo apt install git

Install LXD

sudo snap install lxd
lxd init - default except ipv6

lxc profile create microk8s

wget https://raw.githubusercontent.com/ubuntu/microk8s/master/tests/lxc/microk8s.profile -O microk8s.profile

cat microk8s.profile | lxc profile edit microk8s

Install Python Packages

sudo apt install python3-pip and python3-virtualenv -y

Download Git Repo -

cd $HOME

git clone https://github.com/akaria2001/Lab2022.git bin

cd bin

Setup virtualenv and enable it

virtualenv .
source bin/activate

Python Modules in virtual env

flask
psutil
toml

pip3 install flask psutil toml

Open up a 2nd terminal and navigate to $HOME/bin

cd $HOME/bin

activate the virtual env in the 2nd terminal

source bin/activate

In first terminal launch the Flask Web App

python3 frontend.py

Connect to interface via your web browser (http://<ipaddress>:25000)

Go back to first terminal and run the script to create the Linux Instances

time python3 linux_stack.py
