import socket
import ipaddress
import concurrent.futures
import psutil
from app.config import TCP_PORT, UDP_TIMEOUT  # still using your config for timeouts

def get_local_ip():
    """Get the machine's LAN IP address (non-loopback)."""
    gateways = psutil.net_if_addrs()
    for interface, addrs in gateways.items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                return addr.address
    return None

def scan_ip(ip):
    """Try to connect to a given IP using TCP and return it if it's open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(UDP_TIMEOUT)
            result = sock.connect_ex((str(ip), TCP_PORT))
            if result == 0:
                return str(ip)
    except:
        return None
    return None

def discover_devices():
    devices = []

    # Always check localhost for testing
    if scan_ip("127.0.0.1"):
        devices.append("127.0.0.1")

    # Scan the LAN
    local_ip = get_local_ip()
    if local_ip:
        subnet = ipaddress.IPv4Network(local_ip + "/24", strict=False)
        print(f"[INFO] Scanning network: {subnet}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(scan_ip, ip) for ip in subnet.hosts()]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result and result not in devices:
                    devices.append(result)

    print("\n[+] Devices with open port", TCP_PORT)
    for dev in devices:
        print(" -", dev)

    return devices
