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

from proto import GFS4400Proto
from device.factories import DeviceClientFactory


class GFS4400Factory(DeviceClientFactory):

    def __init__(self, max_reconnection_delay, polling_interval, is_mirror, has_ack):
        DeviceClientFactory.__init__(self, max_reconnection_delay)
        self.protocol_factory = lambda: GFS4400Proto(polling_interval, is_mirror, has_ack)

    def on_read_barcode(self):
        raise NotImplementedError


