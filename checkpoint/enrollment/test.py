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


if __name__ == '__main__':
    server = xmlrpclib.ServerProxy('http://127.0.0.1:9999')
    station_id = 'ENROLL'
    biometric_type_id = 'LEFT_HAND'
    template = '77867F597293876F72'.encode('base64')
    threshold = 70
    name = 'Test'
    timeout = 11
    lane_id = 1

    #print 'read badge:', server.read_badge(station_id, timeout)
    #print 'acquire biometric:', server.acquire_biometric(station_id, biometric_type_id, name)
    #print 'verify biometric:', server.verify_biometric(station_id, biometric_type_id, template, threshold, name)

    params = dict(tokenId='123', sessionId='1234', remoteUrl='http://localhost:7777/xmlrpc')
    print 'verify biometric:', server.verifyBiometric(lane_id, params, biometric_type_id, template, threshold, name)

