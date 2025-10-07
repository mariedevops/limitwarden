# 🚦 LimitWarden

LimitWarden is a Kubernetes-native tool that automatically detects and patches workloads missing resource limits. 
It helps teams enforce best practices by applying smart CPU and memory defaults to `Deployments` and `StatefulSets` 
keeping clusters stable, efficient, and safe.

## ✨ Features

- 🔍 Scans all namespaces for unbounded containers
- 🧠 Applies heuristic-based CPU/memory requests and limits
- 🔧 Patches workloads automatically via Kubernetes API
- 🕒 Runs as a CronJob every hour (configurable)
- 🐍 Written in Python, easy to extend
- 📦 One-line installer for instant setup

## 🚀 Quick Install (One-Line)

```bash
curl -s https://raw.githubusercontent.com/mariedevops/limitwarden/main/install-limitwarden.sh | bash


## 🧵 Install via Helm

```bash
helm repo add limitwarden https://mariedevops.github.io/limitwarden
helm install limitwarden limitwarden/limitwarden


### 2. **Add a Badge**
```markdown
![Helm Chart](https://img.shields.io/badge/Install%20with-Helm-blue?logo=helm)
