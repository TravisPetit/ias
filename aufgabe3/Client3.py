import socket, select, struct, sys

blue = '\033[94m'
green = '\033[92m'
endcolor = '\033[0m'

groups = []

class Address:
    def __init__(self, multicast_ip, port):
        self.ip = multicast_ip
        self.port = ("", port)


serverIP = "localhost"
serverPort = 1234

IPv4 = socket.AF_INET
UDP = socket.SOCK_DGRAM
clientSocket = socket.socket(IPv4, UDP)

key = input(blue + "Press any key to connect to the main server: " + endcolor)

clientSocket.sendto(key.encode(), (serverIP, serverPort))
data = clientSocket.recv(2048)
print(green + data.decode() + endcolor)

for i in range(0, 3):
    groups.append(Address("224.3.29.{}".format(70 + i), 10000 + i))


def getServer():
    room = int(input("Enter room number: "))
    if room == 1:
        addr = groups[0].ip
        port = groups[0].port[1]
    elif room == 2:
        addr = groups[1].ip
        port = groups[1].port[1]

    elif room == 3:
        addr = groups[2].ip
        port = groups[2].port[1]
    else:
        sys.exit("Chat Room " + str(room) + " is not a invalid")
    return addr, port


uname = input("Enter username: ")
multicast_addr, multicast_port = getServer()

sockin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(multicast_addr, multicast_port)
sockin.bind((multicast_addr, multicast_port))
mreq = struct.pack('4sL', socket.inet_aton(multicast_addr), socket.INADDR_ANY)
sockin.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

sockout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockout.settimeout(5)
ttl = struct.pack('b', 1)
sockout.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

while True:
    read_input, _, _ = select.select([sockin, sys.stdin], [], [])
    for notified_input in read_input:
        if notified_input == sockin:
            data = sockin.recv(1024)
            if data: print(data.decode())
            else:
                sockin.close()
                sys.exit("Disconnected from server.")
        else:
            toSend = sys.stdin.readline()
            if not toSend.isspace():
                sockout.sendto(uname.encode() + ": ".encode() + toSend.encode(), (multicast_addr, multicast_port))
