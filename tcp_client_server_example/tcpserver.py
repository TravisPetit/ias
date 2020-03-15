import socket

serverPort = 12000

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

serverSocket = socket.socket(IPv4, TCP)
serverSocket.bind(("", serverPort))

serverSocket.listen(1) # set the maximum number of queued connections requests to 1 i.e. only 1 client can connect at the time

print("The server is ready to recieve")

while True:
	connectionSocket, addr = serverSocket.accept() # create the third socket, the tunnel for connecting with the client
	message = connectionSocket.recv(1024).decode()
	print("Recieved: {}".format(message))
	reply = message.upper()
	connectionSocket.send(reply.encode())
	connectionSocket.close()
