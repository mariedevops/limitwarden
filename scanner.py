from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.exceptions import ApiException
from utils import log
import os

# Load Kubernetes config
try:
    config.load_incluster_config()
    namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read().strip()
    log(f"🔐 Loaded in-cluster config for namespace: {namespace}")
except ConfigException:
    config.load_kube_config()
    namespace = os.getenv("LIMITWARDEN_NAMESPACE", "default")
    log(f"🧪 Loaded local kubeconfig (namespace: {namespace})")

apps_v1 = client.AppsV1Api()

def find_unbounded_workloads():
    workloads = []

    try:
        log("🔍 Attempting cluster-wide scan...")
        deployments = apps_v1.list_deployment_for_all_namespaces().items
        statefulsets = apps_v1.list_stateful_set_for_all_namespaces().items
    except ApiException as e:
        if e.status == 403:
            log("⚠️ Cluster-wide access denied. Falling back to namespace-only scan.")
            deployments = apps_v1.list_namespaced_deployment(namespace=namespace).items
            statefulsets = apps_v1.list_namespaced_stateful_set(namespace=namespace).items
        else:
            raise

    for workload in deployments + statefulsets:
        kind = "Deployment" if workload.metadata.name in [d.metadata.name for d in deployments] else "StatefulSet"
        name = workload.metadata.name

        for container in workload.spec.template.spec.containers:
            resources = container.resources
            if not resources or not resources.requests or not resources.limits:
                log(f"🛠 Found unbounded container: {container.name} in {kind} {name} ({namespace})")
                workloads.append({
                    "kind": kind,
                    "namespace": namespace,
                    "name": name,
                    "container_name": container.name
                })

    return workloads
