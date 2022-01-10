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
from gate import Gate
from helpers import class_repr, class_str


class Site(object):

    __slots__ = ['site_id', 'name', 'gates', 'checkpoint', 'disabled']

    log = Logger()

    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Required('disabled', default=False): bool,
        vol.Required('gates'): {str: Gate.CONFIG_SCHEMA},
    })

    def __init__(self, site_id, config, checkpoint):
        self.site_id = site_id
        self.checkpoint = checkpoint
        self.gates = dict()
        self.name = config.get('name', self.site_id)
        self.disabled = config['disabled']

        # load gates
        for gate_id, gate_config in config['gates'].items():
            self.gates[gate_id] = Gate(gate_id, gate_config, self)

    def start(self):
        if self.disabled:
            self.log.warn('is disabled, skip start')
            return

        self.log.info('starting...')
        for gate in self.gates.values():
            gate.start()

    def __repr__(self):
        return class_repr(self, self.site_id)

    def __str__(self):
        return class_str(self, self.site_id)
