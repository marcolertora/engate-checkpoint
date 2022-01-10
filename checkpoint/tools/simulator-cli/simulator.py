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

from __future__ import unicode_literals

import argparse
from twisted.internet import reactor
from device.devices.simulator import SimulatorServerFactory
from cli import SimulatorCLI, LoggerCLI

if __name__ == '__main__':
    log = LoggerCLI()
    parser = argparse.ArgumentParser()
    parser.add_argument('--listen-port',
                        dest='listen_port',
                        type=int,
                        default=1099,
                        metavar='port',
                        help='listen port (default: %(default)d)')

    cli_args = parser.parse_args()

    log.info('starting simulator server on port {listen_port}...', listen_port=cli_args.listen_port)
    factory = SimulatorServerFactory(log, 'ws://127.0.0.1:{0}'.format(cli_args.listen_port))
    reactor.listenTCP(cli_args.listen_port, factory)

    cli = SimulatorCLI(factory)
    defer = cli.deferred_run()
    defer.addCallback(lambda x: reactor.stop())

    reactor.run()
