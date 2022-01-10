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
from datetime import datetime
from commons.identifiers import Telepass
from device.protocols.exceptions import InvalidPacket
from helpers import fixed_unpack


class MONTRAFMessage(object):
    transit = 'B1'
    life = 'B2'


class MONTRAFField(object):
    header = [('class', 2),
              ('project', 1),
              ('company', 2),
              ('gate', 5),
              ('date', 10),
              ('time', 8),
              ('id', 5),
              ('collector', 6),
              ('shift', 1),
              ('status', 1)
              ]

    transit = [('direction', 1),
               ('id', 1),
               ('out_gate', 4),
               ('in_gate', 3),
               ('in_lane', 2),
               ('in_class', 2),
               ('in_date', 10),
               ('in_time', 8),
               ('obu_code_8', 8),
               ('obu_version', 2),
               ('obu_badge_code', 20),
               ('link_id', 1),
               ('boa', 1),
               ('obu_code_20', 20),
               ]

    life = [('boa_A_status', 2),
            ('boa_B_status', 2),
            ('boa_C_status', 2),
            ('boa_D_status', 2),
            ]


class MONTRAFPush(object):

    BOA_STATUS = Namespace(
        NOT_FOUND=0,
        WORKING=1,
        DEGRADED=2,
        NOT_WORKING=3,
    )

    GOOD_BOA_STATUS = (BOA_STATUS.WORKING, BOA_STATUS.NOT_FOUND)

    STATUS = Namespace(
        WORKING_NOT_USED=0,
        WORKING_USED=1,
        DEGRADED_USED=2,
        NOT_WORKING=3,
        MAINTENANCE=4,
        EMERGENCY=5,
        DEGRADED_NOT_USED=6,
    )

    GOOD_STATUS = (STATUS.WORKING_NOT_USED, STATUS.WORKING_USED)

    @staticmethod
    def luhn_check_digit(code):
        def luhn(digit):
            return sum(divmod(digit * 2, 10))

        digits = map(int, code)
        odds, evens = digits[-2::-2], digits[-1::-2]
        total = sum(map(luhn, evens) + odds)
        check = (10 - total) % 10
        return str(check)

    @staticmethod
    def normalize_code(code):
        code, check = code[:-1], code[-1]
        try:
            # 1st encoding
            if code.isdigit():
                return str(int(code, 10)), check
            # 2nd encoding
            if code[1:].isdigit():
                return str((int(code[0], 16) * 10 ** 6) + int(code[1:], 10)), check
            # 3rd encoding
            return str(int(code, 16)), check
        except ValueError:
            raise ValueError('invalid telepass code {0} check {1}'.format(code, check))

    @staticmethod
    def map_code(value):
        code, check = MONTRAFPush.normalize_code(value)
        luhn = MONTRAFPush.luhn_check_digit(code)
        if check != luhn:
            raise ValueError('invalid code check digit {0} wanted {1} got: {2}'.format(value, luhn, check))
        return code + check

    @staticmethod
    def parse_packet_header(data):
        header = dict()
        try:
            data, values = fixed_unpack(data, MONTRAFField.header)
            header['status'] = int(values['status'])
            header['datetime'] = datetime.strptime(values['date'] + values['time'], '%Y-%m-%d%H.%M.%S')
            header['gate'] = values['gate'].upper()
            header['class'] = values['class']
        except ValueError, err:
            raise InvalidPacket('invalid header packet: {0}'.format(err))

        return data, header

    @staticmethod
    def parse_packet_transit(data, header):
        logs = []
        try:
            data, values = fixed_unpack(data, MONTRAFField.transit)
            uid = MONTRAFPush.map_code(values['obu_code_20'])
            if int(header['status']) not in MONTRAFPush.GOOD_STATUS:
                logs.append('warning status {0}'.format(header['status']))
        except ValueError, err:
            raise InvalidPacket('invalid header packet {0}'.format(err))

        return data, Telepass(uid), logs

    @staticmethod
    def parse_packet_life(data):
        logs = list()
        try:
            data, values = fixed_unpack(data, MONTRAFField.life)
            for bid in ['A', 'B', 'C', 'D']:
                status = int(values.get('boa_{0}_status'.format(bid)))
                if status not in MONTRAFPush.GOOD_BOA_STATUS:
                    logs.append('warning status {0} boa {1}'.format(status, bid))
        except ValueError, err:
            raise InvalidPacket('invalid header packet {0}'.format(err))

        return data, logs

    @staticmethod
    def parse_packets(data):
        return [MONTRAFPush.parse_packet(data)]

    @staticmethod
    def parse_packet(data):
        values = list()
        data, header = MONTRAFPush.parse_packet_header(data)
        unit = int(header['gate'])

        while len(data):
            if header['class'] == MONTRAFMessage.transit:
                data, tag, logs = MONTRAFPush.parse_packet_transit(data, header)
                values.append((unit, logs, tag))
                continue

            if header['class'] == MONTRAFMessage.life:
                data, logs = MONTRAFPush.parse_packet_life(data)
                values.append((unit, logs, None))
                continue

            raise InvalidPacket('unknown packet class {0}'.format(header['class']))

        return header['class'], values
