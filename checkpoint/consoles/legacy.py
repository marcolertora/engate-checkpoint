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
import cPickle
from base import Console
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from messages import LegacyLaneMessageFactory


class LegacyConsole(Console):

    __slots__ = Console.__slots__ + ['host', 'port', 'sender', 'started']

    CONFIG_SCHEMA = Console.CONFIG_SCHEMA.extend({
        vol.Required('host', default=''): str,
        vol.Required('port', default=3001): val.ipv4_port,
    })

    lane_factory = LegacyLaneMessageFactory

    def __init__(self, console_id, config):
        super(LegacyConsole, self).__init__(console_id, config)
        self.sender = reactor.listenUDP(0, DatagramProtocol())
        self.host = config['host']
        self.port = config['port']
        self.started = False

    def send_message(self, packet_type, params):
        if not self.started:
            self.log.info('console not started, skip send')
            return

        params['type'] = packet_type
        self.sender.write(cPickle.dumps(params), (self.host, self.port))

    def starting(self):
        self.started = True
