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
from device.devices import FKLIGHT
from device.devices.fklight import FKLIGHTFactory
from device.devices.fklight.apromix import APROMIX


def print_data(*args):
    print(args)


def set_new_id(device_config, old_address, new_address):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((device_config['host'], device_config['port']))
    message = APROMIX.SetSetupSeriale(old_address, new_address)
    s.send(message)
    s.close()


if __name__ == '__main__':
    config = dict(factory=FKLIGHT, host='172.16.50.154', units=[1])
    config = FKLIGHT.CONFIG_SCHEMA(config)
    # set_new_id(config, old_address, new_address)
    client_factory = FKLIGHTFactory(config['units'], config['interval'])
    client = reactor.connectTCP(config['host'], config['port'], client_factory)
    client.factory.on_badge_read = print_data

    defer = client.factory.read_badge(4)
    defer.addCallback(print_data, 'callback')
    defer.addErrback(print_data, 'errback')

    # reactor.callLater(2, lambda: client.factory.pulse(1, 10))

    reactor.run()


