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

import voluptuous as vol
from configuration import val
from device.factories import HTTPServerFactory
from helpers import class_repr, class_str
from twisted.internet import reactor
from rpc import RpcEnrollment
from station import Station
from twisted.logger import Logger


class Enrollment(object):
    __slots__ = ['enrollment_id', 'listen_port', 'force_http_client', 'stations']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('listen_port', default=9999): val.ipv4_port,
        vol.Required('stations'): {str: Station.CONFIG_SCHEMA},
        vol.Optional('force_http_client'): vol.Url(),
    })

    def __init__(self, enrollment_id, config, force_simulator):
        self.enrollment_id = enrollment_id
        self.listen_port = config['listen_port']
        self.force_http_client = config.get('force_http_client')
        self.stations = {x: Station(x, y, force_simulator) for x, y in config['stations'].items()}

    def __repr__(self):
        return class_repr(self, self.enrollment_id)

    def __str__(self):
        return class_str(self, self.enrollment_id)

    def start(self):
        resource = RpcEnrollment(self.log,
                                 self.stations,
                                 self.force_http_client)
        reactor.listenTCP(self.listen_port, HTTPServerFactory(resource))
