from scapy.all import *

from utils.banner_grabber import get_banner

def icmp_fingerprint(target):

    packet = IP(dst=target) / ICMP()

    response = sr1(
        packet,
        timeout=2,
        verbose=0
    )

    if not response:

        return None

    return {
        "ttl": response.ttl,
        "type": response[ICMP].type,
        "code": response[ICMP].code
    }

def run():
    
    target = input("Enter target IP: ")

    print("\nFingerprinting Target...\n")

    packet = IP(dst=target) / TCP(
        dport=80,
        flags="S"
    )

    response = sr1(
        packet,
        timeout=2,
        verbose=0
    )

    if not response or not response.haslayer(TCP):
        print("No response received.")
        return

    ttl = response.ttl
    window = response[TCP].window
    options = response[TCP].options

    linux_score = 0
    windows_score = 0
    network_device_score = 0

    evidence = []

    # TTL Analysis

    if ttl <= 64:

        linux_score += 1
        evidence.append(
            f"TTL ({ttl}) suggests Linux/Unix"
        )

    elif ttl <= 128:

        windows_score += 1
        evidence.append(
            f"TTL ({ttl}) suggests Windows"
        )

    else:

        network_device_score += 1
        evidence.append(
            f"TTL ({ttl}) suggests Network Device"
        )

    # Window Size Analysis

    linux_windows = [
        5840,
        5720,
        14600,
        29200,
        64240
    ]

    windows_windows = [
        8192,
        16384,
        65535
    ]

    if window in linux_windows:

        linux_score += 1
        evidence.append(
            f"Window Size ({window}) matches common Linux values"
        )

    if window in windows_windows:

        windows_score += 1
        evidence.append(
            f"Window Size ({window}) matches common Windows values"
        )

    # TCP Options Analysis

    option_names = []
    packet_signatures = []
    for option in options:

        if isinstance(option, tuple):

            option_names.append(option[0])
            packet_signatures.append(option[0])
    if "Timestamp" in option_names:

        linux_score += 1
        evidence.append(
            "TCP Timestamp option detected"
        )

    if "WScale" in option_names:

        linux_score += 1
        evidence.append(
            "TCP Window Scaling detected"
        )

    # Banner Analysis

    ssh_banner = get_banner(target, 22)
    http_banner = get_banner(target, 80)
    icmp_data = icmp_fingerprint(target)
    if ssh_banner:

        if "ubuntu" in ssh_banner.lower():

            linux_score += 3

            evidence.append(
                "SSH banner indicates Ubuntu"
            )

        elif "openssh" in ssh_banner.lower():

            linux_score += 2

            evidence.append(
                "OpenSSH detected"
            )

    if http_banner:

        if "ubuntu" in http_banner.lower():

            linux_score += 3

            evidence.append(
                "HTTP banner indicates Ubuntu"
            )

        if "apache" in http_banner.lower():

            linux_score += 1

            evidence.append(
                "Apache web server detected"
            )

    if icmp_data:

        if icmp_data["ttl"] <= 64:

            linux_score += 1

            evidence.append(
                f"ICMP TTL ({icmp_data['ttl']}) suggests Linux/Unix"
            )

        elif icmp_data["ttl"] <= 128:

            windows_score += 1

            evidence.append(
                f"ICMP TTL ({icmp_data['ttl']}) suggests Windows"
            )

        else:

            network_device_score += 1

            evidence.append(
                f"ICMP TTL ({icmp_data['ttl']}) suggests Network Device"
            )
    # Final Decision

    scores = {
        "Linux/Unix": linux_score,
        "Windows": windows_score,
        "Network Device": network_device_score
    }

    likely_os = max(
        scores,
        key=scores.get
    )

    highest_score = scores[likely_os]

    if highest_score >= 6:

        confidence = "Very High"

    elif highest_score >= 4:

        confidence = "High"

    elif highest_score >= 2:

        confidence = "Medium"

    else:

        confidence = "Low"

    # Ubuntu Detection

    if (
        ssh_banner
        and "ubuntu" in ssh_banner.lower()
    ) or (
        http_banner
        and "ubuntu" in http_banner.lower()
    ):

        likely_os = "Ubuntu Linux"

    # Report

    print("=" * 40)
    print("      OS FINGERPRINT REPORT")
    print("=" * 40)

    print(f"\nTarget: {target}")

    print(f"\nTTL Value: {ttl}")
    print(f"TCP Window Size: {window}")

    print("\nTCP Options:")

    if options:

        for option in options:
            print(f"  {option}")

    else:

        print("  None")

    if icmp_data:

        print("\nICMP Analysis")
        print("-------------")

        print(
            f"ICMP TTL: {icmp_data['ttl']}"
        )

        print(
            f"ICMP Type: {icmp_data['type']}"
        )

        print(
            f"ICMP Code: {icmp_data['code']}"
        )
    print("\nPacket Signature Analysis:")
    print("--------------------------")
    if packet_signatures:

        signature_str = ", ".join(packet_signatures)
        print(f"TCP Options Signature: {signature_str}")

    else:

        print("No TCP options detected.")
    
    if len(packet_signatures) >= 4:

        signature_strength = "Strong"
    elif len(packet_signatures) >= 2:

        signature_strength = "Moderate"
    else:
        signature_strength = "Weak"
    print(f"Fingerprint Strength: {signature_strength}")

    print("\nEvidence:")

    for item in evidence:
        print(f"✓ {item}")

    print("\nScores:")
    print(f"Linux/Unix: {linux_score}")
    print(f"Windows: {windows_score}")
    print(
        f"Network Device: {network_device_score}"
    )

    print("\nLikely Operating System:")
    print(likely_os)

    print(f"\nConfidence: {confidence}")

    print("\nFingerprinting Complete.")