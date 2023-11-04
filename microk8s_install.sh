#!/bin
sudo snap install microk8s --classic --channel=1.28
sleep 5
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
microk8s status --wait-ready
microk8s kubectl get nodes
microk8s kubectl get services
