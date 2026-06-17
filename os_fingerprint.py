from scapy.all import *

target = input("Enter target IP: ")

packet = IP(dst=target) / TCP(
    dport=80,
    flags="S"
)

response = sr1(
    packet,
    timeout=2,
    verbose=0
)

if response and response.haslayer(TCP):

    ttl = response.ttl
    window = response[TCP].window

    print("\nOS Fingerprint Report")
    print("---------------------")
    print(f"TTL: {ttl}")
    print(f"Window Size: {window}")

    if ttl <= 64:
        ttl_guess = "Linux/Unix"

    elif ttl <= 128:
        ttl_guess = "Windows"

    else:
        ttl_guess = "Network Device"

    print(f"\nTTL Analysis: {ttl_guess}")

else:
    print("No response received")