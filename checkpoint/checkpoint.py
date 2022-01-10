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
from ruamel.yaml import YAML
from twisted.logger import Logger
import voluptuous as vol
from os import path
from authenticator import Authenticator
from configuration import val, YamlException
from automaton import Automaton
from commons.transits import TransitStatus
from backends import Backend, ItemNotFound
from helpers import class_repr, TransientDict, class_str
from lane.lane_status import LaneStatus
from lane.lane_type import LaneType
from commons import SecurityLevel
from publisher import Publisher
from device.devices import SIMULATOR
from downloader import Downloader
from lane import Site
from uploader import Uploader
import user_tasks

__all__ = ['Checkpoint', 'user_tasks']


class Checkpoint(object):
    __slots__ = ['checkpoint_id', 'config', 'backend', 'uploader', 'publisher', 'downloader', 'automatons',
                 'lane_status', 'transit_status', 'lane_types', 'security_levels', 'sites', 'devices', 'consoles',
                 'attachments', 'force_simulator', 'attachment_time_to_live', 'image_server_url',
                 'invalid_packets_folder', 'user_config_folder', 'authenticator', 'disabled', 'simulator_config',
                 'runtime_config_filename']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema(
        vol.All({
            vol.Required('backend'): Backend.CONFIG_SCHEMA,
            vol.Required('uploader'): Uploader.CONFIG_SCHEMA,
            vol.Required('downloader'): Downloader.CONFIG_SCHEMA,
            vol.Required('publisher'): Publisher.CONFIG_SCHEMA,
            vol.Required('simulator', default={}): {
                vol.Required('host', default='localhost'): vol.Any(val.hostname, val.ipv4_host),
                vol.Required('port', default=1099): val.ipv4_port,
            },
            vol.Required('attachment_time_to_live', default=10): val.timeout,
            vol.Required('image_server_url'): vol.Url(),
            vol.Required('user_config_folder'): vol.IsDir(),
            vol.Optional('runtime_config_filename'): vol.IsFile(),

            # FIXME: not used dump path is hardcoded
            vol.Required('invalid_packets_folder'): vol.IsDir(),
            vol.Required('disabled', default=False): bool,
            vol.Required('lane_status'): {str: LaneStatus.CONFIG_SCHEMA},
            vol.Required('lane_types'):  {str: LaneType.CONFIG_SCHEMA},
            vol.Required('security_levels'): {str: SecurityLevel.CONFIG_SCHEMA},
            vol.Required('devices'): {str: val.FactoryDict('device.devices')},
            vol.Required('consoles'): {str: val.FactoryDict('consoles')},
            vol.Required('transit_status'): {str: TransitStatus.CONFIG_SCHEMA},
            vol.Required('automatons'): {str: Automaton.CONFIG_SCHEMA},
            vol.Required('authenticator', default={}): Authenticator.CONFIG_SCHEMA,
            vol.Required('sites'): {str: Site.CONFIG_SCHEMA},
        },
            # TODO: move reference constraint in key 'target': val.Reference(path_to_choice)
            val.Reference('sites/*/gates/*/consoles/*/', 'consoles/'),
            val.Reference('sites/*/gates/*/initial_security_level/', 'security_levels/'),
            val.Reference('sites/*/gates/*/lanes/*/type/', 'lane_types/'),
            val.Reference('sites/*/gates/*/lanes/*/initial_status/', 'lane_status/'),
            val.Reference('sites/*/gates/*/lanes/*/device_links/*/device/', 'devices/'),
            val.Reference('lane_types/*/default/automaton/', 'automatons/'),
            val.Reference('lane_types/*/overrides/*/config/automaton/', 'automatons/'),
            val.Reference('lane_types/*/overrides/*/selectors/?security_level/', 'security_levels/'),
            val.Reference('lane_types/*/overrides/*/selectors/?lane_status/', 'lane_status/'),
        ))

    def __init__(self, checkpoint_id, config, force_simulator):
        # TODO: filter config by checkpoint_id
        self.checkpoint_id = checkpoint_id
        self.config = config
        self.force_simulator = force_simulator
        self.simulator_config = config['simulator']
        self.attachment_time_to_live = config['attachment_time_to_live']
        self.image_server_url = config['image_server_url']
        self.user_config_folder = config['user_config_folder']
        self.runtime_config_filename = config.get('runtime_config_filename')
        # FIXME: not used
        self.invalid_packets_folder = config.get('invalid_packets_folder')
        self.disabled = config['disabled']
        self.automatons = dict()
        self.authenticator = Authenticator(config['authenticator'])
        self.lane_status = dict()
        self.lane_types = dict()
        self.security_levels = dict()
        self.sites = dict()
        self.devices = dict()
        self.consoles = dict()
        self.attachments = TransientDict()
        self.transit_status = dict()

        # load services
        self.backend = Backend(config['backend'])
        self.uploader = Uploader(config['uploader'], self)
        self.downloader = Downloader(config['downloader'], self)
        self.publisher = Publisher(config['publisher'], self)

        # TODO: compact with map
        # load automatons config
        self.log.info('loading automatons config...')
        for automaton_id, automaton_config in config['automatons'].items():
            self.log.info('add new automaton {automaton}...', automaton=automaton_id)
            self.automatons[automaton_id] = Automaton(automaton_id, automaton_config)

        # load lane status
        self.log.info('loading lane status..')
        for lane_status_id, lane_status_config in config['lane_status'].items():
            self.log.info('add new lane status {lane_status}...', lane_status=lane_status_id)
            self.lane_status[lane_status_id] = LaneStatus(lane_status_id, lane_status_config)

        # load transit status
        self.log.info('loading transit status..')
        for transit_status_id, transit_status_config in config['transit_status'].items():
            self.log.info('add new transit status {transit_status}...', transit_status=transit_status_id)
            self.transit_status[transit_status_id] = TransitStatus(transit_status_id, transit_status_config)

        # load lane types
        self.log.info('loading lane types..')
        for lane_type_id, lane_type_config in config['lane_types'].items():
            self.log.info('add new lane types {lane_type}...', lane_type=lane_type_id)
            self.lane_types[lane_type_id] = LaneType(lane_type_id, lane_type_config)

        # load security levels
        self.log.info('loading security levels..')
        for security_level_id, security_level_config in config['security_levels'].items():
            self.log.info('add new security level {security_level}...', security_level=security_level_id)
            self.security_levels[security_level_id] = SecurityLevel(security_level_id, security_level_config)

        # load sites
        self.log.info('loading sites...')
        for site_id, site_config in config['sites'].items():
            self.sites[site_id] = Site(site_id, site_config, self)

    def __repr__(self):
        return class_repr(self, self.checkpoint_id)

    def __str__(self):
        return class_str(self, self.checkpoint_id)

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        self.uploader.start()
        self.downloader.start()
        self.publisher.start()
        for device in self.devices.values():
            device.start()
        for site in self.sites.values():
            site.start()
        for console in self.consoles.values():
            console.start()

    def get_or_create_device(self, device_id, read_only=True):
        """
        instantiate specific device object using factory class and add to devices
        invoked from lane
        """
        if not read_only and device_id not in self.devices:
            self.log.info('add new device {device}...', device=device_id)
            device_config = self.config['devices'][device_id]
            if self.force_simulator:
                self.devices[device_id] = SIMULATOR(device_id, device_config, self, self.simulator_config)
            else:
                self.devices[device_id] = device_config['factory'](device_id, device_config, self)

        assert device_id in self.devices, 'unknown device'
        return self.devices[device_id]

    def get_or_create_console(self, console_id):
        """
        instantiate specific console object using factory class and add to consoles
        invoked from gate
        """
        if console_id not in self.consoles:
            self.log.info('add new console {console}...', console=console_id)
            console_config = self.config['consoles'][console_id]
            console = console_config['factory'](console_id, console_config)
            self.consoles[console_id] = console
        return self.consoles[console_id]

    def add_attachment(self, attachment):
        """add attachment to a transient dictionary published to console by image service"""
        self.attachments.set_item(attachment.attachment_id, attachment, time_to_live=self.attachment_time_to_live)

    def get_attachment(self, attachment_id):
        self.log.info('get attachment {attachment}', attachment=attachment_id)
        if attachment_id not in self.attachments:
            raise ItemNotFound('missing attachment {0}'.format(attachment_id))
        return self.attachments[attachment_id]

    def read_runtime_config(self, gate_id):
        if not self.runtime_config_filename:
            raise YamlException('no runtime config filename configured')

        self.log.debug('reading runtime config in {filename}...', filename=self.runtime_config_filename)

        if not path.isfile(self.runtime_config_filename):
            raise YamlException('file not found: {0}'.format(self.runtime_config_filename))

        with open(self.runtime_config_filename, 'r') as stream:
            yaml_config = YAML().load(stream)
            if not isinstance(yaml_config, dict):
                raise YamlException('invalid type, wanted dictionary: {0}'.format(self.runtime_config_filename))
            if gate_id not in yaml_config:
                raise YamlException('missing gate: {0}'.format(gate_id))

            return yaml_config[gate_id]
