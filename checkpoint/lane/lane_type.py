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
from collections import OrderedDict
from commons import Directions
from consoles import ConsoleTags
from helpers import dict_affinity, class_repr, inline_dict, class_str


class LaneType(object):

    __slots__ = ['lane_type_id', 'name', 'console_tags', 'default_config', 'override_configs']

    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Required('console_tags', default=[]): [vol.In(ConsoleTags)],
        vol.Required('default'): {
            vol.Required('automaton'): str,  # validated reference
            vol.Required('check_vehicle', default=False): bool,
            vol.Required('check_biometric', default=False): bool,
            vol.Required('check_operator', default=False): bool,
            vol.Required('check_pin', default=False): bool,
            vol.Required('check_pass_back', default=False): bool
        },
        vol.Required('overrides', default=[]): [
            vol.Schema({
                vol.Required('selectors'): vol.Schema({
                    vol.Optional('lane_status'): str,  # validated reference
                    vol.Optional('security_level'): str,  # validated reference
                    vol.Optional('direction'): vol.In(Directions),
                }),
                vol.Required('config'): {
                    vol.Required('automaton'): str,  # validated reference
                    vol.Optional('check_vehicle'): bool,
                    vol.Optional('check_biometric'): bool,
                    vol.Optional('check_operator'): bool,
                    vol.Optional('check_pin'): bool,
                    vol.Optional('check_pass_back'): bool
                },
            })
        ],
    })

    log = Logger()

    def __init__(self, lane_type_id, config):
        self.lane_type_id = lane_type_id
        self.name = config.get('name', self.lane_type_id)
        self.console_tags = list(config['console_tags'])
        self.default_config = config['default']
        self.override_configs = config['overrides']

    def __repr__(self):
        return class_repr(self, self.lane_type_id)

    def __str__(self):
        return class_str(self, self.lane_type_id)

    def get_config(self, lane_status, security_level, direction):
        """
        return lane type config for this lane attributes.
        the default config is updated with the chosen override.
        """
        item = OrderedDict()
        item['lane_status'] = lane_status.lane_status_id
        item['security_level'] = security_level.security_level_id
        item['direction'] = direction

        config = self.default_config.copy()
        config.update(self.select_override_config(item))
        return config

    def select_override_config(self, item):
        """
        select an override configuration comparing selectors defined in config with given
        item dict. item must be an instance of ordered dict, keys order is used to calculate the
        match score. the override with the highest score is selected.
        first is the most important key, last is the less one.
        """
        current_score = 0
        current_config = self.default_config.copy()
        selection_keys = item.keys()

        assert isinstance(item, OrderedDict), 'ordered dict is required for params'

        self.log.debug('selecting best match config with {keys}...', keys=selection_keys)
        for override_config in self.override_configs:
            score = dict_affinity(selection_keys, override_config['selectors'], item)
            selector = inline_dict(override_config['selectors'])

            if score is None:
                continue

            self.log.debug('selector {selector} match score {score}', selector=selector, score=score)
            if score >= current_score:
                current_score = score
                current_config = override_config['config'].copy()

        return current_config
