from scapy.all import *
def run():
    print("Starting XMAS Scan...\n")

    from concurrent.futures import ThreadPoolExecutor
    

    target = input("Enter target IP: ")

    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nXMAS Scanning {target}...\n")

    ofp = []
    cp=0

    def xmas_scan(port):

        packet = IP(dst=target) / TCP(
            dport=port,
            flags="FPU"
        )

        response = sr1(
            packet,
            timeout=1,
            verbose=0
        )

        if response:

            if response.haslayer(TCP):

                if response[TCP].flags & 0x04:
                    cp+=1

        else:
            ofp.append(port)


    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(xmas_scan, ports)

    print("\nXMAS Scan Summary")
    print("-----------------")

    if ofp:
        print("Open|Filtered Ports:")
        print(sorted(ofp))

    print(f"\nTotal Open|Filtered ports: {len(ofp)}")
    print(f"Total Closed ports: {cp}")
    print("\nScan Complete!")