from concurrent.futures import ThreadPoolExecutor
from scanner import scan_port
from banner_grab import grab_banner
from services import get_service




target = input("Enter target IP: ")

start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(f"\nScanning {target}...\n")


def scan_target(port):

    if scan_port(target, port):

        service = get_service(port)

        print(f"\n[+] Port {port} OPEN ({service})")

        if service in ["HTTP", "HTTPS", "SSH", "FTP"]:
            banner = grab_banner(target, port)
            print(f"    Banner: {banner[:100]}")

ports = range(start_port, end_port + 1)

with ThreadPoolExecutor(max_workers=50) as executor:

    executor.map(scan_target, ports)

print("\nScan Complete!")