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
from twisted.internet.defer import inlineCallbacks
from device.devices import E1212
from device.devices.e1212 import ModBusClientFactory, E1212ServerFactory
log = Logger()


@inlineCallbacks
def check_port(port):
    value = yield client.factory.get_port(port)
    yield client.factory.set_port(port, not value)
    value = yield client.factory.get_port(port)
    yield client.factory.set_port(port, not value)


def run_with_log(func):
    d = func()
    d.addErrback(lambda x: log.failure('failure...', failure=x))


if __name__ == '__main__':
    config = dict(factory=E1212, host='192.168.127.254', listen_port=9020)
    config = E1212.CONFIG_SCHEMA(config)

    client = reactor.connectTCP(config['host'], config['port'], ModBusClientFactory())
    client.factory.device_log = log

    server = reactor.listenTCP(config['listen_port'], E1212ServerFactory())
    server.factory.device_log = log
    server.factory.on_port_changed = lambda *x: x

    reactor.callLater(2, run_with_log, lambda: check_port('DO1'))

    reactor.run()
