## Project Overview
This project is intended to be a reflection of my understanding on Devops concepts like CI/CD , Kubernetes, Containerization of application. For that purpose I have used tools like Minikue , docker engine , Helm and github for scm. Project tailored for minikube , but it can be used on any k8s clusters.

## Table of Contents

- [Requirements](#requirements-stages)
- [Folder Structure](#folder-structure)
- [Step-by-step Instructions](#Step-by-step-instructions)
- [Important Notes](#important-notes)

## Requirements
In order to run project you will need below mentioned tools. I have mentioned how to install on a Linux OS , for other operating system you can find informations on links.

- Kubernetes command-line tool , <b>kubectl</b>  
https://kubernetes.io/docs/tasks/tools/install-kubectl/
```sh
$ curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.19.0/bin/linux/amd64/kubectl
$ chmod +x ./kubectl
$ sudo mv ./kubectl /usr/local/bin/kubectl
```
- Docker Engine install , <b>docker</b>  
https://docs.docker.com/engine/install/ubuntu/
```sh
 $ sudo apt-get update
 $ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
 $   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
 $  echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
- Helm Install , <b>helm</b>  
https://helm.sh/docs/intro/install/
```sh
$ curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

- Minikube Install , <b>minikube</b>  
https://minikube.sigs.k8s.io/docs/start/
```sh
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Folder Structure

```sh
.
+-- adjust-helm  (Helm chart folder which contains all of the resource definitions necessary to run an application, tool, or service inside of a Kubernetes cluster.)
|   +-- Chart.yaml ( A YAML file containing information about the chart) 
|   +-- values.yaml(The default configuration values for this chart) 
|   +-- templates/ (A directory of templates that, when combined with values, will generate valid Kubernetes manifest files.) 
|   |	+-- NOTES.txt (A plain text file containing short usage notes) 
|   |	+-- *.yaml (service , deployment, ingress , hpa manifest files for kubernetes) 
+-- http_server (Project folder which contains a Flask Python REST API Application)
|   +-- test_api.py (python application code file) 
|   +-- Dockerfile (Dockerfile to containerize python applciation) 
|   +-- .dockerignore (contains files and folders which will be excluded while containerizing application) 
.
````

## Step-by-step Instructions

- Initially you need to install tools mentioned in [Requirements](#requirements-stages) section. 
- Get into http_server folder and containerize your application. After Creating Docker image of applications and pushing them to  private or public container registry. I have used my docker hub account. *you can replace $ signed places with your values
```sh
$ cd http_server
$ docker build -t $REPO_PATH/$IMAGE_NAME:$IMAGE_VERSION .   # In my project I have used "docker build -t nkaplan19/adjust-test:latest ." nkaplan19 is my dockerhub repo
$ docker push $REPO_PATH/$IMAGE_NAME:$IMAGE_VERSION   # Pushing container image to container registry from which k8s pod will pull image from.
```
-  Go to adjust-helm directory from project root folder. Firstly create a namespace on kubernetes cluster. In our project we are going to create a namespace named <b>adjust</b>.
```sh
$ cd adjust-helm 
$ kubectl create ns adjust 

```
-  In adjust-helm directory install the helm chart to <b>adjust</b> namespace in k8s cluster .
```sh
$ helm install adjust-app . -n adjust 
```
-  If helm chart installation will not fail you will see below instruction lines from which you will be able to connect running application. you can also do port forwarding in order to test locally. 
```sh
NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace adjust -o jsonpath="{.spec.ports[0].nodePort}" services adjust-service )
  export NODE_IP=$(kubectl get nodes --namespace adjust -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
  
Note : If you are using minikube 

kubectl port-forward service/adjust-service YOUR_PORT:5000 -n adjust
2. Also an ingress definiton added, you can change test.adjust.com definition inside values.yaml file.
```

## Important Notes
- Helm package manager tool is used in order to deploy  application to your kubernetes cluster. 
- Project is tailored for minikube. 
- Health check url of application is both used in dockerfile and deployments livenessProbe. 
- For security concerns application running as non-root user. 
- Alpine image is used for containerization in order to minimize image size.
- For HA initial replica number is 2. 
- Horizantal auto scaling is enabled. Both memory and cpu utilization monitored for scaling. Replica limit is set to min 2 and max 5 pods.



