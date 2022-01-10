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

from collections import namedtuple

ZoneItem = namedtuple('ZoneItem', ['gate_id', 'direction'])


class Zone(object):

    def __init__(self):
        self.items = list()

    def add_gate(self, gate_id, direction):
        self.items.append(ZoneItem(gate_id, direction))

    def has_gate(self, my_gate_id, my_direction):
        assert my_gate_id is not None, 'gate is required'
        assert my_direction is not None, 'direction is required'

        # in items direction = null means all directions
        for zone_item in self.items:
            if zone_item.gate_id == my_gate_id:
                if zone_item.direction is None or zone_item.direction == my_direction:
                    return True

        return False

