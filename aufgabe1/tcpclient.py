import socket

serverName = socket.gethostname()
serverPort = 12000

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

clientSocket = socket.socket(IPv4, TCP)
clientSocket.connect((serverName, serverPort))

uname = input("enter a Username: ")
clientSocket.send(uname.encode())

while True:	
	message = input("{}: ".format(uname))
	clientSocket.send(message.encode())

	reply = clientSocket.recv(1024)
	print("From Server: {}".format(reply.decode()))

clientSocket.close()
