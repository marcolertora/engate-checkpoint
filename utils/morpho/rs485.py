import sys
import socket
import struct

class ILV:

    class COMMAND:
        CMD_GET_VERSION = '\x03'
        CMD_PING = '\x08'
        CMD_REBOOT = '\x04'

    @staticmethod
    def buildPacket(command, payload=''):
        data = command + struct.pack('>h', len(payload)) + payload
        return data 


class MA5G:

    PREFIX = '\x4d\x41'

    @staticmethod
    def CRC(data):
        t = 0
        for c in data:
            b, = struct.unpack('>b', c)
            t = t + b
        return ((~t) + 1)

    @staticmethod
    def buildPacket(netid, command, payload=''):
        data = ILV.buildPacket(command, payload)
        data = data.decode('hex')
        return MA5G.PREFIX + struct.pack('>hih', netid, MA5G.CRC(data), len(data)) + data


if __name__ == '__main__':

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    NETID = 1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    def command(s, data):
        print '>>>>>', data.encode('hex')
        s.send(data)
        data = s.recv(1024)
        print '<<<<<', data.encode('hex'), data
        return data

    command(s, MA5G.buildPacket(NETID, ILV.COMMAND.CMD_REBOOT))

    s.close()
