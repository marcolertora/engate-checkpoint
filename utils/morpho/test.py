#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./gen-py')

from Generic_types.ttypes import *
from Generic_types.ttypes import *
from Biofinger_types.ttypes import *
from Generic_commands import Generic_commands

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol, TBinaryProtocol, TJSONProtocol

HOST = '192.168.123.199'

try:
    transport = TSocket.TSocket(HOST, 11010)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = Generic_commands.Client(protocol)

    transport.open()
    print 'connected'

    if 1:
        print 'terminal_get_version'
        ret = client.terminal_get_version(0)
        print ret
    
    if 0:
        print 'keypad'
        ret = client.retrieve_keypad_input(20)
        print ret
    
    if 0:
        print 'card info'
        ret = client.cls_get_info(20)
        print ret, ret.card_info.iso14443_card.serial_number

    if 1:
        print 'retrieve peripherals'
        print client.terminal_retrieve_peripherals()
        print 'get info'
        print client.product_get_info(range(10))

    if 0:
        print 'display text'
        coordinates = XY_coordinates(x=0, y=0)
        print client.display_text('prova display', coordinates, 10)

    if 0:
        print 'biofinger_enroll'
        database = 0
        timeout = 100
        enrolltype = Enrollment_type.transfer
        numoffinger = 1
        user_id = None
        user_fields = None
        intermediate = False
        param = Biofinger_control_optional_param()
        ret = client.biofinger_enroll(database, timeout, enrolltype, numoffinger, user_id, user_fields, intermediate, param)
        print ret

    if 0:
        print 'biofinger_authenticate_ref'
        timeout = 100
        threshold = 8
        intermediate = False
        template_data = '622e00665dff8080726c616c4c96596f367d457238701e738a6c1a61bc95755b5b5ac188525b80629a5f568580893d8341a077ac887a8572899c8d8792b2277f907c919c94968a73a28fa3802b669c9b304da79c8b649c6cb58648526f65594e6b5e91636be66ddd92febfa2585432b1aaff'.decode('hex')
        template = User_templates(template_type=Biofinger_template_type.pkcompv2, template_data=template_data)
        param = Biofinger_control_optional_param(require_matching_score=True)
        ret = client.biofinger_authenticate_ref(timeout, threshold, [template], intermediate, param)
        print ret

    if 0:
        print 'terminal_reboot'
        ret = client.terminal_reboot()
        print ret

    transport.close()
    print 'closed'

except Thrift.TException, tx:
  print tx
