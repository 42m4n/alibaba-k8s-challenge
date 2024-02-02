# Alibaba-k8s-challenge
Alibaba Technical challenge: Scaling a K8s application based on queue size.
### Overview
This repository contains the solution to the Alibaba technical challenge, which involved setting up a Kubernetes cluster, deploying a Rabbitmq instance with exporter, deploying an application across multiple environments, and configuring it for queue-based auto-scaling.
## Install a kubernetes cluster
1. Clone the kubespray project from Github:
```bash
git clone https://github.com/kubernetes-sigs/kubespray.git
```
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -U pip
```
3. Checkout to the desired kubespray release:
```bash
cd kubesparay
git checkout v2.24.0 -b v2.24.0 # for today this is the latest release
```
4. install required packages:
```bash
pip install -r requirements.txt
```
5. Customize the configuration files based on the sample directory and create a new directory:
i customized the configs base on `kubespray/inventory/sample` directory and named the new directory `kubespray/inventory/alibaba-cluster`
6. start to installation:
```bash
cd kubespray
ansible -i inventory/alibaba-cluster/inventory.ini -b
```
## Deploying a RabbitMQ Instance
1. Learning RabbitMQ:
- I completed a course on RabbitMQ to gain a foundational understanding of its concepts and usage.
2. Deployment:
- I deployed a RabbitMQ instance on the Kubernetes cluster using the following command:
```bash
kubectl apply rabbitmq.yaml
```
## Deploy an application
1. **Application Development**:
- I created two simple Python scripts using the Pika library to interact with RabbitMQ:
  - sender.py: Sends messages to a RabbitMQ queue.
  - receiver.py: Receives messages from the queue.
2.  **Containerization**:
- I wrote a `Dockerfile` to package the Python application into a Docker image.
- I built and pushed the image to Docker Hub for accessibility within the cluster.
3. **Kubernetes Deployment**:
- I deployed the receiver application on the cluster using the receiver.yaml manifest.

## Scale the application based on size of a queue
1. **KEDA Installation**:
- I installed KEDA, a Kubernetes-based Event Driven Autoscaling component, using Helm:
```shell
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace
```
2. **Scaling Configuration**:
- I defined the scaling configuration in the scale.yaml manifest, specifying:
  - The target deployment to be scaled.
  - The RabbitMQ queue to monitor for scaling decisions.
  - The scaling thresholds for triggering pod scaling up or down.
3. **KEDA Integration**:
- KEDA continuously monitors the RabbitMQ queue length.
- When the queue length exceeds the defined threshold, KEDA automatically scales up the target deployment by creating additional pods.
- Conversely, when the queue length falls below the threshold, KEDA scales down the deployment by terminating pods. 
