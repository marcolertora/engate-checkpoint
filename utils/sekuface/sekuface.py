#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Copyright (c) 2013 Netfarm S.r.l. Marco Lertora <marco.lertora@infoporto.it>
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

import sys
import xmlrpclib

URL = sys.argv[1]
VERBOSE = 0

if __name__ == '__main__': 

    sf = xmlrpclib.ServerProxy(URL, verbose=VERBOSE)

    def enrollBiometric():
        username = 'Marco Lertora'
        try:
            res = sf.enrollBiometric(username)
            print 'bioTemplate', res['bioTemplate'].data
            print 'imageStream', res['imageStream'].data
            print 'imageContentType', res['imageContentType']
        except xmlrpclib.Fault, e:
            print 'xmlrpc error: [%d] %s' % (e.faultCode, e.faultString)

    def verifyBiometric():
        username = 'Marco Lertora'
        bioTemplate = xmlrpclib.Binary('Prova Byte Array')
        res = sf.verifyBiometric(bioTemplate, username)
        print 'score', res['score']
        print 'imageStream', res['imageStream'].data
        print 'imageContentType', res['imageContentType']

    def showMessage():
        color = 'FF0000'
        message = 'Prova messaggio'
        res = sf.showMessage(message, color)
        print 'ret', res

    def getStatus():
        res = sf.getStatus()
        print res['version']
        print res['status']


    #enrollBiometric()
    #verifyBiometric()
    #showMessage()
    getStatus()
