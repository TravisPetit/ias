import socket, select, sys

blue = '\033[94m'
green = '\033[92m'
endcolor = '\033[0m'

try:
	serverName = sys.argv[0]
	serverPort = int(sys.argv[1])
except:
	print("Invalid command line arguments, using stdin instead...")
	try:
		serverName = input(green + "IP address: " + endcolor)
		serverPort = int(input(green + "Port Number: " + endcolor))
	except:
		print("Bad input, falling back to default mode ...")
		serverName = socket.gethostname()
		serverPort = 12001

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

clientSocket = socket.socket(IPv4, TCP)
clientSocket.connect((serverName, serverPort))

my_uname = input(green + "Enter a username: " + endcolor)
clientSocket.send(my_uname.encode())

things_we_are_going_to_read = [clientSocket, sys.stdin]
things_we_are_going_to_write = [clientSocket]
things_we_might_error_on = [clientSocket, sys.stdin]

partner_uname = clientSocket.recv(1024).decode()
print("Connected to {}".format(partner_uname))

while True:	
	read_input, _, exceptions = select.select(things_we_are_going_to_read, things_we_are_going_to_write, things_we_might_error_on)

	for notified_input in read_input:
		if notified_input == sys.stdin:
			toSend = sys.stdin.readline().strip()
			clientSocket.send(toSend.encode())

		if notified_input == clientSocket:
			recieved_message = clientSocket.recv(1024).decode()
			print(blue + "{}: {}".format(partner_uname, recieved_message) + endcolor)

clientSocket.close()
