import socket, select, sys

blue = '\033[94m'
green = '\033[92m'
endcolor = '\033[0m'

#serverName = socket.gethostname()
serverName = sys.argv[1]

serverPort = 12000
chatPort = 1234

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM
clientSocket = socket.socket(IPv4, UDP)

username = input("Choose a username: ")

def connect(serverReply):
	clientSocket = socket.socket(IPv4, UDP)
	clientSocket.bind(("", chatPort))

	if serverReply[0] != "(":
		print("Waiting for someone to start a chat with you ...")
		partner_uname, partner = clientSocket.recvfrom(2048)
		print("Someone wants to chat!")
		partnerAddress = partner[0]
		print(partnerAddress)
		partnerPort = int(partner[1])
		partnerName = partner_uname.decode()

	else:
		partnerName = serverReply[2:].split("'")[0]
		partnerAddress = serverReply[2:].split("'")[2]
		partnerPort = int(serverReply[2:].split("'")[3][2:-2])
		clientSocket.sendto(username.encode(), (partnerAddress, chatPort))

	print("Connecting to {} with address {} on the port {}".format(partnerName, partnerAddress, partnerPort))

	things_we_are_going_to_read = [clientSocket, sys.stdin]
	things_we_are_going_to_write = [clientSocket]
	things_we_might_error_on = [clientSocket, sys.stdin]

	while True:
		read_input,_,_ = select.select(things_we_are_going_to_read, things_we_are_going_to_write, things_we_might_error_on)

		for notified_input in read_input:
			if notified_input == sys.stdin:
				toSend = sys.stdin.readline().strip()
				clientSocket.sendto(toSend.encode(), (partnerAddress, chatPort))

			if notified_input == clientSocket:
				recieved_message, _ = clientSocket.recvfrom(1024)
				recieved_message = recieved_message.decode()
				print(blue + "{}: {}".format(partnerName, recieved_message) + endcolor)

		

clientSocket.sendto(username.encode(), (serverName, serverPort))

reply,_ = clientSocket.recvfrom(2048)
print(reply.decode())

mssg = input("Write a reply: ")
clientSocket.sendto(mssg.encode(), (serverName, serverPort))

serverReply, _ = clientSocket.recvfrom(2048)
serverReply = serverReply.decode()

print(serverReply)

connect(serverReply)

clientSocket.close()
