import socket, select, sys

#def recieve_message(client_scoket):
#	try:
#		message_header = client_socket.recv(10) #10 is the header length
#
#		if no len(message_header):
#			return False
#
#		message_length = int(message_header.decode().strip())
#		return {"header": message_header, "data": client_socket.recv(len(message_header))}
#
#	except:
#		return False

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

things_we_are_going_to_read = [connectionSocket, sys.stdin]
things_we_are_going_to_write = [connectionSocket]
things_we_might_error_on = [connectionSocket, sys.stdin]

while True:
	read_input, _, exceptions = select.select(things_we_are_going_to_read, things_we_are_going_to_write, things_we_might_error_on)

	for notified_input in read_input:
		if notified_input == sys.stdin:
			toSend = sys.stdin.readline().strip().encode()
			connectionSocket.send(toSend)

		if notified_input == connectionSocket:
			recieved_message = connectionSocket.recv(1024).decode()
			print("{}: {}".format(partner_uname, recieved_message))

	#message = connectionSocket.recv(1024).decode()
	#print("{}: {}".format(partner_uname, message))
	#reply = input("{}: ".format(my_uname))
	#connectionSocket.send(reply.encode())

connectionSocket.close()
