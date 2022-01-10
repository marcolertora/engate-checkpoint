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
from exceptions import IdentifierException
from identifier import Identifier


class MRZ(Identifier):

    __slots__ = Identifier.__slots__ + ['document_class', 'document_sub_class', 'document_country',
                                        'last_name', 'first_name', 'document_number', 'nationality',
                                        'birthday_date', 'gender', 'document_expiration_date', 'personal_number',
                                        'optional_data' 'application_number']

    DOCUMENT_CLASS = Namespace(PASSPORT=('P',), TRAVEL_DOCUMENT=('I', 'A', 'C'), VISA=('V', ))
    CODE = Namespace(FILLER='<', SEPARATOR='<<', CR='\x0D')

    @staticmethod
    def to_str(value):
        value = value.replace(MRZ.CODE.FILLER, ' ')
        value = value.strip()
        return value

    @staticmethod
    def to_datetime(value):
        value = MRZ.to_str(value)
        try:
            return datetime.strptime(value, '%y%m%d').date()
        except ValueError:
            raise IdentifierException('invalid date: {0}'.format(value))

    @staticmethod
    def verify_check_digit(data, check):
        assert check.isdigit(), 'invalid check digit'
        check = int(check) if check != MRZ.CODE.FILLER else 0
        if MRZ.calculate_check_digit(data) != check:
            raise IdentifierException('check digit mismatch {0}'.format(data))

    @staticmethod
    def calculate_check_digit(data):
        total = 0
        weights = [7, 3, 1]

        for pos in range(len(data)):
            char = data[pos]
            weight = weights[pos % len(weights)]

            if 48 <= ord(char) <= 57:
                total += (ord(char) - 48) * weight
                continue

            if 65 <= ord(char) <= 90:
                total += (ord(char) - 55) * weight
                continue

            if char == MRZ.CODE.FILLER:
                continue

            raise IdentifierException('invalid char in mrz: {0}'.format(char))

        return total % 10

    def __init__(self, raw_code, code_type=None, score=None):
        super(MRZ, self).__init__(raw_code, code_type)
        self.score = score
        self.document_class = None
        self.document_sub_class = None
        self.document_country = None
        self.last_name = None
        self.first_name = None
        self.document_number = None
        self.nationality = None
        self.birthday_date = None
        self.gender = None
        self.document_expiration_date = None
        self.personal_number = None
        self.optional_data = None
        self.application_number = None

    def parse_code(self, raw_code, code_type):
        rows = raw_code.split(MRZ.CODE.CR)
        self.document_class = rows[0][0]
        self.document_sub_class = MRZ.to_str(rows[0][1])
        self.document_country = MRZ.to_str(rows[0][2:5])

        # this is a passport
        if self.document_class in MRZ.DOCUMENT_CLASS.PASSPORT:
            MRZ.verify_check_digit(rows[1][13:19], rows[1][19])
            MRZ.verify_check_digit(rows[1][21:27], rows[1][27])
            MRZ.verify_check_digit(rows[1][28:42], rows[1][42])
            MRZ.verify_check_digit(rows[1][0:10] + rows[1][13:20] + rows[1][21:43], rows[1][43])
            MRZ.verify_check_digit(rows[1][0:9], rows[1][9])

            last_name, first_name = rows[0][5:].split(MRZ.CODE.SEPARATOR, 1)
            self.last_name = MRZ.to_str(last_name)
            self.first_name = MRZ.to_str(first_name)
            self.document_number = MRZ.to_str(rows[1][0:9])
            self.nationality = MRZ.to_str(rows[1][10:13])
            self.birthday_date = MRZ.to_datetime(rows[1][13:19])
            self.gender = MRZ.to_str(rows[1][20])
            self.document_expiration_date = MRZ.to_datetime(rows[1][21:27])
            self.personal_number = MRZ.to_str(rows[1][28:42])
            return

        # this is a travel document
        if self.document_class in MRZ.DOCUMENT_CLASS.TRAVEL_DOCUMENT:
            MRZ.verify_check_digit(rows[0][5:14], rows[0][14])
            MRZ.verify_check_digit(rows[1][0:6], rows[1][6])
            MRZ.verify_check_digit(rows[1][8:14], rows[1][14])
            MRZ.verify_check_digit(rows[0][5:] + rows[1][0:7] + rows[1][8:15] + rows[1][15:29], rows[1][29])

            last_name, first_name = rows[2][0:].split(MRZ.CODE.SEPARATOR, 1)
            self.last_name = MRZ.to_str(last_name)
            self.first_name = MRZ.to_str(first_name)
            self.document_number = MRZ.to_str(rows[0][5:14])
            self.optional_data = MRZ.to_str(rows[0][15:])
            self.birthday_date = MRZ.to_datetime(rows[1][0:6])
            self.gender = MRZ.to_str(rows[1][7])
            self.document_expiration_date = MRZ.to_datetime(rows[1][8:14])
            self.application_number = MRZ.to_str(rows[1][15:29])
            return

        raise IdentifierException('invalid document class in mrz: {0}'.format(self.document_class))
