import socket
import select
import struct
import sys

number_servers = int(input("Enter the number of servers desired: "))

groups = []
address_sockets = []

class Address:
	def __init__(self, multicast_ip, port):
		self.ip = multicast_ip
		self.port = ("", port)


for i in range(0, number_servers):
	groups.append(Address("224.3.29.{}".format(70+i), 10000 + i))
	print("Created multicast server {} with IP: {} on port {}".format(i, groups[i].ip, groups[i].port[1]))


for addr in groups:
	# Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind to the server address
	#sock.bind(server_address)
	#sock.bind(addr.port)


	# Tell the operating system to add the socket to the multicast group
	# on all interfaces:

	# converts the group address into binary
	#group_in_byte_format = socket.inet_aton(group) 
	group_in_byte_format = socket.inet_aton(addr.ip)

	# INADDR_ANY is a constant that is equal to 0. It serves as a flag that tells the bind() function to bind a socket to
	# all possible interfaces

	# group together the group and INADDR_ANY constant and pack them together into a binary number
	# 4sl means that what we are packing are 4 strings and and unsigled long digit:
	# the four strings in this case are (I think) 224, 3, 29 and 71 and the unsigned long is just 0
	mreq = struct.pack('4sL', group_in_byte_format, socket.INADDR_ANY)


	# the first parameter tells the kernel at what level to handle this option,
	# we choose  IPPROTO_IP to handle it at the IP level, this is always the case for multicasting
	# the second parameter is the option we are setting: we want to add the socket to the multicast group so we
	# set it to IP_ADD_MEMBERSHIP
	# the third parameter is, in this case, what we want to add, why is myreq
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	sock.settimeout(1/number_servers)

	address_sockets.append((addr, sock))



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 1234))

while True:
	client_uname, client_addr = s.recvfrom(2048) #recieve clinet uname
	client_uname = client_uname.decode()
	print("{} joined the server!".format(client_uname))
	s.sendto("There are {} servers avaliable, reply with a server index".format(number_servers).encode(), client_addr)
	client_choice, _ = s.recvfrom(2048)
	print("{} server choice: {}".format(client_uname, client_choice.decode()))
	s.sendto(groups[int(client_choice.decode())].ip.encode(), client_addr) # send ip
	s.sendto(str(groups[int(client_choice.decode())].port[1]).encode(), client_addr) # send port
