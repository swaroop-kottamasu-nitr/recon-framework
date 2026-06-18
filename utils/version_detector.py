import socket


def detect_version(target, port):

    try:

        s = socket.socket()
        s.settimeout(3)

        s.connect((target, port))

        if port in [80, 8080]:

            s.send(
                b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n"
            )

        banner = s.recv(4096).decode(
            errors="ignore"
        )

        s.close()

        return banner.strip()

    except:

        return None