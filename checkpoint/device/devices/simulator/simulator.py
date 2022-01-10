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


import voluptuous as vol
from commons.identifiers import Badge
from device import DeviceException, Reader
from factory import SimulatorClientFactory


class SIMULATOR(Reader):

    CONFIG_SCHEMA = Reader.CONFIG_SCHEMA.extend({
        vol.Extra: vol.Any(),
    })

    def __init__(self, device_id, config, checkpoint, simulator_config):
        super(SIMULATOR, self).__init__(device_id, config, checkpoint)
        self.simulator_config = simulator_config
        # TODO: should be set from client
        self.raise_exception_on_fire = False
        self.client = None

    def starting(self):
        client_factory = SimulatorClientFactory(self.config['max_reconnection_delay'],
                                                self.device_id,
                                                self.simulator_config['host'],
                                                self.simulator_config['port'])
        self.client = self.tcp_client(self.simulator_config['host'],
                                      self.simulator_config['port'],
                                      client_factory)
        self.client.factory.on_trigger_event = self.on_trigger_event

    def on_trigger_event(self, client, event_params):
        self.log.info('received trigger event {params!r}', params=event_params)

        event_key = event_params.pop('key', None)
        self.log.info('received event {key} {params}', key=event_key, params=event_params)

        if 'identifier' in event_params:
            identifier = Badge(event_params['identifier'], code_type='EM-4X02')
            self.on_read_identifier(identifier)
            return

        kwargs = dict()
        kwargs.update(event_params)
        self.trigger_events(key=event_key, **kwargs)

    def test_user_config(self):
        counter = self.user_config.get('counter', 0)
        self.log.debug('persistent counter is {0}'.format(counter))
        self.user_config['counter'] = counter + 1
        self.save_user_config()

    def is_ready(self):
        if not self.client:
            raise DeviceException('device not started')

        self.test_user_config()
        return self.client.factory.is_ready()

    def fire(self, link_config, parent, edge_config, **kwargs):
        if not self.client:
            raise DeviceException('device not started')

        if self.raise_exception_on_fire:
            raise DeviceException('something wrong firing device')

        self.client.factory.execute_action(link_config)
