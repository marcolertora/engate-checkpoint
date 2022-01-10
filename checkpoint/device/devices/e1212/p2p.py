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

import struct
from argparse import Namespace
from device.protocols.exceptions import InvalidPacket, IncompletePacket


class P2P(object):
    MAGIC = '\x50\x32\x50\x3f\x11\x00'
    MESSAGE_TYPE = Namespace(HEART_BEAT=0, MASK=1)

    @staticmethod
    def one_byte_crc(payload):
        return reduce(lambda x, y: (x + ord(y)) % 256, payload, 0)

    @staticmethod
    def parse_packets(data):
        packets = []
        while len(data) > 0:
            result, data = P2P.parse_packet(data)
            packets.append(result)

        return packets

    @staticmethod
    def parse_packet(data):
        header_length = struct.calcsize('<6sBH')

        if len(data) < header_length:
            raise IncompletePacket('packet too short')

        magic, message_type, payload_length, = struct.unpack_from('<6sBH', data)

        if magic != P2P.MAGIC:
            raise InvalidPacket('invalid packet magic')

        message_length = header_length + payload_length
        if len(data) < message_length:
            raise IncompletePacket('invalid message length')

        message = data[:message_length]

        crc, = struct.unpack('<B', message[-1])
        computed_crc = P2P.one_byte_crc(message[:-1])

        if computed_crc != crc:
            raise InvalidPacket('wrong crc wanted {0}, got {1}'.format(hex(computed_crc), hex(crc)))

        if message_type == P2P.MESSAGE_TYPE.MASK:
            mask, _, _, value, heart_beat = struct.unpack_from('<HHHHH', message, offset=header_length)
            bit_mask = map(lambda x: bool(value & pow(2, x)) if bool(mask & pow(2, x)) else None, range(16))
            return (message_type, bit_mask), data[message_length:]

        elif message_type == P2P.MESSAGE_TYPE.HEART_BEAT:
            heart_beat = struct.unpack_from('<H', message, offset=header_length)
            return (message_type, heart_beat), data[message_length:]

        raise InvalidPacket('unknown message type {0}'.format(message_type))
