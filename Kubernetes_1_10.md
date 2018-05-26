Kubernetes 1.10
===============

Follow the following to run Kubernetes 1.10 Cluster Using Kubeadm on Ubuntu 16.04 / 18.04


Setup
-----

### Nodes

First we need to create at least two or three servers with Ubuntu 16.04 Installed.

```bash
kub-master           http(s)://$kub_master/
kub-worker-01        http(s)://$kub_worker_01/
kub-worker-02        http(s)://$kub_worker_02/
```


### Install Docker

You need to install docker on all these nodes

```bash
$ apt-get update
$ sudo apt install docker.io
```

Then ensure that it is enabled to start after reboot:

```bash
$ sudo systemctl enable docker
```


### Install Kubernetes

Also we need to install Kubernetes on all these nodes

Let's start by adding the Kubernetes signing key:

```bash
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
```

Add Kubernetes repository for server OS

```bash
$ sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
// Or
$ sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-bionic main"

$ apt-get update
$ sudo apt install kubeadm 
```

We need to disable swap memory on all your nodes (master & slave) If Kubernetes will refuse to function:

```bash
$ sudo swapoff -a
```


### Initialize Kubernetes Master Node

Now we can initialize the Kubernetes master node. To do so execute the following on your master node:

```bash
kub-master:~$ sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

**Take a note of the entire kubeadm join command from the bottom of the above Kubernetes master node initialization output** as you will use this command later when joining the Kubernetes cluster with your slave nodes.


To start using your cluster, you need to run the following as a regular user:

```bash
kub-master:~$ mkdir -p $HOME/.kube
kub-master:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
kub-master:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


### Deploy a pod network

We need to deploy a pod network. The pod network is used for communication between nodes within the Kubernetes cluster. 

```bash
kub-master:~$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

it may take some time to bring the entire flannel network up. Use the kubectl command to confirm that everything is up and ready:

```bash
kub-master:~$ kubectl get pods --all-namespaces
```


### Join Kubernetes Cluster

Do you remember the join command that appear in master node initialization output, It is time to run it on the worker or slave nodes.

```bash
kub-worker-01:~$ kubeadm join $kub_master:6443 --token fbfinf.sismkgworgoa5319 --discovery-token-ca-cert-hash sha256:abe4cf3ee491d8e89c2c32bb9e7dba5c09061229a318e995d9617464f5e5144c

kub-worker-02:~$ kubeadm join $kub_master:6443 --token fbfinf.sismkgworgoa5319 --discovery-token-ca-cert-hash sha256:abe4cf3ee491d8e89c2c32bb9e7dba5c09061229a318e995d9617464f5e5144c
```

On your Kubernetes master node confirm that the node `kub-worker-01` and `kub-worker-01` is now part of our Kubernetes cluster:

```bash
kub-master:~$ kubectl get nodes
```


### Running An Application on the Cluster

Still within the master node, execute the following command to create a deployment with nginx:

```bash
kub-master:~$ kubectl run nginx --image=nginx --port 80
```

Then run the following command to create a service named nginx that will expose the app publicly.

It will do so through a NodePort, a scheme that will make the pod accessible through an arbitrary port opened on each node of the cluster:

```bash
kub-master:~$ kubectl expose deploy nginx --port 80 --target-port 80 --type NodePort
```

Run the following command to get services:

```bash
kub-master:~$ kubectl get services
```

From the output, you can retrieve the port that Nginx is running on. Kubernetes will assign a random port that is greater than 30000 automatically, while ensuring that the port is not already bound by another service.

To test that everything is working, visit `http://$kub_worker_01:$nginx_port` or `http://$kub_worker_01:$nginx_port` through a browser on your local machine. You will see Nginx's familiar welcome page.

If you would like to remove the Nginx application, first delete the nginx service from the master node:

```bash
kub-master:~$ kubectl delete service nginx
```

Then delete the deployment:

```bash
kub-master:~$ kubectl delete deployment nginx
```


Acknowledgements
----------------

© 2018, Clivern. Released under [The Apache Software License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt).

**Shrimp** is authored and maintained by [@clivern](http://github.com/clivern).
