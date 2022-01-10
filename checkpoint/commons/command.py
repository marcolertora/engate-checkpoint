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

import uuid
from argparse import Namespace
from datetime import datetime
from helpers import class_repr, class_str


class Command(object):

    __slots__ = ['command_id', 'action', 'params', 'timestamp']

    ACTION = Namespace(
        UPDATE_BIOMETRIC='UPDATE_BIOMETRIC',
        UPDATE_PARKING_SLOT='UPDATE_PARKING_SLOT',
    )

    def __init__(self, action, params, timestamp=datetime.now()):
        self.command_id = uuid.uuid4().hex.upper()
        self.action = action
        self.params = params
        self.timestamp = timestamp

    def __repr__(self):
        return class_repr(self, self.command_id)

    def __str__(self):
        return class_str(self, self.command_id)
