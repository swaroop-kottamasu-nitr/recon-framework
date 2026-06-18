from scapy.all import *
from utils.timing import random_delay
import random
def run():
    print("Starting ACK Scan...\n")

    from concurrent.futures import ThreadPoolExecutor
    from scapy.all import IP, TCP, ICMP, sr1

    target = input("Enter target IP: ")
    unfc=0
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nACK Scanning {target}...\n")


    def ack_scan(port):
        try:
            src_port = random.randint(1024, 65535)
            packet = IP(dst=target) / TCP(
                sport=src_port,
                dport=port,
                flags="A"
            )
            random_delay()  # Introduce a random delay before sending the packet
            response = sr1(
                packet,
                timeout=1.5,
                verbose=0
            )

            if response is None:
                pass

            elif response.haslayer(TCP):

                flags = response[TCP].flags

                # RST or RST-ACK
                if flags & 0x04:
                    print(f"[+] Port {port}: UNFILTERED")
                    unfc+=1

            elif response.haslayer(ICMP):
                pass

        except Exception as e:
            print(f"[!] Port {port}: ERROR ({e})")


    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(ack_scan, ports)
    print(f"\nTotal Unfiltered Ports: {unfc}")
    print("\nScan Complete!")