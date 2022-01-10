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

from vehicle import Vehicle


class JtisEvent(Vehicle):

    def __init__(self, plate=None, event_name=None, timestamp=None, **params):
        super(JtisEvent, self).__init__(plate=plate)
        self.event_name = event_name
        self.timestamp = timestamp
        self.params = params

    @property
    def details(self):
        data = super(Vehicle, self).details
        data['event_name'] = self.event_name
        data['timestamp'] = self.timestamp
        data.update(self.params)
        return data
