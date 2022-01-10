import socket, sys

hostname = sys.argv[1].strip()
port = 2424
pin = int(sys.argv[2].strip())
module = 'A'

host = socket.gethostbyname(hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = chr(0x2a) + module + chr(0)
s.sendto(message, (host, port))
message = chr(0x2a) + module + chr(pow(2, pin))
s.sendto(message, (host, port))
message = chr(0x2a) + module + chr(0)
s.sendto(message, (host, port))
