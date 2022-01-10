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
import voluptuous as vol


class AutomatonNode(object):
    """validate automaton node syntax: [allowed_types]@node_name@node_serial"""

    regexp_node = r'^[{0}]@[a-zA-Z\-]+$'
    regexp_node_w_serial = r'^[{0}]@[a-zA-Z\-\_]+@[0-9\-]+$'

    def __init__(self, *allowed_types, **kwargs):
        self.allow_serial = bool(kwargs.get('allow_serial'))
        self.allowed_types = ''.join(allowed_types)

    def __call__(self, data):
        if re.match(self.regexp_node.format(self.allowed_types), str(data)):
            return str(data)
        if self.allow_serial and re.match(self.regexp_node_w_serial.format(self.allowed_types), str(data)):
            return str(data)
        raise vol.Invalid('invalid automaton node {0}'.format(data))


class AutomatonThrough(object):
    """validate automaton through syntax: [allowed_types]@label"""

    regexp_event = r'^[{0}]@[a-zA-Z\-\_]+$'

    def __init__(self, *allowed_types):
        self.allowed_types = ''.join(allowed_types)

    def __call__(self, data):

        if re.match(self.regexp_event.format(self.allowed_types), str(data)):
            return str(data)

        raise vol.Invalid('invalid automaton event {0}'.format(data))