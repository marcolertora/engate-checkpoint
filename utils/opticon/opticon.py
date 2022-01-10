#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Opticon Barcode Configurator
#
# Copyright (c) 2010-2011 Marco Lertora <marco.lertora@infoporto.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

import sys
import time
import socket

READ_TIMEOUT = 2
WRITE_TIMEOUT = 0.1

def hex2print(data):
    return ' '.join(('0x%02X' % x) for x in data)

def hex2str(data):
    return ''.join(chr(x) for x in data)

def write(data):
    for char in data:
        s.send(chr(char))
        #time.sleep(WRITE_TIMEOUT)
    print '>> %s' % hex2print(data)

def read():
    data = []
    while True:
        try: data.append(ord(s.recv(1)))
        except socket.timeout: break

    print '<< %d: %s' % (len(data), hex2print(data))
    print repr(hex2str(data))
    return hex2str(data).replace('\r', '\r\n')

def do(data):
    data = [ord(x) for x in data.strip()]
    write([0x1B] + data + [0x0D])
    print read()

if __name__ == '__main__':


    actions = {
        'config'    : 'Z3',
        'version'   : 'Z1',
        'goodbeep'  : 'B',
        'errorbeep' : 'E',
        'setprefix' : 'RY9A$29G', #   CodeType#CodeLength#Code
        'setsuffix' : 'RZ9G$31M',
        'defaults'  : 'U2',
        'store'     : 'Z2',
        'read'      : '',
        'command'   : '',
    }

    port = 4002
    params = ''

    if len(sys.argv) < 3: sys.exit('usage barcode.py host[:port] action [param]')

    host = sys.argv[1].strip().lower()
    action = sys.argv[2].strip().lower()
    param = (len(sys.argv) > 3) and sys.argv[3].strip().lower() or ''

    if ':' in host:
        host, port = host.split(':', 1)
        try: port = int(port)
        except ValueError: sys.exit('invalid port')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    if READ_TIMEOUT: s.settimeout(READ_TIMEOUT)

    if action not in actions.keys():
        sys.exit('invalid action: %s\nactions: %s' % (action, ', '.join(actions.keys())))

    command = actions[action]
    if not command:
        if action in ['command']:
            if not param: sys.exit('this action need param')
            command = param

    do(command)
    s.close()
