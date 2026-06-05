import paramiko


SSH_USER = "admin"
SSH_PASS = "fleet2026"


def fetch_remote_node_metrics(
        target_ip,
        node_name):

    ssh = None

    try:

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        ssh.connect(
            hostname=target_ip,
            username=SSH_USER,
            password=SSH_PASS,
            timeout=3
        )

        metric_command = (
            "python3 -c "
            "\"import psutil,platform,socket;"
            "print(f'{int(psutil.cpu_percent(interval=0.1))}"
            "|{int(psutil.virtual_memory().percent)}"
            "|{platform.system()} {platform.release()}"
            "|{socket.gethostname()}.local')\""
        )

        stdin, stdout, stderr = (
            ssh.exec_command(
                metric_command
            )
        )

        metric_output = (
            stdout.read()
            .decode()
            .strip()
        )

        (
            cpu_text,
            ram_text,
            os_text,
            hostname_text
        ) = metric_output.split("|")

        cpu_usage = int(cpu_text)
        ram_usage = int(ram_text)

        process_command = (
            "python3 -c "
            "\"import psutil;"
            "seen=[];"
            "procs=[];"
            "for p in psutil.process_iter(['name']):"
            " n=p.info['name'];"
            " "
            " if n and n not in seen:"
            "  seen.append(n);"
            "  procs.append(n);"
            "print('|'.join(procs[:4]))\""
        )

        stdin, stdout, stderr = (
            ssh.exec_command(
                process_command
            )
        )

        process_output = (
            stdout.read()
            .decode()
            .strip()
        )

        services = []

        if process_output:

            for process_name in (
                    process_output.split("|")):

                services.append({
                    "name": process_name,
                    "status": "Active"
                })

        return {
            "device_name": node_name,
            "ip_address": target_ip,
            "hostname": hostname_text,
            "operating_system": os_text,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "network_interface":
                "Remote Wireless Link Adaptor",
            "services": services
        }

    except Exception as error:

        return {
            "device_name": node_name,
            "ip_address": target_ip,
            "hostname": node_name,
            "operating_system":
                "Remote System (Ping Responsive)",
            "cpu_usage": 0,
            "ram_usage": 0,
            "network_interface":
                "Remote Wireless Link Adaptor",
            "services": [
                {
                    "name": str(error),
                    "status": "Disabled"
                }
            ]
        }

    finally:

        if ssh:

            try:
                ssh.close()
            except Exception:
                pass