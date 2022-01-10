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

import voluptuous as vol
from helpers import class_repr, class_str


class LaneStatus(object):

    __slots__ = ['lane_status_id', 'name']

    CONFIG_SCHEMA = vol.Schema({
            vol.Optional('name'): str,
    })

    def __init__(self, lane_status_id, config):
        self.lane_status_id = lane_status_id
        self.name = config.get('name', self.lane_status_id)

    def __repr__(self):
        return class_repr(self, self.lane_status_id)

    def __str__(self):
        return class_str(self, self.lane_status_id)
