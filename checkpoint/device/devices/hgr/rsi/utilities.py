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


from struct import pack, unpack

__all__ = ['wiegand', 'mk_wiegand', 'hex2str', 'hex2str_p', 'str2hex', 'byte2value', 'value2short_le', 'short_le2value',
           'int_le2value', 'cstring']


def wiegand(data):
    assert len(data) == 4, 'len %d' % len(data)
    value = unpack('>I', data)[0]
    return int((value >> 7) & 0xffff)


def mk_wiegand(user_id):
    value = (user_id << 7) | 0x80000040
    return pack('>I', value)


def hex2str(data):
    return data.encode('hex').upper()


def hex2str_p(data):
    return ' '.join(map(lambda x: x.encode('hex').upper(), data))


def str2hex(data):
    return data.decode('hex')


def byte2value(number):
    assert 0 <= number <= 255
    return chr(number)


def value2short_le(number):
    assert 0 <= number <= 65535
    return pack('<H', number)


def short_le2value(data):
    assert len(data) == 2
    return unpack('<H', data)[0]


def int_le2value(data):
    assert len(data) == 4
    return unpack('<I', data)[0]


def cstring(data):
    return data.split('\x00')[0]
