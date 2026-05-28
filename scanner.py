import socket
t=("45.33.32.156") #target ip address
p=[22, 80, 443] #ports
for port in p:
	s=socket.socket()
	s.settimeout(2)
	r=s.connect_ex((t,port))
	if r == 0:
		print(f"Port {port} is OPEN")
	else:
		print(f"Port {port} is closed")
	s.close()
