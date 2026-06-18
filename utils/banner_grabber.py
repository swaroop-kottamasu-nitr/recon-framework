import socket


def get_banner(target, port):

    try:

        s = socket.socket()
        s.settimeout(2)

        s.connect((target, port))

        if port == 80:
            s.send(
                b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n"
            )

        banner = s.recv(1024).decode(
            errors="ignore"
        )

        s.close()

        return banner

    except:
        return None