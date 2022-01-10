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

from device.protocols.xmlrpc_auth_server import XMLRPCAuth


class LegacyResource(XMLRPCAuth):

    def xmlrpc_authPerson(self, lane_id, person, operator, documents, params):
        self.factory.device_log.info('received auth for {person} to lane {lane}',
                                     lane=lane_id,
                                     person=person['name'],
                                     params=params)
        self.factory.on_auth_person(lane_id, person, operator, documents, params)
        return True

    def xmlrpc_authBadge(self, lane_id, code, code_type):
        self.factory.device_log.info('received auth for badge {code} to lane {lane}',
                                     code=code,
                                     lane=lane_id)
        self.factory.on_auth_badge(lane_id, code, code_type)
        return True

    def xmlrpc_openGate(self, lane_id):
        self.factory.device_log.info('received open gate {lane}',
                                     lane=lane_id)
        self.factory.on_open_gate(lane_id)
        return True
