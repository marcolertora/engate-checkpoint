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

from autobahn.twisted import WebSocketServerProtocol

from base import SimulatorProtocolMixin


class SimulatorServerProtocol(SimulatorProtocolMixin, WebSocketServerProtocol):

    def onOpen(self):
        super(SimulatorServerProtocol, self).onOpen()
        self.factory.register_client(self)

    def connectionLost(self, reason):
        super(SimulatorServerProtocol, self).connectionLost(reason)
        self.factory.unregister_client(self)

    def trigger_event(self, event_params):
        self.send_request(SimulatorProtocolMixin.REQUEST.TRIGGER_EVENT, event_params)
