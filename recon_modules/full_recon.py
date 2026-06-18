from scans.syn_scan import scan_target
from utils.service_enum import enumerate_service
from fingerprint.os_fingerprint import fingerprint_target

def run():
    print("=" * 50)
    print("         FULL RECON REPORT")
    print("=" * 50)
    target = input(
        "Enter target IP: "
    )
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))
    print(f"\nTarget: {target}")
    print(
        "\nRunning Full Recon...\n"
    )

    open_ports = scan_target(
        target,
        start_port,
        end_port
    )

    print("\nOpen Ports")
    print("-"*20)

    for port in open_ports:

        result = enumerate_service(
            target,
            port
        )

        print(f"\n[{port}/tcp]")

        print(
            f"Service: "
            f"{result['service']}"
        )

        if result["banner"]:

            banner = result["banner"]

            first_line = banner.split("\n")[0]

            print(
                f"Version: "
                f"{first_line}"
            )

        else:

            print(
                "Version: Unknown"
            )
    os_result = fingerprint_target(target, open_ports)
    print("\nOS FINGERPRINT")
    print("--------------")
    print(f"Likely OS: {os_result['os']}")
    print(f"Confidence: {os_result['confidence']}")
    print(f"TTL : {os_result['ttl']}")
    print(f"TCP Window Size: {os_result['window']}")
    print("\n Evidence:")
    for item in os_result['evidence']:
        print(f"✓ {item}")
    print("\n" + "=" * 50)
    print("Recon Complete")
    print("=" * 50)