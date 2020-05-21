import socket, select, sys

def wait_for_someone_to_chat_with_me(sock):
	#sock.bind(("",???)) # or maybe create a new socket
	print("Okay then, waiting for someone to chat with you ...")
	partner_uname, partnerAddr = clientSocket.recv(1024) # the partner's first mssg will be their name
	partner_uname = partner_uname.decode()
	print("{} wants to chat! Say hi!".format(partner_uname))

	# start chatting
	try:
		while True:
			read_input, _, _ = select.select([sock, sys.stdin], [], [], 1)

			for notified_input in read_input:
				if notified_input == sys.stdin:
					toSend = sys.stdin.readline()
					sock.sendto(toSend.encode(), partnerAddr)

				elif notified_input ==  sock:
					recieved_message, _ = clientSocket.recv(1024)
					print("{}: {}".format(partner_uname, recieved_message.decode()))
	except:
		print("closing socket ...")
		sock.close() #always close your sockets!

def start_a_chat_with(sock, partner_name, ip, my_name):
	changeME = 1234 #??? maybe also create a new socket here
	sock.sendto(my_name.encode(), (ip, changeME)) # first we send our username

	# then we chat
	try:
		while True:
			read_input, _, _ = select.select([sock, sys.stdin], [], [], 1)

			for notified_input in read_input:
				if notified_input == sys.stdin:
					toSend = sys.stdin.readline()
					sock.sendto(toSend.encode(), partnerAddr)

				elif notified_input ==  sock:
					recieved_message, _ = clientSocket.recv(1024)
					print("{}: {}".format(partner_uname, recieved_message.decode()))
	except Exception as e:
		print(e)
		print("closing socket ...")
		sock.close()

serverIP = "localhost"
serverPort = 1234

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM
clientSocket = socket.socket(IPv4, UDP)

username = input("Choose a username: ")

clientSocket.sendto(username.encode(), (serverIP, serverPort)) # send name to server
users_in_server = clientSocket.recv(1024) # the server replies with all the avaliable names from the server
print(users_in_server.decode())
partner_index = input("Choose the index of the partner you may want to talk to or reply with NO: ")

if partner_index == "NO":
	clientSocket.sendto("NO".encode(), (serverIP, serverPort)) # let the server know you are a loner
	wait_for_someone_to_chat_with_me(clientSocket)

else:
	clientSocket.sendto(partner_index.encode(), (serverIP, serverPort)) # send the partner index to the server
	partner_uname_and_ip, _ = clientSocket.recvfrom(1024) # the server will reply with the partner's name and ip
	partner_uname_and_ip = partner_uname_and_ip.decode()

	# the reply will look something like this ('ben', '127.0.0.1')
	partner_uname_and_ip = partner_uname_and_ip.split(",")
	# after the split it looks like this: ('ben'   '127.0.0.1')

	partner_name = partner_uname_and_ip[0] #('ben'
	ip = partner_uname_and_ip[1] #'127.0.0.1')

	partner_name = partner_name[2:-1] # now instead of ('ben' we have ben
	ip = ip[2:-2] # same thing with ip

	start_a_chat_with(clientSocket, partner_name, ip, username)
