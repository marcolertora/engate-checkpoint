from socket import * 
addr = ('172.16.50.81',  2424, )
s = socket(AF_INET, SOCK_DGRAM)
import time

def send(porta):
    print getporta(porta)
    pkt = 'A%s' % getporta(porta)
    s.sendto(pkt, addr)
    print repr(pkt)
    time.sleep(0.5)
    s.sendto('A\x00', addr)

def getporta(x):
    return pow(2,x)


send(5)
