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


from autobahn.twisted.websocket import WebSocketClientFactory

from device.factories import DeviceClientFactory
from ..proto import SimulatorClientProtocol


class SimulatorClientFactory(WebSocketClientFactory, DeviceClientFactory):

    def __init__(self, max_reconnection_delay, device_id, simulator_host, simulator_port):
        url = u'ws://{0}:{1}'.format(simulator_host, simulator_port)
        WebSocketClientFactory.__init__(self, url=url)
        DeviceClientFactory.__init__(self, max_reconnection_delay)
        self.protocol_factory = lambda: SimulatorClientProtocol(device_id)

    def on_trigger_event(self, client, event_params):
        raise NotImplementedError

    def execute_action(self, link_config):
        self.connected_protocol.execute_action(link_config)

    def is_ready(self):
        return True
