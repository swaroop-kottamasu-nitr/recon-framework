def run():
    print("Starting TCP Connect Scan...\n")
    import socket

    def scan_port(t, p):
        s = socket.socket()
        s.settimeout(2)

        result = s.connect_ex((t, p))

        s.close()

        return result == 0
    t = (input("\nTarget IP Address: "))
    p = int(input("\nRequired Port To Connect: "))
    scan_port(t, p)