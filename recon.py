from scanner import scan_port
from banner_grab import grab_banner

target = input("Enter target IP: ")

start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(f"\nScanning {target}...\n")

for port in range(start_port, end_port + 1):

    if scan_port(target, port):

        print(f"[+] Port {port} OPEN")

        banner = grab_banner(target, port)

        print(f"    Banner: {banner[:100]}")