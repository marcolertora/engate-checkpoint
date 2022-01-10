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

from automaton import Tasks


@Tasks.register
def setLaneStatus(automaton, edge_config, **kwargs):
    assert 'status' in edge_config, 'status is required in setLaneStatus'
    status_id = edge_config['status']
    assert status_id in automaton.parent.checkpoint.lane_status, 'invalid status_id {0}'.format(status_id)
    automaton.parent.set_status(automaton.parent.checkpoint.lane_status[status_id])


@Tasks.register
def checkLaneStatus(automaton, edge_config, **kwargs):
    assert 'status' in edge_config, 'status is required in checkLaneStatus'
    status_id = edge_config['status']
    assert status_id in automaton.parent.checkpoint.lane_status, 'invalid status_id {0}'.format(status_id)
    return automaton.parent.lane_status.lane_status_id == status_id


@Tasks.register
def cleanLaneSpool(automaton, edge_config, **kwargs):
    automaton.parent.reset_duplicate_spool()
