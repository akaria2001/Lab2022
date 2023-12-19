#### Lab2022
Amit Karia Lab 2022

### Setup Lab (To help automate this, working on setup_host.sh which is currently a work in progress)

To setup a Multi Node MicroK8s Cluster on an Ubuntu 22.04 Desktop Physical Installation (also works inside an Ubuntu 22.04 VM)

**Open a terminal**

`sudo apt install git`

`cd $HOME`

`git clone https://github.com/akaria2001/Lab2022.git bin`

`cd bin`

`bash setup_host.sh`

`ssh-keygen -t rsa`

Enter the default options

Copy the contents off `$HOME/.ssh/id_rsa.pub` to the `cloud-init-test.yaml` file at line 15

`cd $HOME/bin`

`source/bin/activate`

`time python3 k8_cluster.py`

The last script will create the nodes as defined in `kubernetes_vms.toml`, by default it will create them as LXC system containers, but you can change the type value to `VM` to use QEMU KVM VMs instead

It used cloud-init to bootstrap the nodes and then ansible for installing MicroK8s

----------

## Manual Steps

On New Ubuntu 22.04 Desktop Install

**Open a terminal**

Install git

`sudo apt install git`

Install LXD

`sudo snap install lxd`
`lxd init` - default except ipv6

`lxc profile create microk8s`

`wget https://raw.githubusercontent.com/ubuntu/microk8s/master/tests/lxc/microk8s.profile -O microk8s.profile`

`cat microk8s.profile | lxc profile edit microk8s`

Install Python Packages

`sudo apt install python3-pip and python3-virtualenv -y`

Download Git Repo -

`cd $HOME`

`git clone https://github.com/akaria2001/Lab2022.git bin`

`cd bin`

Setup virtualenv and enable it

`virtualenv .`
`source bin/activate`

Python Modules in virtual env

flask
psutil
toml

`pip3 install flask psutil toml`

Open up a 2nd terminal and navigate to $HOME/bin

`cd $HOME/bin`

activate the virtual env in the 2nd terminal

`source bin/activate`

In first terminal launch the Flask Web App

`python3 frontend.py`

Connect to interface via your web browser (http://<ipaddress>:35000)

Go back to first terminal and run the script to create the Linux Instances

time python3 linux_stack.py
