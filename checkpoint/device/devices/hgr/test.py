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
from device.devices import HGR
from device.devices.hgr.factory import HGRFactory


def print_data(*args):
    print(args)


if __name__ == '__main__':
    config = dict(factory=HGR, host='172.16.50.111')
    config = HGR.CONFIG_SCHEMA(config)
    template = '77867F597293876F72'
    client_factory = HGRFactory(config['interval'], config['left_hand'], config['timeout'])
    client = reactor.connectTCP(config['host'], config['port'], client_factory)
    client.factory.on_timeout = print_data
    reactor.callLater(2, lambda: client.factory.abort())
    reactor.callLater(2, lambda: client.factory.enroll().addBoth(print_data, 'enroll'))
    reactor.callLater(40, lambda: client.factory.verify(template).addBoth(print_data, 'verify'))

    reactor.run()

