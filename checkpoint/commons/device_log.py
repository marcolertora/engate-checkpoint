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
from helpers import class_str, class_repr


class DeviceLog(object):

    __slots__ = ['device_log_id', 'device_id', 'level', 'code', 'message', 'timestamp']

    LEVEL = Namespace(
        DEBUG='DEBUG',
        INFO='INFO',
        WARNING='WARNING',
        ERROR='ERROR',
    )
    CODE = Namespace(
        DURESS='DURESS',
        DOOR_TAMPER='DOOR_TAMPER',
        READER_TAMPER='READER_TAMPER',
        CASING_OPEN='CASING_OPEN',
        NETWORK_LOST='NETWORK_LOST',
        NETWORK_LOST_END='NETWORK_LOST_END',
    )

    def __init__(self, device_id, level, code, message, timestamp=datetime.now()):
        self.device_log_id = uuid.uuid4().hex.upper()
        self.device_id = device_id
        self.level = level
        self.code = code
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return class_repr(self, self.device_log_id)

    def __str__(self):
        return class_str(self, self.device_log_id)
