from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.exceptions import ApiException
from utils.utils import log
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
batch_v1 = client.BatchV1Api()
core_v1 = client.CoreV1Api()
custom_api = client.CustomObjectsApi()

def find_unbounded_workloads():
    workloads = []

    def scan(kind, items, container_path):
        for item in items:
            name = item.metadata.name
            ns = item.metadata.namespace
            containers = container_path(item)
            for container in containers:
                resources = container.resources if hasattr(container, "resources") else container.get("resources", {})
                if not resources or not resources.get("requests") or not resources.get("limits"):
                    log(f"🛠 Found unbounded container: {container.get('name') or container.name} in {kind} {name} ({ns})")
                    workloads.append({
                        "kind": kind,
                        "namespace": ns,
                        "name": name,
                        "container_name": container.get("name") if isinstance(container, dict) else container.name
                    })

    try:
        log("🔍 Attempting cluster-wide scan...")
        deployments = apps_v1.list_deployment_for_all_namespaces().items
        statefulsets = apps_v1.list_stateful_set_for_all_namespaces().items
        daemonsets = apps_v1.list_daemon_set_for_all_namespaces().items
        jobs = batch_v1.list_job_for_all_namespaces().items
        cronjobs = batch_v1.list_cron_job_for_all_namespaces().items
        pods = core_v1.list_pod_for_all_namespaces().items
        rabbitmq = custom_api.list_cluster_custom_object(
            group="rabbitmq.com",
            version="v1beta1",
            plural="rabbitmqclusters"
        )["items"]
    except ApiException as e:
        if e.status == 403:
            log("⚠️ Cluster-wide access denied. Falling back to namespace-only scan.")
            deployments = apps_v1.list_namespaced_deployment(namespace=namespace).items
            statefulsets = apps_v1.list_namespaced_stateful_set(namespace=namespace).items
            daemonsets = apps_v1.list_namespaced_daemon_set(namespace=namespace).items
            jobs = batch_v1.list_namespaced_job(namespace=namespace).items
            cronjobs = batch_v1.list_namespaced_cron_job(namespace=namespace).items
            pods = core_v1.list_namespaced_pod(namespace=namespace).items
            rabbitmq = custom_api.list_namespaced_custom_object(
                group="rabbitmq.com",
                version="v1beta1",
                namespace=namespace,
                plural="rabbitmqclusters"
            )["items"]
        else:
            raise

    scan("Deployment", deployments, lambda w: w.spec.template.spec.containers)
    scan("StatefulSet", statefulsets, lambda w: w.spec.template.spec.containers)
    scan("DaemonSet", daemonsets, lambda w: w.spec.template.spec.containers)
    scan("Job", jobs, lambda w: w.spec.template.spec.containers)
    scan("CronJob", cronjobs, lambda w: w.spec.job_template.spec.template.spec.containers)
    scan("Pod", pods, lambda w: w.spec.containers)
    scan("RabbitmqCluster", rabbitmq, lambda w: w.get("spec", {}).get("rabbitmq", {}).get("containers", []))

    return workloads
