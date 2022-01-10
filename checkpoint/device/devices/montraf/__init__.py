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

from factory import MontrafServerFactory
from device import Reader, DeviceException
import voluptuous as vol
from configuration import val


class MONTRAF(Reader):

    CONFIG_SCHEMA = Reader.CONFIG_SCHEMA.extend({
        vol.Required('listen_port', default=4023): val.ipv4_port,
    })

    def __init__(self, device_id, config, checkpoint):
        super(MONTRAF, self).__init__(device_id, config, checkpoint)
        self.server = None

    def starting(self):
        self.server = self.udp_server(self.config['listen_port'], MontrafServerFactory())
        self.server.factory.on_read_tag = self.on_read_tag

    def is_ready(self):
        if not self.server:
            raise DeviceException('device not started')

        return self.server.factory.is_ready()

    def get_event_key(self, link_config):
        assert 'unit' in link_config, 'no unit configured in link'
        return link_config['unit']

    def on_read_tag(self, unit, tag):
        self.on_read_identifier(tag, key=unit)
