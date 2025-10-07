from config import DEFAULT_CPU_REQUEST, DEFAULT_MEMORY_REQUEST
from utils import warn

def get_usage_for_container(workload):
    # Stub: Replace with Prometheus or Metrics Server integration
    warn(f"No metrics available for {workload['container_name']} — using defaults.")
    return {
        "cpu_millicores": int(DEFAULT_CPU_REQUEST.replace("m", "")),
        "memory_mebibytes": int(DEFAULT_MEMORY_REQUEST.replace("Mi", ""))
    }
