!/bin/bash
# This script sets up a Python virtual environment and installs necessary packages.
sudo apt install python3-pip and python3-virtualenv -y
cd $HOME/bin
virtualenv .
source bin/activate
pip3 install toml psutil flask ipdb