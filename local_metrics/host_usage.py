import psutil

def get_system_usage():
    
    
    cpu_util = psutil.cpu_percent(interval=0.1)
    ram_util = int(psutil.virtual_memory().percent)

    top_tasks = []
    
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            p_info = proc.info
            state = "Active" if p_info['status'] == psutil.STATUS_RUNNING else "Disabled"
            
            top_tasks.append({
                "pid": p_info['pid'],
                "name": p_info['name'] if p_info['name'] else "Unknown/System",
                "state": state
            })
            
            if len(top_tasks) == 8: # Strictly isolate top 8 tasks
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return {
        "cpu_utilization_percent": cpu_util,
        "ram_utilization_percent": ram_util,
        "processes": top_tasks
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_usage(), indent=4))