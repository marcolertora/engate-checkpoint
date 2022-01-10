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

from twisted.internet.defer import inlineCallbacks
from output import OutputDevice


class Camera(OutputDevice):

    @inlineCallbacks
    def fire(self, link_config, automaton, edge_config, **kwargs):
        self.log.info('triggering...')
        yield self.trigger_camera(automaton.lane.transit)

    @inlineCallbacks
    def trigger_camera(self, transit):
        raise NotImplementedError

    def on_media_received(self, transit, item):
        self.log.info('received media! {item}', item=item)
        transit.add_item(item)
