import socket
import threading
import platform
import os
from queue import Queue

# Globals
live_hosts = []
queue = Queue()

# -----------------------
# Auto-detect subnet
# -----------------------
def get_local_subnet():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = '.'.join(local_ip.split('.')[:3])
        print(f"[*] Detected local IP: {local_ip}")
        print(f"[*] Using subnet: {subnet}.0/24")
        return subnet
    except:
        print("[-] Could not detect local IP.")
        exit()

# -----------------------
# Ping IP
# -----------------------
def ping(ip):
    system = platform.system().lower()
    param = "-n" if system == "windows" else "-c"
    wait = "-w" if system == "windows" else "-W"
    cmd = f"ping {param} 1 {wait} 1 {ip} > nul 2>&1" if system == "windows" else f"ping {param} 1 {wait} 1 {ip} > /dev/null 2>&1"
    if os.system(cmd) == 0:
        print(f"[+] Host up: {ip}")
        live_hosts.append(ip)

# -----------------------
# Discover all hosts
# -----------------------
def discover_hosts():
    subnet = get_local_subnet()
    print(f"[*] Scanning subnet {subnet}.0/24 for live hosts...")

    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        queue.put(ip)

    def worker():
        while not queue.empty():
            ip = queue.get()
            ping(ip)
            queue.task_done()

    for _ in range(100):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    queue.join()

    print("\n[+] Discovery complete. Live hosts:")
    for host in live_hosts:
        print(f"  {host}")

# -----------------------
# Port scanner
# -----------------------
def scan_target(target_ip):
    print(f"\n[*] Starting scan on {target_ip} (ports 1–1024)")
    open_ports = []

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "Unknown"
                    print(f"[+] Port {port} open ({service})")
                    open_ports.append((port, service))
        except:
            pass

    threads = []
    for port in range(1, 1025):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n[+] Scan complete.")
    for port, service in open_ports:
        print(f"  Port {port}: {service}")

# -----------------------
# Menu
# -----------------------
def main():
    while True:
        print("\n--- Network Scanner ---")
        print("1. Find all IPs on the network")
        print("2. Scan ports and services of a target")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            discover_hosts()
        elif choice == "2":
            target_ip = input("Enter target IP: ")
            scan_target(target_ip)
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
