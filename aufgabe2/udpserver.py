import socket

serverPort = 12000

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

serverSocket = socket.socket(IPv4, UDP)

serverSocket.bind(("", serverPort))
print("Server is ready to recieve")

users = []

def sendUserList(address, users, socket):
	message  = "###MESSAGE FROM SERVER###\n"
	message += "Here are the following users you can chat with: \n"
	for i in range(len(users)):
		message += "{} : {}\n".format(i, users[i][0])
	message += "Reply with the index of the user you want to chat with or reply with NO if you don't want to chat with anyone"
	socket.sendto(message.encode(), address)

def getReply(name, address, users, socket):
	message, _ = serverSocket.recvfrom(2048)
	try:
		usr = users[int(message.decode().strip())]
		print("Setting up a connection between {} and {}".format(name, usr[1]))
		#mssg = "Setting up a connection between you and {}.".format(usr[1])
		socket.sendto(str(usr).encode(), address)
		return True
	except:
		print("{} doesn't want to chat with anyone :(".format(name))
		mssg = "###MESSAGE FROM SERVER###\n"
		mssg += "It appears that you don't want to chat with anyone, fine."
		socket.sendto(mssg.encode(), address)
		return False

while True:
	userName, userAddress = serverSocket.recvfrom(2048) #recieve up to 2048 bytes from anyone that sends a message to us
	userName = userName.decode()
	users.append((userName, userAddress))

	print("User {} with address {} connected to the server!".format(userName, userAddress))
	print("Offering {} to establish a connection with someone ...".format(userName))

	sendUserList(userAddress, users, serverSocket)
	getReply(userName, userAddress, users, serverSocket)

	#serverSocket.sendto(reply.encode(), clientAddress)
