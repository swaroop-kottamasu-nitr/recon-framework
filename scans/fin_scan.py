from scapy.all import *
from utils.timing import random_delay
def run():
    print("Starting FIN Scan...\n")
    from concurrent.futures import ThreadPoolExecutor
    

    target = input("Enter target IP: ")
    cc=0
    oc=[]
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nFIN Scanning {target}...\n")


    def fin_scan(port):

        packet = IP(dst=target) / TCP(
            dport=port,
            flags="F"
        )
        random_delay()  # Introduce a random delay before sending the packet
        response = sr1(
            packet,
            timeout=1,
            verbose=0
        )

        if response:

            if response.haslayer(TCP):

                if response[TCP].flags & 0x04:
                    
                    cc+=1

        else:
            
            oc.append(port)


    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(fin_scan, ports)
    print("\nScan Complete!")
    print("\nFIN Scan Results:")
    print("------------------")
    print(f"\nTotal Closed Ports: {cc}")
    if oc:
        print("\nOpen|Filtered Ports:\n")
        print(sorted(oc))
    print(f"\nTotal Open|Filtered Ports: {len(oc)}")
        
