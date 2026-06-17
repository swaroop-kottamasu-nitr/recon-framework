from concurrent.futures import ThreadPoolExecutor
from scapy.all import *

target = input("Enter target IP: ")

start_port = int(input("Start port: "))
end_port = int(input("End port: "))

print(f"\nSYN Scanning {target}...\n")


def syn_scan(port):

    packet = IP(dst=target) / TCP(
        dport=port,
        flags="S"
    )

    response = sr1(
        packet,
        timeout=2,
        verbose=0
    )

    if response and response.haslayer(TCP):

        flags = response[TCP].flags

        if flags == 0x12:

            print(f"[+] Port {port} OPEN")

            rst = IP(dst=target) / TCP(
                dport=port,
                flags="R"
            )

            send(rst, verbose=0)


ports = range(start_port, end_port + 1)

with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(syn_scan, ports)

print("\nScan Complete!")