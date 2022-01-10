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

from commons import Directions
from automaton import Tasks


@Tasks.register
def startTransit(automaton, edge_config, **kwargs):
    automaton.parent.start_transit()


@Tasks.register
def setTransitStatus(automaton, edge_config, **kwargs):
    assert 'status' in edge_config, 'status is required in setTransitStatus'
    status_id = edge_config['status']
    assert status_id in automaton.parent.checkpoint.transit_status, 'invalid status_id {0}'.format(status_id)
    automaton.parent.transit.set_status(automaton.parent.checkpoint.transit_status[status_id])


@Tasks.register
def setTransitDirection(automaton, edge_config, **kwargs):
    assert 'direction' in edge_config, 'direction is required in setTransitDirection'
    direction = Directions(edge_config['direction'])
    automaton.parent.transit.set_direction(direction)

