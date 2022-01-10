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

from device.devices.legacy.proto import LegacyResource
from device.factories import HTTPServerFactory


class LegacyServerFactory(HTTPServerFactory):

    def __init__(self, username, password):
        resource = LegacyResource(username, password, useDateTime=True, allowNone=True)
        HTTPServerFactory.__init__(self, resource)

    def on_auth_person(self, lane_id, person, operator, documents, params):
        raise NotImplementedError

    def on_auth_badge(self, lane_id, code, code_type):
        raise NotImplementedError

    def on_open_gate(self, lane_id):
        raise NotImplementedError
