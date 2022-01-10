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

from exceptions import InvalidPacket, IncompletePacket
from twisted.internet.protocol import Protocol
from helpers import dump_exception_w_payload


class ParsedProtocol(Protocol):

    factory = None
    message_factory = None

    def __init__(self):
        self.data_buffer = ''

    def dataReceived(self, data):
        # self.factory.device_log.debug('data received {data}', data=data)
        try:
            self.data_buffer += data
            messages = self.message_factory(self.data_buffer)
            self.data_buffer = ''
            self.handle_messages(messages)
        except InvalidPacket:
            self.invalid_packet(data)
        except IncompletePacket:
            return

    def handle_messages(self, messages):
        raise NotImplementedError

    def invalid_packet(self, payload):
        self.factory.device_log.failure('received invalid packet:')
        dump_exception_w_payload(payload)
        self.transport.loseConnection()

