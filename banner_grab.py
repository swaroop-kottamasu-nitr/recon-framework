import socket

def grab_banner(t, p):
    try:
        s = socket.socket()
        s.settimeout(0.2)

        s.connect((t, p))

        if p == 80:
            request = (
                b"GET / HTTP/1.1\r\n"
                b"Host: localhost\r\n"
                b"Connection: close\r\n\r\n"
            )

            s.send(request)

        banner = s.recv(1024)

        s.close()

        return banner.decode(errors="ignore")

    except:
        return "No banner received"