import socket
target = "45.33.32.156"      # Target IP address
port = 80                     # Port to scan

s=socket.socket()
s.settimeout(5)
s.connect((target,port))

request = b"GET / HTTP/1.1\r\nHost: scanme.nmap.org\r\nConnection: close\r\n\r\n"
s.send(request)
response = s.recv(4096)         # Receive the response from the server (up to 4096 bytes)
print(response.decode(errors='ignore'))     # Decode the response, ignoring any decoding errors
s.close()
