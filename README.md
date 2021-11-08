# Kubernetes Training/Tutorial

## The problem

Deploy a web application into a node. Consisting of one virtual machine of 8GB RAM, 4 Cores. Usually one would deploy one container. Having more users of the application has the need to scale the application, meaning to create yet another node with the same application running. 

Even worse, say if we have a versioned application, e.g. v2, that we want to deploy. We have to deploy a new node before destroying a prior version, e.g. v1. 

This leaves us with a problem. We would have 12 cores, 24GB RAM, and three containers overall. This is a bit insane. Now, this is where Kubernetes comes into play and can help. 

Kubernetes will take a single node and then utilize the resources in the correct manner. So instead create new nodes, it will fill one node with as many pods as it can (In K8s you can think of pods as a container). This means, instead of having one container per node, we have multiple containers in one node. Kubernetes orchestrates this cluster of us.

![multiple containers](mutliple_containers.png)

**Kubernetes (K8s) is an application orchestrator**

More specifically: 

* K8s deploys and manages containers that run an application (..or else). 
* K8s scales up and down according to demand
* K8s performs zero downtime deployments
* Rollbacks, etc ...


## Minikube

describe minikube

## Resources within Kubernetes

Let's first have a look at its components.

#### Cluster

A cluster is a set of nodes. A node can be a virtual (VM) or a physical machine, running on the cloud, e.g. Azure, AWS, GCP, or on premise.

#### Nodes

It is important to distinguish between nodes within a K8s cluster. In particular between *master nodes* and *worker nodes*.

The **master node** can be seen as the brain of the cluster. This is where all of the decisions are made. Within the master node, there multiple components that make up the *control plane*, e.g. scheduler, cluster store, API server, cloud controller manager, controller manager.

* scheduler
* cluster store
* API server
* cloud controller manager
* controller manager

The **worker nodes** are responsible for the "heavy lifting" of running an application. 

Within one cluster there are often more than one worker node but only one master node.
Master and worker nodes communicate to each other via the *kubelet*.

![kubernetes cluster](kubernetes_cluster.png)

#### Pods

In K8s, a pod is the smallest deployable unit (and not containers). Within a pod there is always one *main container* representing the application (in whatever language written). Further within a pod, there may or may not be *init containers*, and/or *side containers*. Init containers are containers that are executed before the main container. Side containers are containers that support the main containers, e.g. a container that acts as a proxy to your main container. Also within pods there may also be volumes, which enables containers to share data between them. 

Containers communicate with each other within a pod using localhost and whatever port they expose. The port itself has a unique ip adress. This enables communication between pods via the unique adress.

In contrast to K8s, the smallest deployable unit for docker are containers. 

#### Deployments

#### ReplicaSets

#### DeamonSets

#### Services

Lets let pods talk to each other

customer microservices performs a REST api call to order microservice to fetch some order information

bad way:
get ip of order
go to customer deployment
insert spec env: name order-service
after deleting the pods, the ip address will change. Thus our hardcoded way does not work anymore. never rely on ip adress and uses Services instead (ClusterIpServces).

using service:
containerPort of pod and targetPort have to match, and selector-app and pod-app
clusterip service get endpoints
access only service ip - what if the service pod is restarting?
still need portforward to test because we did not implement external ip service yet
can also use minikube service customer-node to open directly 


* ClusterIP (Default): Default Kubernetes Service Type. Only used for internal access and no external. When letting customer talk to order, we use a order service of type clusterIP calling service-name:port. kubernetes clusterIP is created on default to be able to talk to the kube-apiserver-minikube
* NodePort: Allows to open a port on all nodes. Port range between 30000-32767. Example of two nodes: Nodeport opens one port to both nodes so the client can choose which node to access under one port. The NodePort Service handles this request and checks which pod is healthy and only send requests there. Client wants to run on node one, but pod is only running on node 2 -> Nodeport will send request to pod on node two. Disadvantage is that we can only have one service per port: changes usage of ingress (? what example). If node IP change, then we have a problem
* ExternalName
* LoadBalancer: Standard way of exposing applications to the internet. Creates a load balancer per service (a second service needs a second LB). AWS & GCP create a network load balancer (NLB). NLB distributes traffic between instances. minikube tunnel to run locally. Cloud controller manager talks to underlying cloud provider (which it creates an NLB).


## Commands

To interact with the cluster from our local machine, *kubectl* is needed. 

**kubectl** is a command line tool to run commands against our cluster, e.g. deploy, inspect, edit resources, debug, view logs, etc..
kubectl is also used to connect your cluster, whether it's running in production or any environment.


```bash
# Start a cluster with two nodes
minikube start --nodes=2

# check status of minikube nodes
minikube status

# access the running application using the appname
minikube service myapp

# show docker containers created within nodes
docker ps

docker run --rm -p 80:80 amigoscode/kubernetes:customer-v1

# to interact with the cluster use kubectl
# to show available nodes 
kubectl get nodes

# to show all available pods in all namespaces
# this also shows pods of control pane
kubectl get pods -A

# apply configuration file to run.
kubectl apply -f deployment.yml

# to show the cluster-ips and ports
kubectl get svc

kubectl describe pod <name>
kubectl describe node minikube-m02

kubectl api-resources

kubectl port-forward deployment/customer 8080:8080 

kubectl exec -it hello-world -- ls /
kubectl exec -it hello-world -c hello-world -- bash

kubectl logs hello-world
kubectl logs hello-world -c hello-world

kubectl delete pod hello-world

cat pod.yml | kubectl apply -f -

kubectl run hello-world --image=amigoscode/kubernetes:hello-world --port=80

kubectl get endpoints

kubectl describe service order

minikube ip
minikube ip -n minikube-m02

# open up the url to the service
minikube service customer-node

kubectl exec -it order-7d87cb7758-664rl -- sh

# watch for changes
kubectl get svc -w

# access LoadBalancer on minikube
minikube tunnel
```

## Exemplary deployment

To run K8s locally create a local cluster for example using minikube. Make sure do install Docker and Minikube.

To apply the deployment.yml configuration using kubectl use *kubectl apply -f deployment.yml*. *kubectl get pods* should show two pods running now. Check the cluster-ips and ports using *kubectl get svc*. The ports should denote the same as specified within the deployment.yml. Access the running application using the appname
by using *minikube service myapp*. The app can be run within the browser using the shown ip adress.


