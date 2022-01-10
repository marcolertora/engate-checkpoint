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

import socket
import random
from datetime import datetime
from device.devices.montraf.montraf_push import MONTRAFPush, MONTRAFField, MONTRAFMessage
from helpers import fixed_pack


def get_header(packet_class, antenna):
    return {'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H.%M.%S'),
            'company': 'IP',
            'class': packet_class,
            'id': '%05d' % (random.randint(1, 10)),
            'gate': antenna,
            'status': str(MONTRAFPush.STATUS.DEGRADED_USED)}


def get_life():
    return {'boa_A_status': str(MONTRAFPush.BOA_STATUS.NOT_WORKING),
            'boa_B_status': str(MONTRAFPush.BOA_STATUS.NOT_FOUND),
            'boa_C_status': str(MONTRAFPush.BOA_STATUS.NOT_FOUND),
            'boa_D_status': str(MONTRAFPush.BOA_STATUS.NOT_FOUND)}


def get_transit(antenna, obu_code):
    return {'in_date': datetime.now().strftime('%Y-%m-%d'),
            'in_time': datetime.now().strftime('%H.%M.%S'),
            'boa': antenna,
            'obu_version': '2',
            'obu_code_8': obu_code,
            'obu_code_20': obu_code,
            'obu_badge_code': '1234'}


def make_life_packet(gate):
    h = get_header(MONTRAFMessage.life, gate)
    f = get_life()
    data = fixed_pack(h, MONTRAFField.header)
    data += fixed_pack(f, MONTRAFField.life)
    return data


def make_transit_packet(gate, antenna, obu_code, count=1):
    h = get_header(MONTRAFMessage.transit, gate)
    t = get_transit(antenna, obu_code)
    data = fixed_pack(h, MONTRAFField.header)
    for index in range(count):
        data += fixed_pack(t, MONTRAFField.transit)
    return data


if __name__ == '__main__':
    port = 4023
    host = 'localhost'

    boa_id = 'A'
    gate_id = '00002'
    uid_code = '47038180'  # '016210067'
    uid_code = uid_code + MONTRAFPush.luhn_check_digit(uid_code)
    print 'code {0} obu {1} gate {2}'.format(uid_code, boa_id, gate_id)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(make_life_packet(gate_id), (host, port))
    sock.sendto(make_transit_packet(gate_id, boa_id, uid_code, count=1), (host, port))
