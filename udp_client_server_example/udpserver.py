import socket

serverPort = 12000

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

serverSocket = socket.socket(IPv4, UDP)

serverSocket.bind(("", serverPort)) #assigns the server socket the port 12000
print("Server is ready to recieve")

while True:
	message, clientAddress = serverSocket.recvfrom(2048) #recieve up to 2048 bytes from anyone that sends a message to us
	reply = message.decode().upper() # as a reply to the client we return their message in uppercase
	print("Recieved the following message: ") 
	print(message.decode())
	serverSocket.sendto(reply.encode(), clientAddress)
