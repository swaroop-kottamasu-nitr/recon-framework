from utils.service_enum import enumerate_service

from scapy.all import *


def run():
    print("Starting SYN Scan...\n")

    from concurrent.futures import ThreadPoolExecutor
    
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

                result = enumerate_service(
                    target,
                    port
                )

                print(f"\n[+] Port {port} OPEN")

                print(
                    f"    Service: "
                    f"{result['service']}"
                )

                if result["banner"]:

                    banner = result["banner"]

                    first_line = banner.split("\n")[0]

                    print(
                        f"    Version: "
                        f"{first_line}"
                    )

                else:

                    print(
                        "    Version: Unknown"
                    )
                rst = IP(dst=target) / TCP(
                    dport=port,
                    flags="R"
                )

                send(rst, verbose=0)


    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(syn_scan, ports)

    print("\nScan Complete!")