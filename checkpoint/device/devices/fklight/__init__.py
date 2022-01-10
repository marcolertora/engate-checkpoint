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

from configuration import val
import voluptuous as vol
from twisted.internet.defer import inlineCallbacks, returnValue
from device import OutputRelay, DeviceException
from device import Reader
from factory import FKLIGHTFactory


class FKLIGHT(Reader, OutputRelay):

    CONFIG_SCHEMA = Reader.CONFIG_SCHEMA.extend({
        vol.Required('host'): vol.Any(val.hostname, val.ipv4_host),
        vol.Required('port', default=1470): val.ipv4_port,
        vol.Required('interval', default=0.5): val.interval,
        vol.Required('units', default=[1]): [int],
    })

    def __init__(self, device_id, config, checkpoint):
        super(FKLIGHT, self).__init__(device_id, config, checkpoint)
        self.client = None

    def starting(self):
        client_factory = FKLIGHTFactory(self.config['max_reconnection_delay'],
                                        self.config['units'],
                                        self.config['interval'])
        self.client = self.tcp_client(self.config['host'], self.config['port'], client_factory)
        self.client.factory.on_read_badges = self.on_read_badges

    def is_ready(self):
        if not self.client:
            raise DeviceException('device not started')

        return self.client.factory.is_ready()

    def get_event_key(self, link_config):
        assert 'unit' in link_config, 'no unit configured in link'
        return link_config['unit']

    def on_read_badges(self, unit, badges):
        self.on_read_identifiers(badges, key=unit)

    def pulse_port(self, unit, port, value, duration):
        if not self.client:
            raise DeviceException('device not started')

        assert port == 0, 'only port 0 is allowed'
        assert value, 'only true value is allowed'
        self.client.factory.pulse(unit, duration)

    def set_port(self, unit, port, value):
        raise NotImplementedError

    def check_port(self, unit, port, value):
        raise NotImplementedError

