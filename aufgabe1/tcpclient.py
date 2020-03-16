import socket, select, sys

serverName = socket.gethostname()
serverPort = 12000

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

clientSocket = socket.socket(IPv4, TCP)
clientSocket.connect((serverName, serverPort))

uname = input("enter a Username: ")
clientSocket.send(uname.encode())

things_we_are_going_to_read = [clientSocket, sys.stdin]
things_we_are_going_to_write = [clientSocket]
things_we_might_error_on = [clientSocket, sys.stdin]

partner_uname = "SERVER"

while True:	
	read_input, _, exceptions = select.select(things_we_are_going_to_read, things_we_are_going_to_write, things_we_might_error_on)

	for notified_input in read_input:
		if notified_input == sys.stdin:
			toSend = sys.stdin.readline().strip()
			clientSocket.send(toSend.encode())

		if notified_input == clientSocket:
			recieved_message = clientSocket.recv(1024).decode()
			print("{}: {}".format(partner_uname, recieved_message))


	#message = input("{}: ".format(uname))
	#clientSocket.send(message.encode())

	#reply = clientSocket.recv(1024)
	#print("From Server: {}".format(reply.decode()))

clientSocket.close()
