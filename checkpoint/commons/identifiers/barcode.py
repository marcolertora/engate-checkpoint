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

from exceptions import IdentifierException
from identifier import Identifier


class Barcode(Identifier):

    code_types = ['EAN-8', 'EAN-13', 'UPC-A', 'UPC-E', 'CODE-39', 'CODE-128', 'DATAMATRIX']

    def parse_code(self, raw_code, code_type):
        if code_type == 'EAN-8':
            if len(raw_code) != 8:
                raise IdentifierException('invalid code length')
            return raw_code[:-1]

        if code_type == 'EAN-13':
            if len(raw_code) != 13:
                raise IdentifierException('invalid code length')
            return raw_code[:-1]

        if code_type == 'UPC-A':
            return raw_code[:-1]

        if code_type == 'UPC-E':
            return raw_code[:-1]

        if code_type == 'CODE-39':
            return raw_code[:-1]

        if code_type == 'CODE-128':
            return raw_code[:-1]

        if code_type == 'DATAMATRIX':
            return raw_code

        raise IdentifierException('invalid code type: {0}'.format(code_type))
