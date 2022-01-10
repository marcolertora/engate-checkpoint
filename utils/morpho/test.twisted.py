#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./gen-py.twisted/')

from Generic_types.ttypes import *
from Generic_types.ttypes import *
from Biofinger_types.ttypes import *
from Generic_commands import Generic_commands


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator

from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

class CustomThriftClientProtocol(TTwisted.ThriftClientProtocol):

    def dataReceived(self, data):
        self.stringReceived(data)

    def sendString(self, string):
        self.transport.write(string)


@inlineCallbacks
def actions(conn):
    ret = yield conn.client.terminal_get_version(0)
    print ret
    ret = yield conn.client.terminal_get_version(0)
    print ret
    #ret = yield conn.client.terminal_reboot()
    #print ret
    #ret = yield conn.client.retrieve_keypad_input(0)
    #print str(ret)
    coords = XY_coordinates(x=0, y=0)
    ret = yield conn.client.display_text('prova', coords, 10)
    print ret
    ret = yield conn.client.cls_get_info(20)
    print str(ret)
    reactor.stop()


HOST = '192.168.123.210'
PORT = 11010

if __name__ == '__main__':
    d = ClientCreator(reactor,
                      CustomThriftClientProtocol,
                      Generic_commands.Client,
                      TBinaryProtocol.TBinaryProtocolFactory(),
                      ).connectTCP(HOST, PORT)
    d.addCallback(actions)
    reactor.run()
