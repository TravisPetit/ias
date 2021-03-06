import socket, select, sys

blue = '\033[94m'
green = '\033[92m'
endcolor = '\033[0m'


try:
	serverPort = int(sys.argv[1])
except:
	print("Invalid command line arguments, falling back to default mode ...")
	try:
		serverPort = int(input(green + "Port Number: " + endcolor))
	except:
		print("Bad input, falling back to default mode")
		serverPort = 12001

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

serverSocket = socket.socket(IPv4, TCP)
serverSocket.bind(("", serverPort))

serverSocket.listen(1) # set the maximum number of queued connections requests to 1 i.e. only 1 client can connect at the time

my_uname = input(green + "Enter a username: " + endcolor)

print("Waiting for someone to connect ...")

connectionSocket, addr = serverSocket.accept() # create the third socket, the tunnel for connecting with the client
print("Someboy connected!")

partner_uname = connectionSocket.recv(1024).decode()
print("It's {}!".format(partner_uname))
connectionSocket.send(my_uname.encode())

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
			print(blue + "{}: {}".format(partner_uname, recieved_message) + endcolor)

connectionSocket.close()
