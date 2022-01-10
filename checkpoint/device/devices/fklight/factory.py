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

from helpers import SerialDeferred
from proto import FKLIGHTProto
from device.factories import DeviceClientFactory


class FKLIGHTFactory(DeviceClientFactory):

    def __init__(self, max_reconnection_delay, units, polling_interval):
        DeviceClientFactory.__init__(self, max_reconnection_delay)
        self.defer = SerialDeferred()
        self.protocol_factory = lambda: FKLIGHTProto(units, polling_interval)

    def on_badges_received(self, unit, badges):
        self.device_log.info('{badges} read on unit {unit}!', unit=unit, badges=badges)
        self.defer.callback(badges)
        self.on_read_badges(unit, badges)

    def pulse(self, unit, duration):
        self.device_log.info('pulsing unit {unit} for {duration} secs', unit=unit, duration=duration)
        self.connected_protocol.pulse(unit, duration)

    def read_badge(self, timeout=10):
        self.device_log.info('reading badge for {timeout} secs', timeout=timeout)
        return self.defer.new_deferred(timeout)

    def on_read_badges(self, unit, badges):
        raise NotImplementedError
