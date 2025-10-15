# 🚦 LimitWarden

LimitWarden is a Kubernetes-native tool that automatically detects and patches workloads missing resource limits. It helps teams enforce best practices by applying smart CPU and memory defaults to Kubernetes objects — keeping clusters stable, efficient, and safe.

Originally designed for non-GitOps environments, LimitWarden now supports GitOps workflows as a manifest patcher, making it easy to integrate into CI pipelines, GitHub Actions, or manual workflows.

## ✨ Features

- 🔍 Scans all namespaces for unbounded containers
- 🧠 Applies heuristic-based CPU/memory requests and limits
- 🔧 Patches workloads automatically via Kubernetes API or directly in manifests
- 🕒 Runs as a CronJob every hour (configurable)
- 🐍 Written in Python, easy to extend
- 📦 Available as a one-line installer, Helm chart, or pip-installable CLI

## 🚀 Quick Install (One-Line)

🚀 Installation Options
🛠 For Non-GitOps Projects (Cluster CronJob)
Install LimitWarden directly into your cluster to run as a scheduled CronJob:

bash
# Cluster-wide install
curl -s https://raw.githubusercontent.com/mariedevops/limitwarden/main/install-limitwarden.sh | bash

# Namespace-scoped install (for RBAC-restricted or testing environments)
curl -s https://raw.githubusercontent.com/mariedevops/limitwarden/main/install-limitwarden-ns.sh | bash

Or use Helm:

helm repo add limitwarden https://mariedevops.github.io/limitwarden

helm install limitwarden limitwarden/limitwarden

# 🧵 For GitOps Projects (Manifest Patching)

Use LimitWarden as a CLI tool to patch manifests directly in your GitOps repo:

pip3 install limitwarden

limitwarden scan . --patch --dry-run

limitwarden scan . --patch --write

# You can:

✅ Run it manually before committing

✅ Add it to a pre-commit hook

✅ Integrate it into your CI/CD pipeline (e.g. GitHub Actions, Azure Pipelines)

✅ Enforce hygiene without touching the cluster