import socket

serverName = socket.gethostname()
# I'm connecting to my own computer, so I wrote down my hostname, which is debian-x220. I could have also written
# 127.0.0.1 down

serverPort = 12000 #completely arbitrary, could have been anything really

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM
clientSocket = socket.socket(IPv4, UDP) # note that we are not specifying the port number when we create it, we are letting the OS create it for us

# now the door has been created!

message = input("Write something cool: ")

clientSocket.sendto(message.encode(), (serverName, serverPort)) # remember, the port number and IP of the client host is needed here, but it is done automatically!

reply,ignoreme = clientSocket.recvfrom(2048) #2048 is the buffer size. At most 2048 bytes from the reply will be read

print(reply.decode())

clientSocket.close() 
