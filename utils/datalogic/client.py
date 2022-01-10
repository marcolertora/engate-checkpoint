#!/usr/bin/env python

import socket

HOST = '192.168.123.26'
PORT = 4001
BUFFER_SIZE = 1024


def receive(s):
    while 1:
        data = s.recv(BUFFER_SIZE)
        print '<<< %r [%s] (%d)' % (data, data.encode('hex'), len(data))
        if not data: break
    return data

def send(s, data):
    print '>>> %r [%s] (%d)' % (data, data.encode('hex'), len(data))
    s.send(data)

if __name__ == '__main__': 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print 'socket connected: %s %d'  % (HOST, PORT)

    send(s, '\x07')
    #receive(s)
    #send(s)

    s.close()
