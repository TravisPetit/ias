import socket
import select
import sys

serverPort = 1234

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

socket = socket.socket(IPv4, UDP)
socket.bind(("localhost", serverPort))
print("Server is ready to receive")

while True:
    read_input, _, _ = select.select([socket, sys.stdin], [], [])
    for notified_input in read_input:
        if notified_input == socket:
            data, clt_addr = socket.recvfrom(2048)
            print("{} has joined the unicast server:".format(clt_addr))
            toSend = "Available Chat Rooms: Room 1 , Room 2 , Room 3"
            socket.sendto(toSend.encode(), clt_addr)
