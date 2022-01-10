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

from argparse import Namespace
from device import Biometric, DeviceException, BiometricType
from device.devices.hgr.factory import HGRFactory
import voluptuous as vol
from configuration import val


class HGR(Biometric):

    CONFIG_SCHEMA = Biometric.CONFIG_SCHEMA.extend({
        vol.Required('host'): vol.Any(val.hostname, val.ipv4_host),
        vol.Required('port', default=3001): val.ipv4_port,
        vol.Required('timeout', default=65): val.timeout,
        vol.Required('interval', default=1.0): val.interval,
        vol.Required('left_hand', default=True): bool,
    })

    def __init__(self, device_id, config, checkpoint):
        biometric_type = BiometricType.LEFT_HAND if config['left_hand'] else BiometricType.RIGHT_HAND
        super(HGR, self).__init__(device_id, config, checkpoint, biometric_type)
        self.client = None

    def starting(self):
        client_factory = HGRFactory(self.config['max_reconnection_delay'],
                                    self.config['interval'],
                                    self.config['left_hand'],
                                    self.config['timeout'])
        self.client = self.tcp_client(self.config['host'], self.config['port'], client_factory)

    def is_ready(self):
        if not self.client:
            raise DeviceException('device not started')

        return self.client.factory.is_ready()

    def verify(self, transit, biometric, template):
        if not self.client:
            raise DeviceException('device not started')

        defer = self.client.factory.verify(template)
        defer.addCallback(lambda x: self.on_verify_complete(x[0], x[1], transit, biometric))
        defer.addErrback(self.on_failure, transit)
