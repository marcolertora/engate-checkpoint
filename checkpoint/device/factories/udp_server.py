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

from twisted.internet.protocol import DatagramProtocol
from twisted.logger import Logger


class UDPServerFactory(DatagramProtocol):
    noisy = False
    device_log = Logger()
    protocol_factory = None

    def __init__(self):
        pass

    def buildProtocol(self, address):
        assert self.protocol_factory, 'protocol_factory should be set'
        protocol = self.protocol_factory()
        protocol.factory = self
        return protocol

    def datagramReceived(self, datagram, address):
        self.buildProtocol(address).dataReceived(datagram)

    def is_ready(self):
        return True
