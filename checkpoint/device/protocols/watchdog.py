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

from time import time
from twisted.internet import reactor
from client import ClientProtocol


class ProtocolWatchDog(ClientProtocol):

    def __init__(self):
        ClientProtocol.__init__(self)
        self.watchdog_interval = 5.0
        self.watchdog_scale = 1.5
        self.last_seen = time()

    def set_last_seen(self):
        self.last_seen = time()

    def watchdog(self):
        if self.last_seen < (time() - (self.watchdog_interval * self.watchdog_scale)):
            self.factory.device_log.warn('device not responding to keep alive, closing connection')
            self.transport.loseConnection()
            return

        reactor.callLater(self.watchdog_interval, self.watchdog)
