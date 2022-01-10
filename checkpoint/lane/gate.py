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
from twisted.internet import reactor
from helpers import class_repr, class_str
from twisted.logger import Logger
from lane import Lane
from configuration import val, YamlException


class Gate(object):

    __slots__ = ['name', 'gate_id', 'location', 'disabled', 'site', 'lanes', 'consoles', 'update_config_interval',
                 'update_config_loop', 'security_level']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Required('initial_security_level'): str,  # validated reference
        vol.Required('update_config_interval', default=30.0): val.interval,
        vol.Optional('latitude'): val.latitude,
        vol.Optional('longitude'): val.longitude,
        vol.Required('disabled', default=False): bool,
        vol.Required('lanes'): {str: Lane.CONFIG_SCHEMA},
        vol.Required('consoles', default=[]): [str],
    })

    def __init__(self, gate_id, config, site):
        self.gate_id = gate_id
        self.site = site
        self.name = config.get('name', self.gate_id)
        self.lanes = dict()
        self.update_config_loop = None
        self.consoles = dict()
        self.disabled = config['disabled']

        self.update_config_interval = config['update_config_interval']
        self.location = config.get('latitude'), config.get('longitude')
        self.security_level = self.checkpoint.security_levels[config['initial_security_level']]

        # load console linked in gate and attach to checkpoint
        for console_id in config['consoles']:
            self.consoles[console_id] = self.checkpoint.get_or_create_console(console_id)

        # load lanes
        for lane_position, (lane_id, lane_config) in enumerate(config['lanes'].items()):
            self.lanes[lane_id] = Lane(lane_id, lane_config, lane_position, self)

    @property
    def checkpoint(self):
        return self.site.checkpoint

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.update_config_loop = reactor.callLater(self.update_config_interval, self.update_config)
        for lane in self.lanes.values():
            lane.start()

    def __repr__(self):
        return class_repr(self, self.gate_id)

    def __str__(self):
        return class_str(self, self.gate_id)

    def reload_lane(self, lane):
        """replace the current lane with the new one preserving pending_config"""
        lane_id = lane.lane_id
        self.log.info('reloading {lane}...', lane=lane_id)
        new_lane = Lane(lane_id, lane.config, lane.position, self, pending_config=lane.pending_config, is_reload=True)
        if lane_id in self.lanes:
            self.lanes[lane_id].detach()
        self.lanes[lane_id] = new_lane
        self.lanes[lane_id].start()

    def update_config(self):
        self.log.debug('updating config...')
        try:
            config = self.checkpoint.read_runtime_config(self.gate_id)
        except YamlException, err:
            self.log.debug('skip config update: {err}', err=err)
            self.update_config_loop = reactor.callLater(self.update_config_interval, self.update_config)
            return

        if 'security_level' in config:
            if config['security_level'] not in self.checkpoint.security_levels:
                self.log.warn('invalid security_level {0}, skip update'.format(config['security_level']))
                return

            for lane in self.lanes.values():
                lane.set_security_level(self.checkpoint.security_levels[config['security_level']])

        if 'default_message' in config:
            for console in self.checkpoint.consoles.values():
                console.set_default_message(config['default_message'])

        self.update_config_loop = reactor.callLater(self.update_config_interval, self.update_config)

    def stop_update_config_loop(self):
        if self.update_config_loop is not None and self.update_config_loop.active():
            self.update_config_loop.cancel()
