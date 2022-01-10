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

from transit_item import TransitItem


class Authorization(TransitItem):

    __slots__ = TransitItem.__slots__ + ['operator', 'destination', 'reason']

    def __init__(self, operator, destination, reason, attachments=None):
        super(Authorization, self).__init__(attachments)
        self.operator = operator
        self.destination = destination
        self.reason = reason

    @property
    def details(self):
        data = super(Authorization, self).details
        data['operator'] = self.operator
        data['destination'] = self.destination
        data['reason'] = self.reason
        return data

