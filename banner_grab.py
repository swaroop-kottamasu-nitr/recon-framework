import socket
target = "45.33.32.156"
port = 80

s=socket.socket()
s.settimeout(5)
s.connect((target,port))

request = b"GET / HTTP/1.1\r\nHost: scanme.nmap.org\r\nConnection: close\r\n\r\n"
s.send(request)
response = s.recv(4096)
print(response.decode(errors='ignore'))
s.close()
