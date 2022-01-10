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

import re
import socket
import voluptuous as vol
from helpers import traverse, load_module

# tcp/udp port
ipv4_port = vol.All(int, vol.Range(min=1, max=2**16))


# ipv4 address
def ipv4_host(data):
    try:
        socket.inet_aton(data)
        return str(data)
    except socket.error:
        raise vol.Invalid('invalid host {0}'.format(data))


# hostname
def hostname(data):
    """validate hostname"""
    if re.match(r'^[a-zA-Z0-91\-.]+$', str(data)):
        return str(data)
    raise vol.Invalid('invalid automaton node {0}'.format(data))


# could be callable
def is_callable(data):
    if callable(data):
        return data
    raise vol.Invalid('invalid callable {0!r}'.format(data))


# positive float seconds
interval = vol.All(float, vol.Range(min=0.1))

# positive int seconds
timeout = vol.All(int,  vol.Range(min=1))

# float in (+/-) 90 range
latitude = vol.All(float, vol.Range(min=-90, max=90))

# float in (+/-) 180 range
longitude = vol.All(float, vol.Range(min=-180, max=180))


class FactoryDict(object):
    """resolve factory attribute to class"""

    def __init__(self, base_module, factory_attribute='factory'):
        self.base_module = base_module
        self.factory_attribute = factory_attribute

    def __call__(self, data):
        try:
            factory = load_module(self.base_module, data[self.factory_attribute])
        except ImportError:
            raise vol.Invalid('invalid module {0}'.format(data[self.factory_attribute]))
        data[self.factory_attribute] = factory
        return data[self.factory_attribute].CONFIG_SCHEMA(data)


class Reference(object):
    """validate reference inside schema"""

    def __init__(self, path_to_target, path_to_choice, separator='/'):
        self.path_to_target = path_to_target
        self.path_to_choice = path_to_choice
        self.separator = separator

    def __call__(self, data):
        try:
            items = traverse(self.path_to_choice, data, separator=self.separator)
        except KeyError:
            raise vol.Invalid('invalid choices path {0!r}'.format(self.path_to_choice))
        assert len(items) == 1, 'choices path should drive to single result'
        path_to_choices, choices = items[0]
        try:
            targets = traverse(self.path_to_target, data, separator=self.separator)
        except KeyError:
            raise vol.Invalid('invalid target path {0!r}'.format(self.path_to_target))
        for path_to_target, target in targets:
            if target not in choices:
                path_to_value = path_to_target.rstrip(self.separator)
                raise vol.Invalid('invalid reference {0!r}'.format(target), path=path_to_value.split(self.separator))
        return data


