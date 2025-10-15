import os
import yaml
from heuristics import suggest_resources
from utils.utils import log
from utils.container_utils import extract_containers

# Preserve block-style formatting for multi-line strings
def str_presenter(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

def scan_and_patch_manifests(path, write=False, dry_run=True):
    patched_files = []
    valid_kinds = {"Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "Pod", "RabbitmqCluster"}

    for root, _, files in os.walk(path):
        for file in files:
            if not file.endswith((".yaml", ".yml")):
                continue

            full_path = os.path.join(root, file)
            with open(full_path) as f:
                try:
                    docs = list(yaml.safe_load_all(f))
                except yaml.YAMLError:
                    continue  # skip invalid YAML

            changed = False
            new_docs = []

            for doc in docs:
                if not isinstance(doc, dict):
                    new_docs.append(doc)
                    continue

                kind = doc.get("kind")
                if kind not in valid_kinds:
                    new_docs.append(doc)
                    continue

                containers = extract_containers(doc, kind)

                # Inject default container for RabbitmqCluster if missing
                if kind == "RabbitmqCluster" and not containers:
                    log(f"⚠️ No containers declared in RabbitmqCluster. Injecting default container for patching.")
                    doc.setdefault("spec", {}).setdefault("rabbitmq", {})["containers"] = [{
                        "name": "rabbitmq",
                        "resources": suggest_resources(None)
                    }]
                    changed = True
                    new_docs.append(doc)
                    continue

                for container in containers:
                    name = container.get("name")
                    resources = container.get("resources", {})
                    if not resources or not resources.get("requests") or not resources.get("limits"):
                        log(f"🛠 Found unbounded container: {name} in {kind} ({file})")
                        usage = None  # optional: load from metrics
                        container["resources"] = suggest_resources(usage)
                        changed = True

                new_docs.append(doc)

            if changed:
                patched_files.append(full_path)
                if write and not dry_run:
                    with open(full_path, "w") as f:
                        yaml.dump_all(new_docs, f, sort_keys=False, default_style=None, default_flow_style=False)

    if patched_files:
        log("✅ Patched the following files:")
        for f in patched_files:
            print(f"  - {f}")
    else:
        log("🎉 No files needed patching.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scan and patch Kubernetes manifests")
    parser.add_argument("path", help="Path to directory containing YAML files")
    parser.add_argument("--write", action="store_true", help="Write changes to disk")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    scan_and_patch_manifests(args.path, write=args.write, dry_run=args.dry_run)
