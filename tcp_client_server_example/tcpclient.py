import socket

serverName = socket.gethostname()
serverPort = 12000

IPv4 = socket.AF_INET
TCP = socket.SOCK_STREAM

clientSocket = socket.socket(IPv4, TCP)
clientSocket.connect((serverName, serverPort))

# again, we are not binding the socket to any port, we could do it but we are letting the OS do it for us

message = input("write something: ")
clientSocket.send(message.encode())

reply = clientSocket.recv(1024)
print("From Server: {}".format(reply.decode()))

clientSocket.close()
