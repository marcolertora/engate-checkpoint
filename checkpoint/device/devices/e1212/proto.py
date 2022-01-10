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

from p2p import P2P
from device.protocols import ServerProtocol


class E1212ServerProto(ServerProtocol):

    def __init__(self):
        ServerProtocol.__init__(self)
        self.message_factory = P2P.parse_packets

    def handle_messages(self, messages):
        for message_type, value in messages:
            if message_type == P2P.MESSAGE_TYPE.MASK:
                self.factory.on_mask_received(value)
