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

import re
from pymodbus.client.asynchronous import twisted
from twisted.internet.defer import inlineCallbacks, returnValue
from device import DeviceException
from proto import E1212ServerProto
from device.factories import DeviceClientFactory, DeviceServerFactory


class ModBusClientFactory(DeviceClientFactory):

    @staticmethod
    def parse_port(port):
        match = re.match(r'^(?P<type>D[IO])(?P<id>[0-9]+)$', port)
        if not match:
            raise ValueError('invalid port id')
        return match.group('type'), int(match.group('id'))

    def __init__(self, max_reconnection_delay):
        DeviceClientFactory.__init__(self, max_reconnection_delay)
        self.protocol_factory = lambda: twisted.ModbusTcpClientProtocol()

    @inlineCallbacks
    def set_port(self, port, value):
        self.device_log.debug('setting port {port} value to {value}...', port=port, value=value)
        port_type, port_index = ModBusClientFactory.parse_port(port)
        if port_type == 'DI':
            raise DeviceException('cannot set input port')

        result = yield self.connected_protocol.write_coil(port_index, value)
        if result.isError():
            raise DeviceException('unknown protocol error')

        self.device_log.debug('port value has been set!')

    @inlineCallbacks
    def get_port(self, port):
        self.device_log.debug('getting port {port} value...', port=port)
        port_type, port_index = ModBusClientFactory.parse_port(port)
        if port_type == 'DI':
            result = yield self.connected_protocol.read_discrete_inputs(port_index, count=1)
        else:
            result = yield self.connected_protocol.read_coils(port_index, count=1)

        if result.isError():
            raise DeviceException('unknown protocol error')

        value = result.bits[0]
        self.device_log.debug('got port value {value}!', value=value)
        returnValue(value)


class E1212ServerFactory(DeviceServerFactory):

    def __init__(self):
        DeviceServerFactory.__init__(self)
        self.last_values = list()
        self.protocol_factory = lambda: E1212ServerProto()

    def on_mask_received(self, values):
        if not self.last_values:
            self.device_log.info('missing last values, using this ones...')
            self.last_values = values
            return

        for index, value in enumerate(values):
            if value is not None and self.last_values[index] != value:
                self.last_values[index] = value
                port = 'DI{0}'.format(index)
                self.device_log.debug('port {port} has changed value to {value}!', port=port, value=value)
                self.on_port_changed(port, value)

    def on_port_changed(self, port, value):
        raise NotImplementedError
