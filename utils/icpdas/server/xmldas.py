#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# Software Controllo Accessi
#
# Copyright (c) 2013 Infoporto La Spezia S.r.l.
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

from twisted.internet import reactor
from twisted.web import xmlrpc, server
from twisted.python import log

import os
from ctypes import *

def getTopLevel():
    base = os.path.abspath(__file__)
    return os.path.dirname(base)

DASLIB = cdll.LoadLibrary(getTopLevel() + '/libUSBIO_arm.so')

class DAS:
    
    class DeviceException(Exception):
        pass

    ERRORCODES = {
        0     : 'ERR_NO_ERR',
        65536 : 'ERR_USBDEV_INVALID_DEV',
        65537 : 'ERR_USBDEV_DEV_OPENED',
        65538 : 'ERR_USBDEV_DEVNOTEXISTS',
        65539 : 'ERR_USBDEV_GETDEVINFO', 
        65540 : 'ERR_USBDEV_ERROR_PKTSIZE', 
        65541 : 'ERR_USBDEV_ERROR_WRITEFILE', 
        65542 : 'ERR_USBDEV_ERROR_OPENFILE', 
        65543 : 'ERR_USBDEV_ERROR_CreateRxThread', 
        65544 : 'ERR_USBDEV_ERROR_RestartRxThread', 
        65792 : 'ERR_USBIO_COMM_TIMEOU', 
        65793 : 'ERR_USBIO_DEV_OPENED', 
        65794 : 'ERR_USBIO_DEV_NOTOPEN', 
        65795 : 'ERR_USBIO_INVALID_RESP', 
        65796 : 'ERR_USBIO_IO_NOTSUPPORT', 
        65797 : 'ERR_USBIO_PARA_ERROR', 
        65798 : 'ERR_USBIO_BULKVALUE_ERR', 
        65799 : 'ERR_USBIO_GETDEVINFO', 
    }
 
    def __init__(self, boardid):
        self.boardid = boardid
        self.devid = c_int()
        self.numofdoport = c_ubyte()
        self.numofdiport = c_ubyte()
        self.dostate = 0
        self.distate = 0
        self.open()

    def open(self):
        self.log('Opening Device with boardId %d' % (self.boardid))
        self.checkReturn(DASLIB.USBIO_OpenDevice(c_ubyte(self.boardid), byref(self.devid)))
        self.checkReturn(DASLIB.USBIO_GetDOTotal(self.devid, byref(self.numofdoport)))
        self.checkReturn(DASLIB.USBIO_GetDITotal(self.devid, byref(self.numofdiport)))
        self.log('Total DO %d; Total DI %d' % (self.numofdoport.value, self.numofdiport.value))
        self.refreshDOPort()
        self.refreshDIPort()
        
    def close(self):
        self.log('Closing Device with boardId %d' % (self.boardId))
        self.checkReturn(DASLIB.USBIO_CloseDevice(self.devid))
        
    def checkReturn(self, errcode):
        if not errcode: return
        self.log('Command returned %d - %s' % (errcode, DAS.ERRORCODES.get(errcode)))
        raise DAS.DeviceException('%d - %s' % (errcode, DAS.ERRORCODES.get(errcode)))

    def log(self, message):
        log.msg(message)
        
    def setDOPort(self, portid, value):
        if portid not in range(self.numofdoport.value): raise DAS.DeviceException('invalid port DO portid')
        dowvalue = c_ubyte(self.calculateByteValue(portid, value))
        self.log('WriteValue DO: PortId %d PortValue %r Value 0x%X' % (portid, value, dowvalue.value))
        self.checkReturn(DASLIB.USBIO_DO_WriteValue(self.devid, byref(dowvalue)))
        self.refreshDOPort()

    def refreshDOPort(self):
        dorvalue = c_ubyte()
        self.checkReturn(DASLIB.USBIO_DO_ReadValue(self.devid, byref(dorvalue)))
        self.dostate = dorvalue.value

    def refreshDIPort(self):
        dirvalue = c_ubyte()
        self.checkReturn(DASLIB.USBIO_DI_ReadValue(self.devid, byref(dirvalue)))
        self.distate = dirvalue.value
        
    def getDOPort(self, portid):
        self.refreshDOPort()
        if portid not in range(self.numofdoport.value): raise DAS.DeviceException('invalid port DO portid')
        value = DAS.getBitValue(portid, self.dostate)
        self.log('ReadValue DO: PortId %d PortValue %r Value 0x%X' % (portid, value, self.dostate))
        return value

    def getDIPort(self, portid):
        self.refreshDIPort()
        if portid not in range(self.numofdiport.value): raise DAS.DeviceException('invalid port DI portid')
        value = DAS.getBitValue(portid, self.distate)
        self.log('ReadValue DI: PortId %d PortValue %r Value 0x%X' % (portid, value, self.distate))
        return value
        
    def calculateByteValue(self, portid, value):
        bitvalue = 0x01 << portid
        cvalue = DAS.getBitValue(portid, self.dostate)
        if cvalue == value: return self.dostate
        cstate = self.dostate ^ bitvalue
        return cstate
         
    @staticmethod
    def getBitValue(portid, value):
        return ((value >> portid) & 0x01) == 1


class XMLDAS(xmlrpc.XMLRPC):

    def __init__(self, das, **kw):
        self.das = das
        xmlrpc.XMLRPC.__init__(self, **kw)

    def xmlrpc_getPortValue(self, portgroupid, portid):
        if portgroupid == 'DI':
            return self.das.getDIPort(portid)

        if portgroupid == 'DO':
            return self.das.getDOPort(portid)

        raise xmlrpc.Fault(11, 'Invalid Port Group: %s' % portgroupid)

    def xmlrpc_setPortValue(self, portgroupid, portid, portvalue):
        if portgroupid == 'DO':
            self.das.setDOPort(portid, portvalue)
            return True

        raise xmlrpc.Fault(11, 'Invalid Port Group: %s' % portgroupid)

    def xmlrpc_keepAlive(self):
        return True


if __name__ == '__main__':
    import sys

    log.startLogging(sys.stdout, setStdout=False)
    boardid = 1
    das = DAS(boardid)
    mydas = XMLDAS(das)
    reactor.listenTCP(7080, server.Site(mydas))
    reactor.run()
