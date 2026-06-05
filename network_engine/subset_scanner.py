import socket
import subprocess
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_local_subnet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
    finally:
        sock.close()

    return ".".join(local_ip.split(".")[:3])


def get_mac_address(ip_address):
    try:

        if sys.platform.startswith("win"):
            arp_output = subprocess.check_output(
                ["arp", "-a"],
                text=True,
                stderr=subprocess.DEVNULL
            )

            pattern = (
                rf"{re.escape(ip_address)}\s+"
                r"([0-9a-fA-F\-]{17})"
            )

        else:
            arp_output = subprocess.check_output(
                ["arp", "-a"],
                text=True,
                stderr=subprocess.DEVNULL
            )

            pattern = (
                rf"\({re.escape(ip_address)}\)\s+at\s+"
                r"([0-9a-fA-F:]{17})"
            )

        match = re.search(pattern, arp_output)

        if match:
            return match.group(1)

    except Exception:
        pass

    return "Unknown"


def ping_host(ip_address):

    try:

        if sys.platform.startswith("win"):

            command = [
                "ping",
                "-n",
                "1",
                "-w",
                "800",
                ip_address
            ]

        else:

            command = [
                "ping",
                "-c",
                "1",
                "-t",
                "1",
                ip_address
            ]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode != 0:
            return None

        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except Exception:
            hostname = f"Node-{ip_address.split('.')[-1]}"

        mac_address = get_mac_address(ip_address)

        return {
            "device_name": hostname,
            "ip_address": ip_address,
            "mac_address": mac_address,
            "device_type": "workstation"
        }

    except Exception:
        return None


def write_internet_details(device_count, subnet):

    try:

        with open("_InternetDetails.txt", "w") as file:

            file.write("Internet Details\n")
            file.write("====================\n\n")

            file.write("Service Provider: Unknown\n")
            file.write("Speed: Unknown\n")
            file.write(
                f"Connected Subnet Devices: "
                f"{device_count}\n"
            )
            file.write(
                f"Subnet Prefix: {subnet}\n"
            )

    except Exception:
        pass


def scan_local_subnet():

    subnet_prefix = get_local_subnet()

    discovered_nodes = []

    with ThreadPoolExecutor(max_workers=65) as executor:

        futures = []

        for host in range(1, 255):

            ip_address = (
                f"{subnet_prefix}.{host}"
            )

            futures.append(
                executor.submit(
                    ping_host,
                    ip_address
                )
            )

        for future in as_completed(futures):

            result = future.result()

            if result:
                discovered_nodes.append(result)

    write_internet_details(
        len(discovered_nodes),
        subnet_prefix
    )

    return discovered_nodes