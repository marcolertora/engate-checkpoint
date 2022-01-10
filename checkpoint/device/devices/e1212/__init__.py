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

from functools import partial
from twisted.internet.defer import inlineCallbacks, returnValue
from device import OutputRelay, InputRelay, DeviceException
from device.devices.e1212.factory import ModBusClientFactory, E1212ServerFactory
import voluptuous as vol
from configuration import val


class E1212(OutputRelay, InputRelay):

    CONFIG_SCHEMA = OutputRelay.CONFIG_SCHEMA.extend({
        vol.Required('host'): vol.Any(val.hostname, val.ipv4_host),
        vol.Required('port', default=502): val.ipv4_port,
        vol.Required('listen_port', default=9020): val.ipv4_port,
    })

    def __init__(self, device_id, config, checkpoint):
        super(E1212, self).__init__(device_id, config, checkpoint)
        self.unit = None
        self.client = None
        self.server = None

    def starting(self):
        client_factory = ModBusClientFactory(self.config['max_reconnection_delay'])
        self.client = self.tcp_client(self.config['host'], self.config['port'], client_factory)
        self.server = self.tcp_server(self.config['listen_port'], E1212ServerFactory())
        self.server.factory.on_port_changed = partial(self.on_port_changed, self.unit)

    def is_ready(self):
        if not self.client:
            raise DeviceException('device not started')

        return self.client.factory.is_ready()

    @inlineCallbacks
    def set_port(self, unit, port, value):
        if not self.client:
            raise DeviceException('device not started')

        assert unit == self.unit, 'unit is not supported'
        yield self.client.factory.set_port(port, value)

    @inlineCallbacks
    def get_port(self, unit, port):
        if not self.client:
            raise DeviceException('device not started')

        assert unit == self.unit, 'unit is not supported'
        value = yield self.client.factory.get_port(port)
        returnValue(value)
