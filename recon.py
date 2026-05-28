import socket
t="45.33.32.156"      # Target IP address
p=[22 , 80 , 443]     # List of ports to scan(ssh,http,https)
def grab_banner(target,port):     # Function to grab banner information from a specific port
    
    try:
        s=socket.socket()
        s.settimeout(3)
        s.connect((target,port))
        if port == 80:
            request = b"GET / HTTP/1.1\r\nHost: scanme.nmap.org\r\nConnection: close\r\n\r\n"
            s.send(request)
        banner = s.recv(1024)
        return banner.decode(errors='ignore')      # Decode the banner information, ignoring any decoding errors
    except :
        return "No banner received"
    finally:
        s.close()

for port in p:
    s=socket.socket()
    s.settimeout(3)
    res=s.connect_ex((t,port))
    if res == 0:
        print(f"\n[+] Port {port} is OPEN")
        banner = grab_banner(t,port)             # Grab the banner information for the open port
        print(f"Banner for port {port}: {banner}")
    s.close()
