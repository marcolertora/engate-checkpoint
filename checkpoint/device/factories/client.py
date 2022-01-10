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
from twisted.logger import Logger
from device import DeviceException
from twisted.internet.protocol import ReconnectingClientFactory


class DeviceClientFactory(ReconnectingClientFactory):
    noisy = False
    device_log = Logger()
    protocol_factory = None

    def __init__(self, max_reconnection_delay):
        self.protocol = None
        self.maxDelay = max_reconnection_delay

    def startedConnecting(self, connector):
        ReconnectingClientFactory.startedConnecting(self, connector)
        self.device_log.info('connecting...')

    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        self.device_log.warn('connection failed: {reason}, retry in {secs:.0f} secs...',
                             reason=reason.value,
                             secs=self.delay)

    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        self.device_log.warn('connection lost: {reason}, retry in {secs:.0f} secs...',
                             reason=reason.value,
                             secs=self.delay)

    def buildProtocol(self, address):
        self.device_log.info('connection has been established!')
        assert self.protocol_factory, 'protocol_factory should be set'
        self.resetDelay()
        self.protocol = self.protocol_factory()
        self.protocol.factory = self
        return self.protocol

    @property
    def connected_protocol(self):
        if not self.protocol:
            raise DeviceException('device not connected')
        return self.protocol

    def is_ready(self):
        return self.protocol and self.protocol.transport and bool(self.protocol.transport.connected)
