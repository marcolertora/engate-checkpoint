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
from device.devices.gfs4400.factory import GFS4400Factory
from device import Reader, DeviceException


class GFS4400(Reader):

    CONFIG_SCHEMA = Reader.CONFIG_SCHEMA.extend({
        vol.Required('host'): vol.Any(val.hostname, val.ipv4_host),
        vol.Required('port', default=4002): val.ipv4_port,
        vol.Required('interval', default=3.0): val.interval,
        vol.Optional('mirror', default=False): bool,
        vol.Required('has_ack', default=True): bool,
    })

    def __init__(self, device_id, config, checkpoint):
        super(GFS4400, self).__init__(device_id, config, checkpoint)
        self.client = None

    def starting(self):
        client_factory = GFS4400Factory(self.config['max_reconnection_delay'],
                                        self.config['interval'],
                                        self.config['mirror'],
                                        self.config['has_ack'])
        self.client = self.tcp_client(self.config['host'], self.config['port'], client_factory)
        self.client.factory.on_read_barcode = self.on_read_identifier

    def is_ready(self):
        if not self.client:
            raise DeviceException('device not started')

        return self.client.factory.is_ready()
