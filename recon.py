from scans import null_scan


def display_menu():

    print("\n" + "=" * 40)
    print("      RED RECON FRAMEWORK")
    print("=" * 40)

    print("1. TCP Connect Scan")
    print("2. SYN Scan")
    print("3. ACK Scan")
    print("4. FIN Scan")
    print("5. XMAS Scan")
    print("6. UDP Scan")
    print("7. OS Fingerprint")
    print("8. NULL Scan")
    print("9. Exit")

    print("=" * 40)


while True:

    display_menu()

    choice = input("Choose option: ")

    if choice == "1":
        from scans import tcp_connect
        tcp_connect.run()

    elif choice == "2":
        from scans import syn_scan
        syn_scan.run()

    elif choice == "3":
        from scans import ack_scan
        ack_scan.run()

    elif choice == "4":
        from scans import fin_scan
        fin_scan.run()

    elif choice == "5":
        from scans import xmas_scan
        xmas_scan.run()

    elif choice == "6":
        from scans import udp_scan
        udp_scan.run()

    elif choice == "7":
        from fingerprint import os_fingerprint
        os_fingerprint.run()

    elif choice == "8":
        from scans import null_scan
        null_scan.run()

    elif choice == "9":
        print("\nExiting Red Recon Framework...")
        break

    else:
        print("\nInvalid choice.")