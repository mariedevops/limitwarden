#!/bin/bash

echo "🚀 Installing LimitWarden..."

# Apply RBAC
kubectl apply -f https://raw.githubusercontent.com/mariedevops/limitwarden/main/k8s/limitwarden-rbac-ns.yaml

# Apply CronJob
kubectl apply -f https://raw.githubusercontent.com/mariedevops/limitwarden/main/k8s/limitwarden-cronjob.yaml

echo "✅ LimitWarden installed and scheduled to run every hour."

echo "🔍 Verifying installation..."
kubectl get cronjob limitwarden
