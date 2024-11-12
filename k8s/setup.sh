#!/bin/bash

cd "$(dirname "$0")"
ACTION=${1:-up}

if [[ "$ACTION" == "up" ]]; then
    echo "Starting deployment..."

    # Apply the PostgreSQL Persistent Volume Claim (PVC)
    kubectl apply -f postgres-pvc.yml

    # Apply the PostgreSQL Deployment
    kubectl apply -f postgres-deployment.yml

    # Apply the Backend Deployment
    kubectl apply -f backend-deployment.yml

    # Apply the Backend Horizontal Pod Autoscaler (HPA)
    kubectl apply -f backend-hpa.yml

    echo "Deployment completed."

elif [[ "$ACTION" == "down" ]]; then
    echo "Tearing down deployment..."
    kubectl delete -f .
fi

