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

from twisted.internet import reactor


class TransientDict(dict):
    """a dictionary where items are deleted when time_to_live expire"""
    default_time_to_live = 10

    def set_item(self, key, value, time_to_live=None):
        time_to_live = time_to_live if time_to_live else self.default_time_to_live

        if key not in self:
            eraser = reactor.callLater(time_to_live, lambda x: self.__delitem__(x), key)
            item = dict(eraser=eraser, time_to_live=time_to_live, value=value)
            super(TransientDict, self).__setitem__(key, item)
            return

        assert self[key]['eraser'].active(), 'item still in dictionary but eraser not active'
        self[key]['eraser'].reset(time_to_live)

    def __setitem__(self, key, value):
        self.set_item(key, value, time_to_live=self.default_time_to_live)

    def __getitem__(self, key):
        item = super(TransientDict, self).__getitem__(key)
        return item['value']
