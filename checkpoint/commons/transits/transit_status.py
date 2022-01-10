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
from argparse import Namespace
import voluptuous as vol
from configuration import val
from helpers import class_repr, class_str


class TransitStatus(object):
    __slots__ = ['status_id', 'name', 'granted', 'color', 'timeout']

    Color = Namespace(red='red', yellow='yellow', green='green')

    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('name'): str,
        vol.Required('color'): vol.In(Color),
        vol.Required('granted', default=False): bool,
        vol.Optional('timeout'): val.timeout,
    })

    def __init__(self, status_id, config):
        self.status_id = status_id
        self.name = config.get('name', self.status_id)
        self.granted = config['granted']
        self.color = config['color']
        self.timeout = config.get('timeout')

    def __repr__(self):
        return class_repr(self, self.status_id)

    def __str__(self):
        return class_str(self, self.status_id)
