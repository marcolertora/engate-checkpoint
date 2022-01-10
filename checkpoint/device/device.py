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

from os import path
from ruamel.yaml import YAML
from twisted.internet import reactor
from twisted.logger import Logger
from exceptions import DeviceException
from helpers import class_str, class_repr
import voluptuous as vol
from configuration import val


class Device(object):
    __slots__ = ['device_id', 'config', 'checkpoint', 'attached_events', 'attachment_prefix', 'max_reconnection_delay',
                 'user_config_folder', 'user_config', 'invalid_packets_folder', 'disabled']

    log = Logger()

    ATTACHMENT_SEPARATOR = '@'

    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Required('factory'): val.is_callable,
        vol.Required('disabled', default=False): bool,
        vol.Optional('attachment_prefix'): str,
        vol.Required('max_reconnection_delay', default=60): vol.All(int, vol.Range(min=1)),
    })

    single_lane = False

    def __init__(self, device_id, config, checkpoint):
        self.checkpoint = checkpoint
        self.device_id = device_id
        self.config = config
        self.disabled = config['disabled']
        self.attachment_prefix = config.get('attachment_prefix', self.device_id)
        self.user_config_folder = self.checkpoint.user_config_folder
        self.invalid_packets_folder = self.checkpoint.invalid_packets_folder
        # TODO: move in start
        self.user_config = self.load_user_config()

    def __repr__(self):
        return class_repr(self, self.device_id)

    def __str__(self):
        return class_str(self, self.device_id)

    def tcp_client(self, host, port, factory):
        factory.device_log = self.log
        return reactor.connectTCP(host, port, factory)

    def tcp_server(self, listen_port, factory):
        factory.device_log = self.log
        return reactor.listenTCP(listen_port, factory)

    def udp_server(self, listen_port, factory):
        factory.device_log = self.log
        port = reactor.listenUDP(listen_port, factory)
        port.factory = factory
        return port

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.starting()

    def starting(self):
        raise NotImplementedError

    def is_ready(self):
        raise NotImplementedError

    def get_attachment_name(self, *keys):
        keys = [self.attachment_prefix] + list(keys)
        return Device.ATTACHMENT_SEPARATOR.join(keys).lower()

    @property
    def user_config_filename(self):
        filename = 'device-{device}.dump'.format(device=self.device_id)
        return path.join(self.user_config_folder, filename)

    def save_user_config(self):
        if not self.user_config:
            self.log.debug('saving user config in {filename}...', filename=self.user_config_filename)
            if not self.user_config_folder:
                raise DeviceException('user config folder not configured')
            if not path.isdir(self.user_config_folder):
                raise DeviceException('invalid user config folder: {0}'.format(self.user_config_folder))
            with open(self.user_config_filename, 'w') as stream:
                YAML().dump(self.user_config, stream)

    def load_user_config(self):
        if not self.user_config_folder:
            raise DeviceException('user config folder not configured')
        if path.isfile(self.user_config_filename):
            self.log.info('loading user config in {filename}...', filename=self.user_config_filename)
            with open(self.user_config_filename, 'r') as stream:
                yaml_config = YAML().load(stream)
                if yaml_config:
                    return yaml_config

        return dict()
