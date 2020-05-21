import socket, select, sys

serverPort = 1234

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

socket = socket.socket(IPv4, UDP)

socket.bind(("localhost", serverPort))
print("Server is ready to recieve")

#requestsList = []
users = []

while True:
	name, addr = socket.recvfrom(1024) # the first mssg from the user to the server will be the user's name
	print("{} connected to the server!".format(name.decode()))

	users.append((name.decode(), addr[0])) #add the username and ip to the userlist

	s = "### MESSAGE FROM SERVER ###\nThe avaliable users are:\n"
	for i in range(len(users)):
		s += "{}: {}\n".format(i, users[i])
	socket.sendto(s.encode(), addr) # reply with the user list

	reply, _ = socket.recvfrom(1024) # the user will have replied with either an index or NO

	if reply.decode() == "NO":
		print("{} will wail for someone to start chatting with them".format(name.decode()))

	else:
		mssg = users[int(reply.decode())] # the user at the index that the clinet selected
		mssg = str(mssg)
		mssg = mssg.encode()

		socket.sendto(mssg, addr)
	

#while True:
#
#	read_input, _, _= select.select([socket, sys.stdin], [], [])
#
#	for notified_input in read_input:
#
#		if notified_input == socket: #new client
#			found = False
#			userInfos = []
#			userData, userAddress = notified_input.recvfrom(1024)
#			(userIP, userPort) = userAddress
#			userInfos.append(userIP)  # userinfos = [userIP]
#			userInfos.append(userPort)  # connectioninfos = [userIP, userPort]
#			messageList = userData.decode().split()
#			userInfos.append(messageList[0])  # userinfos = [userIP, userPort, own username]
#			userInfos.append(messageList[1])  # userinfos = [userIP, userPort, own username, partner username]
#			# connectionInfos->#0: own IP, 1: own Port, 2: own username, 3: partner username
#
#			print("Client Port: ", userPort) #new client connected
#
#			for i in requestsList:
#				if userInfos[3] == i[2] and not found:  # partnerusername == (username)already in users
#					# send infos to clients->send ip and port to both
#					socket.sendto((userIP + ' ' + str(userPort)).encode(), (i[0], i[1]))
#					socket.sendto((i[0] + ' ' + str(i[1])).encode(), (userIP, userPort))
#					requestsList.remove(i)
#					#while true!
#					found = True
#
#			#first request
#			if not found:
#				requestsList.append(userInfos)  # saves infos about new client and his peer if request from peer exists
#				socket.sendto(("Your partner hasn't connected yet, please wait...").encode(), (userIP, userPort))
#
#
#socket.close()
