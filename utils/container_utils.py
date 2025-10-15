from utils.utils import log
def extract_containers(doc, kind):
    if kind in {"Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob"}:
        return doc.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
    elif kind == "Pod":
        return doc.get("spec", {}).get("containers", [])
    elif kind == "RabbitmqCluster":
        rabbitmq_spec = doc.get("spec", {}).get("rabbitmq", {})
        containers = rabbitmq_spec.get("containers", [])
        if containers:
            return containers
        log("⚠️ No containers declared in RabbitmqCluster. Injecting default container for patching.")
        return [{
            "name": "rabbitmq",
            "resources": rabbitmq_spec.get("resources", {})  # fallback if operator supports this
        }]
    else:
        return []
