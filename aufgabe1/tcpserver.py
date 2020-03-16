import socket

serverPort = 12000

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

serverSocket = socket.socket(IPv4, TCP)
serverSocket.bind(("", serverPort))

serverSocket.listen(1) # set the maximum number of queued connections requests to 1 i.e. only 1 client can connect at the time

my_uname = input("Enter a username: ")

connectionSocket, addr = serverSocket.accept() # create the third socket, the tunnel for connecting with the client

print("Someboy connected!")

partner_uname = connectionSocket.recv(1024).decode()

print("It's {}".format(partner_uname))

while True:
	message = connectionSocket.recv(1024).decode()
	print("{}: {}".format(partner_uname, message))
	reply = input("{}: ".format(my_uname))
	connectionSocket.send(reply.encode())

connectionSocket.close()
