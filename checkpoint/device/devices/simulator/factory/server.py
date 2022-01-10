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

import random
from autobahn.twisted.websocket import WebSocketServerFactory
from ..exception import SimulatorException
from ..proto import SimulatorServerProtocol
from collections import namedtuple

DictDevice = namedtuple('DictDevice', ['device_id', 'device_config'])


class SimulatorServerFactory(WebSocketServerFactory):
    protocol = SimulatorServerProtocol

    def __init__(self, log, *args, **kwargs):
        self.log = log
        self.clients = dict()
        super(SimulatorServerFactory, self).__init__(*args, **kwargs)

    @property
    def devices(self):
        devices = filter(lambda x: x is not None, self.clients.values())
        devices.sort(key=lambda x: x.device_id)
        return devices

    def get_client(self, device_id):
        clients = filter(lambda x: self.clients[x].device_id == device_id, self.clients)
        if not len(clients):
            raise SimulatorException('no client for device {0}'.format(device_id))
        assert len(clients) <= 1, 'more than one client for device {0}'.format(device_id)
        return clients[0]

    def get_device(self, client):
        assert client in self.clients, 'unregistered client {0}'.format(client.peer)
        return self.clients[client]

    def get_random_device(self):
        assert len(self.devices), 'no registered devices found'
        return random.choice(self.devices)

    def register_client(self, client):
        if client not in self.clients:
            self.clients[client] = None
            self.log.debug('client registered {client} [{count}]', client=client.peer, count=len(self.clients))

    def unregister_client(self, client):
        if client in self.clients:
            del self.clients[client]
            self.log.debug('client unregistered {client} [{count}]', client=client.peer, count=len(self.clients))

    def on_execute_action(self, client, action_name):
        device = self.get_device(client)
        self.log.info('received action {device} {action}', device=device.device_id, action=action_name)

    def on_announce(self, client, device_id, device_config):
        assert client in self.clients, 'unregistered client'
        self.clients[client] = DictDevice(device_id, device_config=device_config)
        self.log.info('announced device {device} on client {client}', client=client.peer, device=device_id)

    def trigger_event(self, device_id, event_params):
        self.log.info('trigger event on device {device}', device=device_id)
        self.get_client(device_id).trigger_event(event_params)
