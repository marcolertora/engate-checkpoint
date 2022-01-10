#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Software Controllo Accessi
#
# Copyright (c) 2010 Netfarm S.r.l.
# Gianluigi Tiesi <sherpya@netfarm.it>
# Alfredo Oliviero <alfredo.oliviero@netfarm.it>
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
# ======================================================================

def hex2str_p(bytes):
    return ' '.join(map(lambda x: '0x%02x' % ord(x), bytes))

if __name__ == '__main__':
    from socket import * 
    s = socket(AF_INET, SOCK_DGRAM)
    addr =  ('192.168.69.80', 2424)
    for i in range(5, 25):
        s.sendto("'R%c\x00\x00" % chr(i), addr)
        data = s.recv(4)[2:]
        print i, hex2str_p(data), map(ord, data)
