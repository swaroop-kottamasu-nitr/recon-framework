import socket

def scan_port(t, p):
    s = socket.socket()
    s.settimeout(2)

    result = s.connect_ex((t, p))

    s.close()

    return result == 0
