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
from twisted.logger import Logger
from functools import partial
import voluptuous as vol
from time import time
from twisted.internet import reactor

import configuration.validation.automaton
from automaton import Node, NodeType, ThroughType
from commons import Directions
from helpers import class_repr, class_str
from commons.transits import Transit
from configuration import val


class Lane(object):

    __slots__ = ['lane_id', 'config', 'position', 'gate', 'name', 'discard_transit', 'disabled', 'pass_back_interval',
                 'check_devices_loop', 'check_devices_interval', 'lane_type', 'direction', 'lane_status',
                 'security_level', 'not_ready_devices', 'automaton', 'pending_config', 'data', 'duplicate_spool',
                 'transit', 'devices', 'ready', 'authenticator', 'legacy_lane_id', 'disable_check_zone']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Optional('legacy_lane_id'): int,  # TODO: remove after grace period
        vol.Required('direction'): vol.In(Directions),
        vol.Required('type'): str,  # validated reference
        vol.Required('initial_status'): str,  # validated reference
        vol.Required('pass_back_interval', default=None): vol.Maybe(val.interval),
        vol.Required('check_devices_interval', default=3.0): val.interval,
        vol.Required('discard_transit', default=False): bool,
        vol.Required('disabled', default=False): bool,
        vol.Required('disable_check_zone', default=False): bool,
        vol.Required('device_links'): [vol.Schema({
            vol.Required('device'): str,  # validated reference
            vol.Optional('action'): configuration.validation.automaton.AutomatonNode(NodeType.A),
            vol.Optional('event'): configuration.validation.automaton.AutomatonThrough(ThroughType.E)
            # action or event are required
        }).extend(Node.CONFIG_SCHEMA_EXTRA)],
    })

    def __init__(self, lane_id, config, position, gate, pending_config=None, is_reload=False):
        self.lane_id = lane_id
        self.config = config.copy()
        self.position = position
        self.gate = gate
        self.name = config.get('name', self.lane_id)
        self.legacy_lane_id = config.get('legacy_lane_id')
        self.discard_transit = config['discard_transit']
        self.disabled = config['disabled']
        self.pass_back_interval = config['pass_back_interval']
        self.check_devices_interval = config['check_devices_interval']
        self.pending_config = dict()
        self.direction = config['direction']
        self.disable_check_zone = config['disable_check_zone']
        self.lane_type = self.checkpoint.lane_types[config['type']]
        self.security_level = self.gate.security_level

        if pending_config and 'security_level' in pending_config:
            self.security_level = pending_config['security_level']

        self.lane_status = self.checkpoint.lane_status[config['initial_status']]
        if pending_config and 'lane_status' in pending_config:
            self.lane_status = pending_config['lane_status']

        self.devices = dict()
        self.ready = False
        self.not_ready_devices = None

        # stuff
        self.transit = Transit(self)

        # shared data between device
        self.data = dict()
        self.duplicate_spool = dict()

        # authenticator
        self.authenticator = self.checkpoint.authenticator.copy(lane=self)

        # automaton
        self.automaton = self.checkpoint.automatons[self.lane_type_config['automaton']].copy(parent=self)
        self.log.info('bound to {automaton}', automaton=self.automaton)

        self.check_devices_loop = None

        # link devices
        for link_index, link_config in enumerate(config.get('device_links')):
            self.link_device_w_lane(link_config, is_reload=is_reload)
            self.link_device_w_automaton(link_index, link_config)

    @property
    def checkpoint(self):
        return self.gate.checkpoint

    @property
    def consoles(self):
        return self.gate.consoles

    @property
    def lane_type_config(self):
        return self.lane_type.get_config(self.lane_status, self.security_level, self.direction)

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.check_devices_loop = reactor.callLater(self.check_devices_interval, self.check_devices)

    def update_config(self, new_lane_status=None, new_security_level=None):
        """retrieve and apply new lane config. if automaton is changed lane reload is needed to apply it"""
        lane_status = self.lane_status if new_lane_status is None else new_lane_status
        security_level = self.security_level if new_security_level is None else new_security_level
        new_lane_type_config = self.lane_type.get_config(lane_status, security_level, self.direction)
        new_automaton_id = new_lane_type_config['automaton']

        if self.automaton.automaton_id != new_automaton_id:
            # to update automaton a lane reload is needed, add new config in pending_config and schedule a reload
            # in lane_reload pending_config are applied
            self.log.info('schedule lane reload to change from {old} to {new}',
                          old=self.automaton.automaton_id,
                          new=new_automaton_id)
            self.pending_config = dict(lane_status=lane_status, security_level=security_level)
            self.automaton.schedule_reload()

        else:
            # update config without reload
            self.lane_status = lane_status
            self.security_level = security_level

    def __repr__(self):
        return class_repr(self, self.lane_id, self.gate.gate_id, self.direction)

    def __str__(self):
        return class_str(self, self.lane_id, self.gate.gate_id, self.direction)

    def __del__(self):
        self.log.info('removed')

    def set_status(self, lane_status):
        """set the lane status, this is called by automaton"""
        if self.lane_status != lane_status:
            self.log.info('change status from {old} to {new}', old=self.lane_status, new=lane_status)
            self.update_config(new_lane_status=lane_status)

    def set_security_level(self, security_level):
        """set the lane security level, this is called by gate"""
        if self.security_level != security_level:
            self.log.info('change security level from {old} to {new}', old=self.security_level, new=security_level)
            self.update_config(new_security_level=security_level)

    def check_devices(self):
        """check ready state of all linked devices, if all of them are ready the the lane is ready too"""
        not_ready_devices = [x for x in self.devices.values() if not x.is_ready()]

        if self.not_ready_devices is None or self.not_ready_devices != not_ready_devices:
            self.not_ready_devices = not_ready_devices

            if len(not_ready_devices) > 0:
                self.log.warn('not ready devices {not_ready}, lane not ready', not_ready=not_ready_devices)
                self.ready = False
                self.automaton.stop()
            else:
                self.log.info('all devices are ready, lane is ready')
                self.ready = True
                self.automaton.start()

        self.for_any_console(lambda c: c.keep_alive(self.ready))
        self.check_devices_loop = reactor.callLater(self.check_devices_interval, self.check_devices)

    def link_device_w_lane(self, link_config, is_reload=False):
        """
        link checkpoint device with lane
        linked devices come from config, they will be always the same even across lane reload
        """
        device = self.checkpoint.get_or_create_device(link_config['device'], read_only=is_reload)
        self.devices[device.device_id] = device
        self.log.info('associating {lane} to {device}', lane=self, device=device)

    def link_device_w_automaton(self, link_index, link_config):
        """
        link lane devices with automaton event and action
        . if event attach event to device
        . if action attach fire device to action as task
        if the automaton change the links could change across lane reload
        """
        assert link_config['device'] in self.devices, 'missing device'
        device = self.devices[link_config['device']]

        if 'event' in link_config:
            event_label = link_config['event']
            # it should not used in current automaton
            if event_label in self.automaton.events:
                device.attach_event(link_config, self, link_index, self.automaton.events[event_label])

        if 'action' in link_config:
            node_id = link_config['action']
            for node in filter(lambda x: x.base_id == node_id, self.automaton.actions.values()):
                node.add_task(partial(device.fire, link_config))

    def detach(self):
        """called in lane_reload. it deactivate lane before unload"""
        self.log.info('detaching lane...')
        self.automaton.stop()
        self.stop_check_devices_loop()
        for device in self.devices.values():
            device.detach_events(self)

    def stop_check_devices_loop(self):
        if self.check_devices_loop is not None and self.check_devices_loop.active():
            self.check_devices_loop.cancel()

    def for_any_console(self, func):
        for console in self.consoles.values():
            func(console.lane_message_factory(self))

    def on_automaton_start(self):
        self.transit.set_end_date()
        self.for_any_console(lambda c: c.end_transit(self.transit))
        self.transit = Transit(self, uploader=self.checkpoint.uploader)
        self.data = dict()

    def on_automaton_reset(self):
        self.for_any_console(lambda c: c.reset())

    def reload(self):
        self.gate.reload_lane(self)

    def is_duplicated(self, key, interval=60.0):
        """
        check if, in the given interval, the key has already been seen
        at the same time update the key timestamp
        """
        duplicated = not self.duplicate_spool.get(key, 0) <= time()
        self.duplicate_spool[key] = time() + interval
        return duplicated

    def reset_duplicate_spool(self):
        self.log.info('reset duplicate spool')
        self.duplicate_spool = dict()

    def start_transit(self):
        self.log.info('start new transit')
        self.reset_duplicate_spool()
        self.transit.set_start_date()
        self.for_any_console(lambda c: c.start_transit(self.transit))
