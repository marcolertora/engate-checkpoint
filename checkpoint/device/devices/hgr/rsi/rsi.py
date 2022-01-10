#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# engate-checkpoint
#
# Copyright (C) 2018 Marco Lertora <marco.lertora@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from argparse import Namespace
from crc import CRC
from device.protocols.exceptions import IncompletePacket, InvalidPacket
from utilities import value2short_le, byte2value, mk_wiegand, wiegand, short_le2value, cstring
from utilities import int_le2value, hex2str_p, str2hex, hex2str
from status import Status
from types import IntType, StringType
from datetime import datetime

models = {0: 'HP-2000', 1: 'HP-3000', 2: 'HP-4000', 3: 'HK-CR', 4: 'HK-2'}
memory = {0: 128, 1: 256, 2: 640}
prefix = {0: '', 1: 'E6-', 2: 'E6HP-'}
me = {0: 'No adaptor', 1: 'Modem', 2: 'Ethernet'}

hostcmd = {
    'Resume': {'nargs': 0, 'op': 0x31, 'len': 0, 'reply': 'HereIsStatus', 'handler': ()},
    'Abort': {'nargs': 0, 'op': 0x32, 'len': 0, 'reply': 'HereIsStatus', 'handler': ()},
    'SendUserRecord': {'nargs': 1, 'op': 0x38, 'len': 5, 'reply': 'HereIsUserRecord',
                       'handler': (('usertohp', IntType),)},
    'SendLastUserRecord': {'nargs': 0, 'op': 0x40, 'len': 0, 'reply': 'HereIsUserRecord', 'handler': ()},
    'SendResults': {'nargs': 0, 'op': 0x43, 'len': 0, 'reply': 'HereAreResults', 'handler': ()},
    'SendStatusCRC': {'nargs': 0, 'op': 0x44, 'len': 0, 'reply': 'HereIsStatus', 'handler': ()},
    'EnterIdleMode': {'nargs': 0, 'op': 0x45, 'len': 0, 'reply': 'HereIsStatus', 'handler': ()},
    'EnrollUser': {'nargs': 1, 'op': 0x49, 'len': 2, 'reply': 'HereIsStatus', 'handler': (('prompt', IntType),)},
    'VerifyOnExternalData': {'nargs': 2, 'op': 0x4a, 'len': 11, 'reply': 'HereIsStatus',
                             'handler': (('prompt', IntType), ('template', StringType))},
    'SendTemplate': {'nargs': 0, 'op': 0x4b, 'len': 0, 'reply': 'HereIsTemplate', 'handler': ()},
    'SendSetup': {'nargs': 0, 'op': 0x4e, 'len': 0, 'reply': 'HereIsSetupData', 'handler': ()},
    'SendTimeAndDate': {'nargs': 0, 'op': 0x61, 'len': 0, 'reply': 'HereIsTimeAndDate', 'handler': ()},
    'Beep': {'nargs': 2, 'op': 0x62, 'len': 2, 'reply': 'HereIsStatus',
             'handler': (('bytevalue', IntType), ('bytevalue', IntType))},
    'SendCardData': {'nargs': 0, 'op': 0x67, 'len': 0, 'reply': 'HereIsCardData', 'handler': ()},
    'SendOEMCode': {'nargs': 0, 'op': 0x6f, 'len': 0, 'reply': 'HereIsOEMCode', 'handler': ()},
    'SendReaderInfo': {'nargs': 0, 'op': 0x73, 'len': 0, 'reply': 'HereIsReaderInfo', 'handler': ()},

    'HereIsStatus': {'nargs': 1, 'op': 0x30, 'len': 3, 'reply': None, 'handler': (('status', Status),)},
    'HereIsCardData': {'nargs': 2, 'op': 0x34, 'len': 4, 'reply': None,
                       'handler': (('status', Status), ('userid', IntType))},
    'HereAreResults': {'nargs': 2, 'op': 0x35, 'len': 7, 'reply': None,
                       'handler': (('usertohp', IntType), ('score', IntType))},
    'HereIsTemplate': {'nargs': 2, 'op': 0x37, 'len': 11, 'reply': None,
                       'handler': (('score', IntType), ('template', StringType))},
}

unitcmd = {
    'SendResults': {'len': 0, 'op': 0x43, 'parser': 'null'},
    'SendStatusCRC': {'len': 0, 'op': 0x44, 'parser': 'null'},
    'VerifyOnExternalData': {'len': 2, 'op': 0x4a, 'parser': 'extdata'},
    'SendTemplate': {'len': 0, 'op': 0x4b, 'parser': 'null'},
    'SendCardData': {'len': 0, 'op': 0x67, 'parser': 'null'},

    'HereIsStatus': {'len': 3, 'op': 0x30, 'parser': 'status'},
    'HereIsUserRecord': {'len': 16, 'op': 0x32, 'parser': 'userrecord'},
    'HereIsCardData': {'len': 4, 'op': 0x34, 'parser': 'carddata'},
    'HereAreResults': {'len': 7, 'op': 0x35, 'parser': 'results'},
    'HereIsTemplate': {'len': 11, 'op': 0x37, 'parser': 'template'},
    'HereIsSetupData': {'len': 128, 'op': 0x39, 'parser': 'setupdata'},
    'HereIsOEMCode': {'len': 2, 'op': 0x4f, 'parser': 'oemcode'},
    'HereIsReaderInfo': {'len': 102, 'op': 0x53, 'parser': 'readerinfo'},
    'HereIsTimeAndDate': {'len': 6, 'op': 0x61, 'parser': 'timedate'},
}

# Reverse map of reply packets
msgmap = {}
for key, value in unitcmd.items():
    entry = dict(command=key)
    entry.update(value)
    msgmap[value['op']] = entry


class RSI(object):
    NULL = '\x00'
    HDR = '\xFF\x0A'
    EOT = '\xFF'

    # score range is 0-250 and 0 is perfect match
    SCORE = Namespace(MIN=0, MAX=250)

    def __init__(self, unit=0):
        self.__unit = chr(unit)

    def makepacket(self, op, payload=''):
        packet = self.__unit + chr(op) + chr(len(payload)) + payload
        return RSI.HDR + packet + CRC(packet).digest()

    # Command codes
    @staticmethod
    def getop(command):
        cmd = unitcmd.get(command, None)
        assert cmd is not None
        return cmd['op']

    # Handlers
    @staticmethod
    def _h_usertohp(userid):
        """code of userid for rsi box: 12345678 -> 0x12 0x34 0x56 0x78"""
        assert 0 <= userid < 65535
        return str2hex('%010d' % userid)

    @staticmethod
    def _h_hptouser(userid):
        return hex2str(userid)

    @staticmethod
    def _h_template(template):
        assert len(template) == 9 * 2
        return str2hex(template)

    @staticmethod
    def _h_score(score):
        return value2short_le(score)

    @staticmethod
    def _h_prompt(prompt):
        return value2short_le(prompt)

    @staticmethod
    def _h_bytevalue(number):
        return byte2value(number)

    @staticmethod
    def _h_status(status):
        return status.serialize()

    @staticmethod
    def _h_userid(user_id):
        if user_id == -1:
            return RSI.NULL

        assert 0 < user_id < 65535
        # data len 26
        return '\x1a' + mk_wiegand(user_id)

    # Parsers
    @staticmethod
    def _p_carddata(data):
        status = Status(data[:3])
        data_len = ord(data[3])
        data = data[4:]

        if data_len == 0:
            user_id = -1
        elif data_len == 26:
            user_id = wiegand(data)
        else:
            raise InvalidPacket('CardData: Wrong data len %d' % data_len)

        return dict(status=status, userid=user_id)

    @staticmethod
    def _p_userrecord(data):
        try:
            user_id = int(hex2str(data[:5]))
        except ValueError, e:
            raise InvalidPacket('Results: %s' % e.message)
        data = data[5:]
        template = hex2str(data[:9])
        data = data[9:]
        authority = ord(data[0])
        timezone = ord(data[1])
        return dict(userid=user_id, template=template, authority=authority, timezone=timezone)

    @staticmethod
    def _p_oemcode(data):
        return dict(oemcode=short_le2value(data[:2]))

    @staticmethod
    def _p_template(data):
        score = short_le2value(data[:2])
        data = data[2:]
        template = hex2str(data)
        return dict(score=score, template=template)

    @staticmethod
    def _p_setupdata(data):
        return dict(setupdata=hex2str(data))

    @staticmethod
    def _p_results(data):
        try:
            user_id = int(hex2str(data[:5]))
        except ValueError, e:
            raise InvalidPacket('Results: %s' % e.message)
        data = data[5:]
        score = short_le2value(data)
        return dict(score=score, userid=user_id)

    @staticmethod
    def _p_status(data):
        return dict(status=Status(data))

    @staticmethod
    def _p_timedate(data):
        date = map(ord, data)
        date.reverse()
        date[0] += 2000
        try:
            return dict(datetime=datetime(*date))
        except ValueError:
            raise InvalidPacket('Wrong TimeDate')

    @staticmethod
    def _p_readerinfo(data):
        results = {'model': models.get(ord(data[0]), 'Unknown')}
        data = data[1:]
        results['memory'] = memory.get(ord(data[0]), -1)
        data = data[1:]
        results['promdate'] = cstring(data[:20])
        data = data[20:]
        results['modelname'] = cstring(data[:17])
        data = data[17:]
        results['sn'] = int_le2value(data[:4])
        data = data[4:]
        results['snprefix'] = prefix.get(ord(data[0]), 'Unknown')
        data = data[1:]
        results['ucap'] = short_le2value(data[:2])
        data = data[2:]
        results['tcap'] = short_le2value(data[:2])
        data = data[2:]
        results['unum'] = short_le2value(data[:2])
        data = data[2:]
        results['tnum'] = short_le2value(data[:2])
        data = data[2:]
        results['config'] = cstring(data[:14])
        data = data[14:]
        results['me'] = me.get(ord(data[0]), 'Unknown')
        data = data[1:]
        results['altprom'] = ord(data[0])
        # data = data[1:]
        # results['reserved'] = hex2str(data)
        return results

    @staticmethod
    def _p_extdata(data):
        prompt = short_le2value(data[:2])
        template = hex2str(data[2:11])
        return dict(prompt=prompt, template=template)

    @staticmethod
    def _p_null(data):
        return dict()

    def makecmd(self, cmd, *kw):
        assert cmd['nargs'] == len(kw)
        payload = ''
        for arg, hd in zip(kw, cmd['handler']):
            assert type(arg) == hd[1], '%s <> %s' % (type(arg), hd[1])
            handler = getattr(RSI, '_h_' + hd[0], None)
            assert handler is not None, hd[0]
            payload += handler(arg)
        return self.makepacket(cmd['op'], payload)

    @staticmethod
    def parsePacket(data):
        crclength = 2
        headerlength = 3
        prefixlength = len(RSI.HDR)
        suffixlength = len(RSI.EOT)
        packetlength = prefixlength + headerlength + crclength + suffixlength

        if len(data) < packetlength:
            raise IncompletePacket('Invalid length got %d wanted at least %d' % (len(data), packetlength))

        if not data.startswith(RSI.HDR):
            raise InvalidPacket('Wrong start of packet')

        unit = ord(data[2])
        cmdid = ord(data[3])
        payloadlength = ord(data[4])
        packetlength += payloadlength

        cmd = msgmap.get(cmdid)

        if not cmd:
            raise InvalidPacket('Unknown command: %s' % hex2str_p(cmdid))

        if payloadlength != cmd['len']:
            raise InvalidPacket('Invalid length reported %d defined %d' % (payloadlength, cmd['len']))

        if len(data) < packetlength:
            raise IncompletePacket('Invalid length got %d wanted %d' % (len(data), packetlength))

        if data[packetlength - suffixlength] != RSI.EOT:
            raise InvalidPacket('Wrong end of packet')

        crc = data[packetlength - crclength - suffixlength:packetlength - suffixlength]
        payload = data[prefixlength:prefixlength + headerlength + payloadlength]

        mycrc = CRC(payload).digest()
        if crc != mycrc:
            raise InvalidPacket('Wrong CRC %s != %s' % (hex2str_p(crc), hex2str_p(mycrc)))

        parser = getattr(RSI, '_p_' + cmd['parser'])
        assert parser is not None, 'missing parser for: %s' % hex2str_p(cmdid)
        result = parser(payload[headerlength:])
        result.update(dict(command=cmd['command']))
        return data[packetlength:], result

    @staticmethod
    def parsePackets(data):
        packets = []
        while len(data):
            data, packet = RSI.parsePacket(data)
            packets.append(packet)

        assert not len(data), 'should be empty'
        return packets

    def __getattr__(self, attr):
        def command(*kw):
            # Commands
            cmd = hostcmd.get(attr)
            assert cmd is not None, 'Unknown command %s' % attr
            return self.makecmd(cmd, *kw)

        return command
