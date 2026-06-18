from scapy.all import *
def run():
    print("Starting UDP Scan...\n")

    from concurrent.futures import ThreadPoolExecutor

    import threading

    target = input("Enter target IP: ")

    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nUDP Scanning {target}...\n")

    open_filtered_ports = []
    closed_ports = []

    lock = threading.Lock()


    def udp_scan(port):
        try:
            packet = IP(dst=target) / UDP(dport=port)

            response = sr1(
                packet,
                timeout=4,
                verbose=0
            )

            with lock:

                if response is None:
                    open_filtered_ports.append(port)

                elif response.haslayer(ICMP):

                    icmp_type = response[ICMP].type
                    icmp_code = response[ICMP].code

                    # Destination Unreachable - Port Unreachable
                    if icmp_type == 3 and icmp_code == 3:

                        closed_ports.append(port)

                    else:

                        print(
                            f"[DEBUG] Port {port}: "
                            f"ICMP Type={icmp_type} Code={icmp_code}"
                        )

                else:

                    print(
                        f"[DEBUG] Port {port}: "
                        f"Unexpected Response"
                    )
                

        except Exception as e:

            with lock:
                print(f"[ERROR] Port {port}: {e}")


    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:

        executor.map(udp_scan, ports)

    print("\nUDP Scan Summary")
    print("----------------")

    if open_filtered_ports:

        print("\nOpen|Filtered Ports:")
        print(sorted(open_filtered_ports))

    if closed_ports:

        print("\nClosed Ports:")
        print(sorted(closed_ports))

    print(f"\nTotal Open|Filtered: {len(open_filtered_ports)}")
    print(f"Total Closed: {len(closed_ports)}")

    print("\nNote:")
    print("Open|Filtered means no ICMP Port Unreachable response was received.")
    print("It does NOT guarantee that the port is open.")

    print("\nScan Complete!")