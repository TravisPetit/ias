import socket, select, sys

serverIP = "localhost"
serverPort = 1234

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM
clientSocket = socket.socket(IPv4, UDP)

peerIP = ""
peerPort = ""

username = input("Choose a username: ")
partnerUsername = input("Enter partner's username: ")
clientSocket.sendto((username + " " + partnerUsername).encode(), (serverIP, serverPort))
partnerFound = False

while True:

    read_input, _, _ = select.select([clientSocket, sys.stdin], [], [], 1)

    for notified_input in read_input:

        if notified_input == sys.stdin and not partnerFound: #send message to server
            toSend = sys.stdin.readline()
            clientSocket.sendto(toSend.encode(), (serverIP, serverPort))

        elif notified_input == sys.stdin and partnerFound: #send message to partner
            toSend = sys.stdin.readline()
            clientSocket.sendto(toSend.encode(), (peerIP, peerPort))

        elif notified_input == clientSocket and not partnerFound: #recieve message from server
            recieved_message = clientSocket.recv(1024)
            recieved_message = recieved_message.decode()
            print("Your partner {} wants to chat: ".format(recieved_message))
            if ("Your partner hasn't connected yet, please wait..." != recieved_message): #your partner is already waiting for you
                peerInfos = recieved_message.split()
                peerIP = peerInfos[0] #user saves infos about the partner
                peerPort = int(peerInfos[1])
                partnerFound = True
            # else: the user will be saved in requests list by the server

        elif notified_input == clientSocket and partnerFound: #partner already found, msg from partner
            recieved_message = clientSocket.recv(1024)
            recieved_message = recieved_message.decode()
            print("{}: {}".format(partnerUsername, recieved_message))

clientSocket.close()