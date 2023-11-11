#!/bin
# Get the hostname
HOSTNAME=$(hostname)
printf "Installing MicroK8s on $HOSTNAME"
sudo snap install microk8s --classic --channel=1.28
sleep 5
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
microk8s status --wait-ready
microk8s kubectl get nodes
if [[ $HOSTNAME == *"master"* ]]; then
  # If it does, run your logic here
    printf "Configuring MicroK8s on Controller Node $HOSTNAME"
    microk8s enable observability
    microk8s enable dns
    # Enable MetalLB
    # microk8s enable metallb
    # # Provide an IP address range for MetalLB
    # microk8s kubectl apply <<EOF
    # apiVersion: v1
    # kind: ConfigMap
    # metadata:
    # namespace: metallb-system
    # name: config
    # data:
    # config: |
    #     address-pools:
    #     - name: default
    #     protocol: layer2
    #     addresses:
    #     - 192.168.1.240/28
EOF
    microk8s kubectl create deployment nginx --image=nginx
    microk8s kubectl scale deployment nginx --replicas=2
    microk8s kubectl get deployment nginx
    microk8s kubectl expose deployment nginx --type=NodePort --port=80
    microk8s kubectl get svc nginx
    microk8s kubectl get services
    microk8s kubectl describe svc nginx
    microk8s kubectl get pods
    microk8s enable dns
    microk8s enable hostpath-storage
    microk8s kubectl get all --all-namespaces -o wide
fi
