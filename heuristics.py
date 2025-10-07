from config import DEFAULT_CPU_REQUEST, DEFAULT_CPU_LIMIT, DEFAULT_MEMORY_REQUEST, DEFAULT_MEMORY_LIMIT

def suggest_resources(usage):
    if usage:
        cpu_request = int(usage["cpu_millicores"] * 0.9)
        cpu_limit = int(cpu_request * 1.5)
        mem_request = int(usage["memory_mebibytes"] * 0.9)
        mem_limit = int(mem_request * 1.5)

        return {
            "requests": {
                "cpu": f"{cpu_request}m",
                "memory": f"{mem_request}Mi"
            },
            "limits": {
                "cpu": f"{cpu_limit}m",
                "memory": f"{mem_limit}Mi"
            }
        }
    else:
        return {
            "requests": {
                "cpu": DEFAULT_CPU_REQUEST,
                "memory": DEFAULT_MEMORY_REQUEST
            },
            "limits": {
                "cpu": DEFAULT_CPU_LIMIT,
                "memory": DEFAULT_MEMORY_LIMIT
            }
        }
