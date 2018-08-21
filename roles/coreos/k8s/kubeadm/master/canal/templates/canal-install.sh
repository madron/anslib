#!/bin/sh

set -e

/opt/bin/kubectl apply -f https://docs.projectcalico.org/v3.2/getting-started/kubernetes/installation/hosted/canal/rbac.yaml
/opt/bin/kubectl apply -f https://docs.projectcalico.org/v3.2/getting-started/kubernetes/installation/hosted/canal/canal.yaml
/opt/bin/kubectl apply -f https://docs.projectcalico.org/v3.2/getting-started/kubernetes/installation/manifests/app-layer-policy/kubernetes-datastore/flannel/calico-node.yaml
/opt/bin/kubectl apply -f /opt/kubernetes/istio-1.0.0/istio-1.0.0/install/kubernetes/istio-demo-auth.yaml
/opt/bin/kubectl apply -f https://docs.projectcalico.org/v3.2/getting-started/kubernetes/installation/manifests/app-layer-policy/istio-inject-configmap.yaml

touch /etc/kubernetes/network-plugin-installed
