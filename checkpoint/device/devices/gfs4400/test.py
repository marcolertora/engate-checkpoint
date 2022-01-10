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


from twisted.internet import reactor
from device.devices import GFS4400
from device.devices.gfs4400 import GFS4400Factory


def print_data(*args):
    print(args)


if __name__ == '__main__':
    config = dict(factory=GFS4400, host='cs005')
    config = GFS4400.CONFIG_SCHEMA(config)
    client_factory = GFS4400Factory(config['interval'], config['mirror'], config['has_ack'])
    client = reactor.connectTCP(config['host'], config['port'], client_factory)
    client.factory.on_read_barcode = print_data
    reactor.run()


