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
from helpers import class_repr, class_str


class Identifier(object):
    __slots__ = ['raw_code', 'code', 'code_type', 'code_types']

    code_types = list()

    def __init__(self, raw_code, code_type=None):
        self.raw_code = raw_code
        self.code_type = code_type

        if self.code_types and self.code_type not in self.code_types:
            raise IdentifierException('unknown code type: {0}'.format(code_type))

        self.code = self.parse_code(raw_code, code_type)

    def __repr__(self):
        return class_repr(self, code=self.code)

    def __str__(self):
        return class_str(self, self.code)

    def parse_code(self, raw_code, code_type):
        return raw_code

