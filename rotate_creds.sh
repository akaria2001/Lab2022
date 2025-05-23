#!/bin/sh

cd $HOME
rm -rfv $HOME/.ssh/id_ecdsa*
ssh-keygen -b 256 -t ecdsa -q -f $HOME/.ssh/id_ecdsa -N ""
KEY=$(cat $HOME/.ssh/id_ecdsa.pub)
sleep 2
cp -rfv $HOME/bin/cloud-init-test.yaml.template $HOME/bin/cloud-init-test.yaml
sed -i "s|TMPKEY|$KEY|g" $HOME/bin/cloud-init-test.yaml
cat $HOME/.ssh/id_ecdsa.pub 
grep -i ecdsa $HOME/bin/cloud-init-test.yaml
