from kubernetes import client
from utils import log

apps_v1 = client.AppsV1Api()

def patch_workload(workload, resources):
    patch = {
        "spec": {
            "template": {
                "spec": {
                    "containers": [{
                        "name": workload["container_name"],
                        "resources": resources
                    }]
                }
            }
        }
    }

    namespace = workload["namespace"]
    name = workload["name"]
    kind = workload["kind"]

    if kind == "Deployment":
        apps_v1.patch_namespaced_deployment(name, namespace, patch)
    elif kind == "StatefulSet":
        apps_v1.patch_namespaced_stateful_set(name, namespace, patch)

    log(f"Patched {kind} {name} in {namespace} with resources for container {workload['container_name']}")
