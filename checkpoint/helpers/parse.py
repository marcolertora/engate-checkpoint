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


def fixed_unpack(data, fields):
    pos = 0
    values = dict()
    length = sum(field_size for field_name, field_size in fields)

    if len(data) < length:
        raise ValueError('too short: wanted {wanted} got {got}'.format(wanted=length, got=len(data)))

    for field_name, field_size in fields:
        value = data[pos:pos + field_size]
        values[field_name] = value.strip()
        pos += field_size

    return data[pos:], values


def fixed_pack(values, fields, separator=''):
    data = list()
    for field_name, field_size in fields:
        value = values.get(field_name, '')
        assert isinstance(value, str), 'value should be string'
        data.append(value[:field_size].rjust(field_size))
    return separator.join(data)
