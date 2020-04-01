import socket
import struct
import select
import sys

blue = '\033[94m'
green = '\033[92m'
endcolor = '\033[0m'

unicast_addr = input("Enter unicast host ip addr: ")
uname = input("Enter username: ")
unicast_port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Connecting to server ...")

s.sendto(uname.encode(), (unicast_addr, unicast_port))
mssg, server = s.recvfrom(2048)
print(blue + "### MSSG FROM SERVER ###")
print(mssg.decode() + endcolor)

server_nr = input("Enter server nr: ")
s.sendto(server_nr.encode(), server)
server_ip, _ = s.recvfrom(2048) # obtain ip
server_ip = server_ip.decode()
server_port, _ = s.recvfrom(2048) # obtain port
server_port = int(server_port.decode())

s.close()
print("Joining Multicast chat room on addr {} and port {} ...".format(server_ip, server_port))

message = 'very important data'
multicast_group = (server_ip, server_port)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(5)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment. Again, in binary:

ttl = struct.pack('b', 1)
# at the IP level, set the time to live option to ttl
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

#sock.bind(("", server_port))
#sock.bind(multicast_group)

try:
	while True:
		read_input,_,_ = select.select([sys.stdin, sock], [sock], [sys.stdin, sock])
		for notified_input in read_input:
			if notified_input == sys.stdin:
				toSend = sys.stdin.readline().strip()
				sock.sendto(toSend.encode(), multicast_group)
			if notified_input == sock:
				mssg, _ = sock.recvfrom(2048)
				print(mssg.decode())

finally:
    print('closing socket')
    sock.close()
