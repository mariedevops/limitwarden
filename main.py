from scanner import find_unbounded_workloads
from metrics import get_usage_for_container
from heuristics import suggest_resources
from patcher import patch_workload
from utils import log

def main():
    log("🚀 Starting LimitWarden...")
    workloads = find_unbounded_workloads()

    for workload in workloads:
        usage = get_usage_for_container(workload)
        resources = suggest_resources(usage)
        patch_workload(workload, resources)

    log("✅ LimitWarden completed.")

if __name__ == "__main__":
    main()
