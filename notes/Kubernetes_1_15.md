<p align="center">
    <img alt="Kubernets Logo" src="https://cdn.worldvectorlogo.com/logos/kubernets.svg" height="150" />
</p>


Setup
-----

Follow the following to run Kubernetes 1.10 Cluster Using Kubeadm on Ubuntu 16.04 / 18.04

### Nodes

First we need to create at least two or three servers with Ubuntu 16.04 Installed.

```console
kub-master           http(s)://$kub_master/
kub-worker-01        http(s)://$kub_worker_01/
kub-worker-02        http(s)://$kub_worker_02/
```


### Install Docker

You need to install docker on all these nodes

```console
$ apt-get update
$ sudo apt install docker.io
```

Then ensure that it is enabled to start after reboot:

```console
$ sudo systemctl enable docker
```


### Install Kubernetes

Also we need to install Kubernetes on all these nodes

Let's start by adding the Kubernetes signing key:

```console
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
```

Add Kubernetes repository for server OS

```console
$ sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
// Or
$ sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-bionic main"

$ apt-get update
$ sudo apt install kubeadm
```

We need to disable swap memory on all your nodes (master & slave) If Kubernetes will refuse to function:

```console
$ sudo swapoff -a
```


### Initialize Kubernetes Master Node

Now we can initialize the Kubernetes master node. To do so execute the following on your master node:

```console
kub-master:~$ sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

**Take a note of the entire kubeadm join command from the bottom of the above Kubernetes master node initialization output** as you will use this command later when joining the Kubernetes cluster with your slave nodes.


To start using your cluster, you need to run the following as a regular user:

```console
kub-master:~$ mkdir -p $HOME/.kube
kub-master:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
kub-master:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


### Deploy a pod network

We need to deploy a pod network. The pod network is used for communication between nodes within the Kubernetes cluster.

```console
kub-master:~$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

it may take some time to bring the entire flannel network up. Use the kubectl command to confirm that everything is up and ready:

```console
kub-master:~$ kubectl get pods --all-namespaces
```


### Join Kubernetes Cluster

Do you remember the join command that appear in master node initialization output, It is time to run it on the worker or slave nodes.

```console
kub-worker-01:~$ kubeadm join $kub_master:6443 --token fbfinf.sismkgworgoa5319 --discovery-token-ca-cert-hash sha256:abe4cf3ee491d8e89c2c32bb9e7dba5c09061229a318e995d9617464f5e5144c

kub-worker-02:~$ kubeadm join $kub_master:6443 --token fbfinf.sismkgworgoa5319 --discovery-token-ca-cert-hash sha256:abe4cf3ee491d8e89c2c32bb9e7dba5c09061229a318e995d9617464f5e5144c
```

On your Kubernetes master node confirm that the node `kub-worker-01` and `kub-worker-01` is now part of our Kubernetes cluster:

```console
kub-master:~$ kubectl get nodes
```


### Running An Application on the Cluster

Still within the master node, execute the following command to create a deployment with nginx:

```console
kub-master:~$ kubectl run nginx --image=nginx --port 80
```

Then run the following command to create a service named nginx that will expose the app publicly.

It will do so through a NodePort, a scheme that will make the pod accessible through an arbitrary port opened on each node of the cluster:

```console
kub-master:~$ kubectl expose deploy nginx --port 80 --target-port 80 --type NodePort
```

Run the following command to get services:

```console
kub-master:~$ kubectl get services
```

From the output, you can retrieve the port that Nginx is running on. Kubernetes will assign a random port that is greater than 30000 automatically, while ensuring that the port is not already bound by another service.

To test that everything is working, visit `http://$kub_worker_01:$nginx_port` or `http://$kub_worker_01:$nginx_port` through a browser on your local machine. You will see Nginx's familiar welcome page.

If you would like to remove the Nginx application, first delete the nginx service from the master node:

```console
kub-master:~$ kubectl delete service nginx
```

Then delete the deployment:

```console
kub-master:~$ kubectl delete deployment nginx
```

Architecture
------------



Working with the Cluster
------------------------

### Recommended Labels

You can visualize and manage Kubernetes objects with more tools than kubectl and the dashboard. A common set of labels allows tools to work interoperably, describing objects in a common manner that all tools can understand.

In order to take full advantage of using these labels, they should be applied on every resource object.

| Key                                   | Description                                                       | Example                     | Type   |
| --------------------------------------|-------------------------------------------------------------------|---------------------------- |--------|
| app.kubernetes.io/name                | The name of the application                                       | mysql                       | string |
| app.kubernetes.io/instance            | A unique name identifying the instance of an application          | wordpress-abcxzy            | string |
| app.kubernetes.io/version             | The current version of the application                            | 5.7.21                      | string |
| app.kubernetes.io/component           | The component within the architecture                             | database                    | string |
| app.kubernetes.io/part-of             | The name of a higher level application this one is part of        | wordpress                   | string |
| app.kubernetes.io/managed-by          | The tool being used to manage the operation of an application     | helm                        | string |

for example
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  labels:
    app.kubernetes.io/name: mysql
    app.kubernetes.io/instance: wordpress-abcxzy
    app.kubernetes.io/version: "5.7.21"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: wordpress
    app.kubernetes.io/managed-by: helm
```

Pocket Reference
----------------

```console
// kubectl on linux
$ curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/linux/amd64/kubectl
$ chmod +x ./kubectl
$ sudo mv ./kubectl /usr/local/bin/kubectl
$ kubectl version


// kubectl on mac
$ curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/darwin/amd64/kubectl
$ chmod +x ./kubectl
$ sudo mv ./kubectl /usr/local/bin/kubectl
$ kubectl version

$ export KUBECONFIG="/path/to/kubeconfig.yaml"

// help
$ kubectl help

// get nodes list
$ kubectl get nodes

// Create the objects defined in a configuration file
$ kubectl create -f nginx.yaml

// Delete the objects defined in two configuration files:
$ kubectl delete -f nginx.yaml -f redis.yaml

// Update the objects defined in a configuration file by overwriting the live configuration:
$ kubectl replace -f nginx.yaml

// Process all object configuration files in the configs directory, and create or patch the live objects.
// You can first diff to see what changes are going to be made, and then apply:
$ kubectl diff -f configs/
$ kubectl apply -f configs/

// Recursively process directories
$ kubectl diff -R -f configs/
$ kubectl apply -R -f configs/

// To set the namespace for a current request, use the --namespace flag.
$ kubectl run nginx --image=nginx --namespace=<insert-namespace-name-here>
$ kubectl get pods --namespace=<insert-namespace-name-here>

// Setting the namespace preference
// You can permanently save the namespace for all subsequent kubectl commands in that context.
$ kubectl config set-context --current --namespace=<insert-namespace-name-here>
# Validate it
$ kubectl config view | grep namespace:

// Most Kubernetes resources (e.g. pods, services, replication controllers, and others) are in some namespaces.
// However namespace resources are not themselves in a namespace. And low-level resources, such as nodes and persistentVolumes,
// are not in any namespace.
// To see which Kubernetes resources are and aren’t in a namespace:
# In a namespace
$ kubectl api-resources --namespaced=true

# Not in a namespace
$ kubectl api-resources --namespaced=false


// label selector styles can be used to list or watch resources
//   apiVersion: v1
//   kind: Pod
//   metadata:
//     name: label-demo
//     labels:
//       environment: production
//       app: nginx
//   spec:
//     containers:
//     - name: nginx
//       image: nginx:1.7.9
//       ports:
//       - containerPort: 80
$ kubectl get pods -l environment=production,tier=frontend
$ kubectl get pods -l 'environment in (production),tier in (frontend)'
$ kubectl get pods -l 'environment in (production, qa)'
$ kubectl get pods -l 'environment,environment notin (frontend)'


// Field selectors let you select Kubernetes resources based on the value of one or more resource fields.
$ kubectl get pods --field-selector status.phase=Running
$ kubectl get pods --field-selector metadata.name=my-service
$ kubectl get pods --field-selector metadata.namespace!=default
$ kubectl get pods --field-selector status.phase=Pending

// Field selectors are essentially resource filters. By default, no selectors/filters are applied,
// meaning that all resources of the specified type are selected. This makes the following kubectl queries equivalent:
$ kubectl get pods
$ kubectl get pods --field-selector ""

// This selects all Kubernetes Services that aren’t in the default namespace
$ kubectl get services  --all-namespaces --field-selector metadata.namespace!=default


// This kubectl command selects all Pods for which the status.phase does not equal Running and the spec.restartPolicy field equals Always:
$ kubectl get pods --field-selector=status.phase!=Running,spec.restartPolicy=Always
```


References
----------
- [Kubernetes Concepts.](https://kubernetes.io/docs/concepts/)
- [Kubectl Docs.](https://kubectl.docs.kubernetes.io/)
- [Community Content.](https://github.com/kubernetes/community)
