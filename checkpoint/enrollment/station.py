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
import voluptuous as vol
from device.devices import SIMULATOR
from helpers import class_repr, class_str
from configuration import val


class Station(object):

    __slots__ = ['station_id', 'legacy_lane_id', 'force_simulator', 'badge', 'biometric', 'user_config_folder',
                 'invalid_packets_folder']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Required('legacy_lane_id'): int,
        vol.Required('badge'): val.FactoryDict('enrollment.devices'),
        vol.Required('biometric'): val.FactoryDict('enrollment.devices'),
        vol.Required('user_config_folder', default='config/user_config'): str,
        vol.Required('invalid_packets_folder', default='invalid_packets'): str,
    })

    def __init__(self, station_id, config, force_simulator):
        self.station_id = station_id
        self.legacy_lane_id = config['legacy_lane_id']
        self.force_simulator = force_simulator
        self.user_config_folder = config['user_config_folder']
        self.invalid_packets_folder = config['invalid_packets_folder']
        self.badge = self.get_device('badge', config['badge'])
        self.biometric = self.get_device('biometric', config['biometric'])

    def get_device(self, device_id, device_config):
        factory = device_config['factory'] if not self.force_simulator else SIMULATOR
        return factory(device_id, device_config, self)

    def __repr__(self):
        return class_repr(self, self.station_id)

    def __str__(self):
        return class_str(self, self.station_id)
