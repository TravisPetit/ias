import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)


# Tell the operating system to add the socket to the multicast group
# on all interfaces:

# converts the group address into binary
group_in_byte_format = socket.inet_aton(multicast_group) 

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


# Receive/respond loop
while True:
    print("waiting to receive message")
    data, address = sock.recvfrom(1024)
    
    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    print('sending acknowledgement to {}'.format(address))
    sock.sendto('ack'.encode(), address)
