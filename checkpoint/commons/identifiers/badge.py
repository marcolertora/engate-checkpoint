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

from helpers import hex2str, msb2lsb, str2hex
from exceptions import IdentifierException
from identifier import Identifier


class Badge(Identifier):

    code_types = ['ISO-15693', 'ISO-14443-A', 'ISO-14443-B', 'EM-4X02', 'I-CODE-1', 'EPC-CLASS-1-GEN-2']

    def parse_code(self, raw_code, code_type):

        if code_type == 'EPC-CLASS-1-GEN-2':
            prefix, code = raw_code[:4], raw_code[4:]
            return code

        if code_type == 'ISO-14443-A':
            return raw_code.rjust(16, '0')

        if code_type == 'EM-4X02':
            return raw_code

        raise IdentifierException('invalid code type: {0}'.format(code_type))

    @property
    def lsb_code(self):
        if self.code_type == 'EM-4X02':
            return hex2str(msb2lsb(str2hex(self.code)))

        raise NotImplementedError
