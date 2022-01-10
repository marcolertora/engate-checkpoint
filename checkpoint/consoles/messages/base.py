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


class LaneMessageFactory(object):

    def __init__(self, parent, lane):
        self.parent = parent
        self.lane = lane

    def keep_alive(self, ready):
        raise NotImplementedError

    def set_transit_status(self, transit, status):
        raise NotImplementedError

    def set_transit_direction(self, transit, direction):
        raise NotImplementedError

    def add_transit_member(self, transit, member):
        raise NotImplementedError

    def reset_transit_members(self, transit):
        raise NotImplementedError

    def add_transit_item(self, transit, transit_item):
        raise NotImplementedError

    def start_transit(self, transit):
        raise NotImplementedError

    def end_transit(self, transit):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
