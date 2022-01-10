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

from device import DeviceException
from montraf_push import MONTRAFPush, MONTRAFMessage
from device.protocols.parsed import ParsedProtocol


class MontrafServerProto(ParsedProtocol):

    def __init__(self):
        ParsedProtocol.__init__(self)
        self.message_factory = MONTRAFPush.parse_packets

    def handle_messages(self, messages):
        for command, values in messages:
            self.factory.device_log.warn('received command {command}', command=command)

            for unit, logs, tag in values:
                for log in logs:
                    self.factory.device_log.warn('received log: {log}', log=log)

                if command == MONTRAFMessage.transit:
                    self.factory.on_read_tag(unit, tag)
                    continue

                if command == MONTRAFMessage.life:
                    continue

                raise DeviceException('unknown command {0}'.format(command))

