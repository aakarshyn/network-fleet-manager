import os
import platform
import socket
import uuid

def get_core_host_info():
    
    local_ip = "127.0.0.1"
   
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except Exception:
        pass

    
    mac_raw = uuid.getnode()
    mac_address = ':'.join(['{:02x}'.format((mac_raw >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])

    return {
        "device_name": platform.node(),
        "ip_address": local_ip,
        "mac_address": mac_address,
        "hostname": socket.gethostname(),
        "operating_system": f"{platform.system()} {platform.release()} (Kernel: {platform.version()})"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_core_host_info(), indent=4))