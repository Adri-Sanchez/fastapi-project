# FastAPI ECG Microservice

This project is a FastAPI microservice that processes and analyzes electrocardiogram (ECG) data, designed with scalability and security in mind. The microservice is containerized with Docker and can be deployed on Kubernetes.
User roles and security implemented in the different endpoints.
## Prerequisites

- Docker
- Kubernetes (Minikube or any other Kubernetes cluster)
- kubectl
- Python 3.11

## Setup

### Leverage the services using Docker Compose
```sh
docker compose up --build
```

### Usage of the Kubernetes cluster (minkube example)
Build the Docker image for the FastAPI backend:

```sh
# Start the minikube cluster if not already running
minikube start
eval $(minikube docker-env) # Use the minikube Docker daemon

# Build the Docker image for the FastAPI backend
docker build -t ecg-backend:latest backend/
chmod +x ./k8s/setup.sh

# To start the services
./k8s/setup.sh up

# To stop the services
./k8s/setup.sh down
```

### Run the tests automatically
```sh
docker compose run --rm --build pytest
```