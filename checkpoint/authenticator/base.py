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
from copy import deepcopy
import voluptuous as vol
from twisted.internet.defer import inlineCallbacks
from helpers import class_repr, class_str
from twisted.logger import Logger


class AuthenticatorBase(object):

    CONFIG_SCHEMA = vol.Schema({})

    __slots__ = ['authenticator_lane']

    log = Logger()

    def __init__(self, config):
        assert config is not None, 'invalid config'
        self.authenticator_lane = None

    @property
    def lane(self):
        assert self.authenticator_lane is not None, 'set lane never invoked'
        return self.authenticator_lane

    @lane.setter
    def lane(self, lane):
        self.authenticator_lane = lane

    def copy(self, lane):
        automaton = deepcopy(self)
        automaton.lane = lane
        return automaton

    def __repr__(self):
        return class_repr(self)

    def __str__(self):
        return class_str(self)

    @inlineCallbacks
    def get_transit_member(self):
        raise NotImplementedError
