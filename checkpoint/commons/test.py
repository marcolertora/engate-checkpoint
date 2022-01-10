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


from identifiers import MRZ, Badge, Person, Plate, Barcode

if __name__ == '__main__':
    a = MRZ('P<GBRUK<SPECIMEN<<ANGELA<ZOE<<<<<<<<<<<<<<<<\r9250764733GBR8809117F2007162<<<<<<<<<<<<<<08\r', score=10)
    b = Badge('2800A5DF46', 'ISO-14443-A')
    c = Badge('2800A5DF46', 'EM-4X02')
    d = Person(100)
    e = Plate('DF314EN', 'IT')
    f = Barcode('12345678', 'EAN-8')
