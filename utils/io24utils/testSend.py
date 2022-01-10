#!/usr/bin/env python
import sys

if len(sys.argv)>1:
    val = pow(2,  int(sys.argv[1]))
else:
    val = '\x40'

from socket import *
t = socket(AF_INET, SOCK_DGRAM)
t.sendto('!A%c' % val, ('localhost', 2424))

