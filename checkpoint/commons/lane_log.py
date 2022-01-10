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


class LaneLog(object):

    __slots__ = ['lane_log_id', 'lane_id', 'level', 'code', 'message', 'timestamp']

    LEVEL = Namespace(
        INFO='INFO',
        WARNING='WARNING',
        ERROR='ERROR',
    )

    CODE = Namespace(
        START='START',
        RELOAD='RELOAD',
        CHANGE_STATUS='CHANGE_STATUS',
        GENERIC_ALARM='GENERIC_ALARM',
        GENERIC_WARNING='GENERIC_WARNING',
        DOOR_ALARM_OPEN_TOO_LONG='DOOR_ALARM_OPEN_TOO_LONG',
        DOOR_ALARM_OPEN_FORCED='DOOR_ALARM_OPEN_FORCED',
        DOOR_ALARM_END='DOOR_ALARM_END',
        DOOR_FAULT='DOOR_FAULT',
        DOOR_FAULT_END='DOOR_FAULT_END',
        DOOR_TAMPER='DOOR_TAMPER',
        DOOR_TAMPER_END='DOOR_TAMPER_END',
    )

    def __init__(self, lane_id, level, code, message, timestamp=datetime.now()):
        self.lane_log_id = uuid.uuid4().hex.upper()
        self.lane_id = lane_id
        self.level = level
        self.code = code
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return class_repr(self, self.lane_log_id)

    def __str__(self):
        return class_str(self, self.lane_log_id)
