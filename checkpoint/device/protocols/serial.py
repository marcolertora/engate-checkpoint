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

from collections import deque
from twisted.internet import reactor
from watchdog import ProtocolWatchDog


class ProtocolSerial(ProtocolWatchDog):

    def __init__(self, polling_interval):
        ProtocolWatchDog.__init__(self)
        assert polling_interval < self.watchdog_interval, 'polling interval too low for watchdog'
        self.polling_interval = polling_interval
        self.messages = deque()

    def get_next_polling_message(self):
        raise NotImplementedError

    def add_message(self, message):
        self.messages.append(message)

    def next_message(self):
        if len(self.messages):
            self.transport.write(self.messages.popleft())
        else:
            reactor.callLater(self.polling_interval, self.transport.write, self.get_next_polling_message())

