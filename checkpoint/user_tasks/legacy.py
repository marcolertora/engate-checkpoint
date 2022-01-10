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

from twisted.internet.defer import inlineCallbacks, returnValue
from automaton import Tasks


@Tasks.register
@inlineCallbacks
def checkUid(automaton, edge_config, **kwargs):
    assert 'identifier' in kwargs, 'identifier is required'
    transit_member = yield automaton.parent.authenticator.get_transit_member(kwargs['identifier'])
    automaton.parent.transit.add_member(transit_member)
    returnValue(transit_member.auth_status.status_id)


@Tasks.register
def checkTransit(automaton, edge_config, **kwargs):
    return automaton.parent.authenticator.validate_transit()


@Tasks.register
def checkMemberPin(automaton, edge_config, **kwargs):
    assert 'identifier' in kwargs, 'identifier is required'
    return automaton.parent.authenticator.validate_pin(kwargs['identifier'])


