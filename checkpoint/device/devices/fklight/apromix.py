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
from commons.identifiers import Badge
from device.protocols.exceptions import InvalidPacket


class APROMIX:

    UID_size = 10
    UID_type = 'EM-4X02'

    STX = chr(0x02)
    ETX = chr(0x03)
    EOT = chr(0x04)
    ACK = chr(0x06)

    class EXIT:
        OK, NONEXISTENT_COMMAND, DATAFORMAT_ERROR, UNKNOWN1, UNKNOWN2, BCC_ERROR, INVALID_COMMAND = xrange(7)

        desc = ['ok',
                'unknown command',
                'invalid data format',
                'unknown 01',
                'unknown 02',
                'wrong bcc'
                'invalid command in this operating mode (TMAC)'
                ]

        @staticmethod
        def to_str(e):
            return APROMIX.EXIT.desc[e]

    class REQUEST:
        SETUP = '1'
        FIRMWARE_VERSION = '2'
        READ = '3'
        FIRST_MATRICOLA = '4'
        MATRICOLA_CORRENTE = '5'
        NEXT_MATRICOLA = '6'
        ESISTENZA_MATRICOLA = '7'

    class REPLY:
        ACK, EXIT, NO_BADGE, BADGE_READY, BADGE, FIRMWARE_VERSION, SETUP = xrange(7)

    GLOBAL_ADDRESS = '\x60\x60'

    @staticmethod
    def calculate_bcc(payload):
        bcc = 0
        for v in payload:
            bcc ^= ord(v)
        return bcc

    @staticmethod
    def addr2bytes(address, selecting=True):
        # ottiene i 2 byte che indicano l'indirizzo
        # usare 0 per indirizzo broadcast
        # selecting True per un comando di selecting, False per polling

        if address == 0:
            return APROMIX.GLOBAL_ADDRESS

        if not 0 < address <= 255:
            raise ValueError('Address must be >= 0 and <= 255')

        # 54 => hex(54) => 36 => 3, 6 => (selecting: 33, 36 - polling: 33, 26)
        first, second = divmod(address, 0x10)
        first += 0x30
        second += 0x30 if selecting else 0x20
        return chr(first) + chr(second)

    @staticmethod
    def bytes2addr(address):
        selecting = False

        if address == APROMIX.GLOBAL_ADDRESS:
            return 0, True

        first, second = ord(address[0]), ord(address[1])

        if not 0x30 <= first <= 0x3f:
            ValueError('Invalid address first byte')

        first -= 0x30

        if 0x20 <= second <= 0x2f:
            selecting = False
            second -= 0x20
        elif 0x30 <= second <= 0x3f:
            selecting = True
            second -= 0x30
        else:
            ValueError('Invalid second address byte')

        address = (first << 0x10) | second

        return address, selecting

    @staticmethod
    def buildPacket(address, payload, selecting=True):
        packet = APROMIX.STX
        packet += APROMIX.addr2bytes(address, selecting)
        packet += payload
        packet += APROMIX.ETX
        return APROMIX.EOT + APROMIX.EOT + packet + chr(APROMIX.calculate_bcc(packet))

    @staticmethod
    def Request(address, code, selecting=False):
        return APROMIX.buildPacket(address, code, selecting)

    @staticmethod
    def Setup(tproto=10, rele=0, tmcode=50, tbuzz=10, tmac=7, led_v=1, ttag='U', tinp=0, mimp=0):
        conf = '1'

        if not 0 <= tproto <= 5999:  # 0 disabled
            raise ValueError('tproto should be >= 0 and <= 5900')
        conf += '%04d' % tproto

        if not ((0 <= rele <= 900) or (rele == 999)):
            raise ValueError('rele should be >= 1 and <= 900, or 999')
        conf += '%03d' % rele

        if not 0 <= tmcode <= 999:
            raise ValueError('tmcode should be >= 0 and <= 999')
        conf += '%03d' % tmcode

        if not ((1 <= tbuzz <= 900) or (tbuzz == 999)):
            raise ValueError('tbuzz should be >= 1 and <= 900, or 999')
        conf += '%03d' % tbuzz

        if not 0 <= tmac <= 7:
            raise ValueError('tmac should be >= 0 and <= 7')
        conf += str(tmac)

        if tmac == 7 and not (1 <= tproto <= 10):
            raise ValueError('tproto should be >=1 and <=10 if tmac is 7')

        if led_v not in (0, 1, 2):
            raise ValueError('led_v should be 0, 1 or 2')
        conf += str(led_v)

        # if ttag not in ('U', 'T', 'Z', 'h', 'H'):
        #     raise ValueError('ttag should be H, T, Z, h, or H')
        # conf += ttag

        # type of the transponder (reader)
        # 'U' EM-4x02 (default) (10 chars)
        # 'T' EM-4x50 (8 chars)
        # 'Z' ISO-FDXB (EM-4x05) (16 chars)
        # 'h' Hitag 1 (8 chars)
        # 'H' Hitag 2 (8 chars)

        # if tinp not in (0, 1):
        #     raise ValueError('tinp should be 0 or 1')
        # conf += str(tinp)

        # if mimp not in (0, 1, 2, 3, 4):
        #     raise ValueError('mimp should be 0, 1, 2, 3 or 4')
        # conf += str(mimp)

        return conf

    @staticmethod
    def SetSetup(address, tproto=10, rele=0, tmcode=50, tbuzz=10, tmac=7, led_v=1, ttag='U', tinp=0, mimp=0):
        payload = APROMIX.Setup(tproto, rele, tmcode, tbuzz, tmac, led_v, ttag, tinp, mimp)
        return APROMIX.buildPacket(address, payload, selecting=True)

    @staticmethod
    def SetSetupSeriale(address, new_address, baud_rate=9600):
        baud_rates = [1200, 2400, 4800, 9600, 19200, 38400]

        if baud_rate not in baud_rates:
            raise ValueError('invalid baud rate')

        payload = '2'
        payload += APROMIX.addr2bytes(new_address)
        payload += str(baud_rates.index(baud_rate))

        return APROMIX.buildPacket(address, payload, selecting=True)

    @staticmethod
    def Acknowledgment(address):
        return APROMIX.buildPacket(address, APROMIX.ACK, selecting=False)

    @staticmethod
    def SetOutput(address, relay=None, buzzer=None, led=None):
        relay = relay if relay is not None else 901
        buzzer = buzzer if buzzer is not None else 901
        led = led if led is not None else 901

        if not 0 <= relay <= 999:
            raise ValueError('relay should be >= 0 and <= 999')
        if not 0 <= buzzer <= 999:
            raise ValueError('buzzer should be >= 0 and <= 999')
        if not 0 <= led <= 999:
            raise ValueError('led should be >= 0 and <= 999')

        payload = '3'
        payload += '%03d%03d%03d' % (relay, buzzer, led)
        return APROMIX.buildPacket(address, payload, selecting=True)

    @staticmethod
    def parsePacket(data):
        bcc = ord(data[-1])
        cbcc = APROMIX.calculate_bcc(data[:-1])
        if bcc != cbcc:
            raise InvalidPacket('wrong BCC 0x%02x instead of 0x%02x' % (bcc, cbcc))

        # STX + packet + ETX + BCC
        data = data[1:-2]
        address, selecting = APROMIX.bytes2addr(data[:2])
        data = data[2:]

        psize = len(data)

        if selecting:
            if psize != 1:
                raise InvalidPacket('invalid Exit packet len')

            try:
                code = int(data[0])
                if not (0 <= code <= 6):
                    raise ValueError
            except ValueError:
                raise InvalidPacket('invalid Exit code')

            return APROMIX.REPLY.EXIT, address, code

        # Polling
        reply = data[0]

        if reply == 'N':
            return APROMIX.REPLY.NO_BADGE, address, None

        elif reply == 'P':
            data = data[1:]
            if len(data) % APROMIX.UID_size != 0:
                raise InvalidPacket('badge size(s) mismatch')

            badges = []
            while len(data) > 0:
                uid = data[:APROMIX.UID_size]
                data = data[APROMIX.UID_size:]
                badges.append(Badge(uid, code_type=APROMIX.UID_type))

            return APROMIX.REPLY.BADGE, address, badges

        elif reply == '3':
            raise InvalidPacket('unknown packet code 3')

        elif psize == 15:
            tproto = data[:4]
            data = data[4:]
            rele = data[:3]
            data = data[3:]
            tmcode = data[:3]
            data = data[3:]
            tbuzz = data[:3]
            data = data[3:]
            tmac = data[0]
            data = data[1:]
            led_v = data[0]

            try:
                (tproto, rele, tmcode, tbuzz, tmac, led_v) = map(int, (tproto, rele, tmcode, tbuzz, tmac, led_v))
            except ValueError:
                raise InvalidPacket('invalid setup')

            setup = dict(tproto=tproto, rele=rele, tmcode=tmcode, tbuzz=tbuzz, tmac=tmac, led_v=led_v)
            return APROMIX.REPLY.SETUP, address, setup

        elif psize == 16:
            return APROMIX.REPLY.FIRMWARE_VERSION, address, data

        raise InvalidPacket('unknown packet type')

    @staticmethod
    def parsePackets(data):
        data = data.lstrip(APROMIX.EOT)
        # split on start_packet_char
        packets = data.split(APROMIX.STX)[1:]
        return map(lambda packet: APROMIX.parsePacket(APROMIX.STX + packet), packets)
