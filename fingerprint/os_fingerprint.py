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

def fingerprint_target(target, open_ports=None):



    print("\nFingerprinting Target...\n")
    fingerprint_port = 80
    if open_ports:
        fingerprint_port = open_ports[0]
    packet = IP(dst=target) / TCP(
        dport=fingerprint_port,
        flags="S"
    )

    response = sr1(
        packet,
        timeout=2,
        verbose=0
    )

    if not response or not response.haslayer(TCP):
        print("No response received.")
        return {
            "os": "Unknown",
            "confidence": "Low",
            "ttl": None,
            "window": None,
            "options": [],
            "icmp": None,
            "evidence": ["No TCP fingerprint response received."],
            "scores": {
                "Linux/Unix": 0,
                "Windows": 0,
                "Network Device": 0
            }
        }

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
    if highest_score == 0:

        likely_os = "Unknown"
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
    return {
        "os": likely_os,
        "confidence": confidence,
        "ttl": ttl,
        "window": window,
        "options": option_names,
        "icmp": icmp_data,
        "evidence": evidence,
        "scores": scores
    }

def run():

    target = input("Enter target IP: ")

    result = fingerprint_target(target)

    print("\n" + "=" * 40)
    print("      OS FINGERPRINT REPORT")
    print("=" * 40)

    print(f"\nTarget: {target}")

    if result["ttl"] is not None:

        print(f"\nTTL Value: {result['ttl']}")
        print(f"TCP Window Size: {result['window']}")

    else:

        print("\nTCP Fingerprint Data Unavailable")
    print("\nTCP Options:")

    if result["options"]:

        for option in result["options"]:

            print(f"  {option}")

    else:

        print("  None")

    if result["icmp"]:

        print("\nICMP Analysis")
        print("-------------")

        print(
            f"ICMP TTL: "
            f"{result['icmp']['ttl']}"
        )

        print(
            f"ICMP Type: "
            f"{result['icmp']['type']}"
        )

        print(
            f"ICMP Code: "
            f"{result['icmp']['code']}"
        )

    print("\nEvidence:")

    for item in result["evidence"]:

        print(f"✓ {item}")

    print("\nScores:")

    for os_name, score in result["scores"].items():

        print(
            f"{os_name}: {score}"
        )

    print("\nLikely Operating System:")
    print(result["os"])

    print(
        f"\nConfidence: "
        f"{result['confidence']}"
    )

    print("\nFingerprinting Complete.")