from kubernetes import client, config
from utils import log

config.load_kube_config()
apps_v1 = client.AppsV1Api()

def find_unbounded_workloads():
    workloads = []
    deployments = apps_v1.list_deployment_for_all_namespaces().items
    statefulsets = apps_v1.list_stateful_set_for_all_namespaces().items

    for workload in deployments + statefulsets:
        kind = "Deployment" if workload in deployments else "StatefulSet"
        namespace = workload.metadata.namespace
        name = workload.metadata.name

        for container in workload.spec.template.spec.containers:
            resources = container.resources
            if not resources or not resources.requests or not resources.limits:
                log(f"Found unbounded container: {container.name} in {kind} {name} ({namespace})")
                workloads.append({
                    "kind": kind,
                    "namespace": namespace,
                    "name": name,
                    "container_name": container.name
                })
    return workloads
