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

import xmlrpclib
from datetime import datetime


if __name__ == '__main__':
    server = xmlrpclib.ServerProxy('http://vgate:51595716877496@localhost:9997')
    lane_id = 10
    company = dict(name='acme', type_name='vector')
    person = dict(name='akim', birth_date=datetime.now(), birth_country='IT', photo_id=10023, company=company)
    person.get('birth_date'),
    person.get('birth_country'),
    person.get('photo_id')
    operator = 'admin'
    documents = list()
    params = dict(destination='somewhere', reason='my business')
    # print 'open gate:', server.openGate(lane_id)
    print 'auth person:', server.authPerson(lane_id, person, operator, documents, params)
