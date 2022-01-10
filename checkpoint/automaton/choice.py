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

from through import ThroughType, Through


class Choice(Through):

    def __init__(self, through_id):
        super(Choice, self).__init__(through_id)

    @staticmethod
    def result_to_label(value):
        if isinstance(value, bool):
            value = 'on' if value else 'off'

        return Through.dump_id(ThroughType.L, value)


class DefaultChoice(Choice):

    LABEL = 'L@__default__'

    def __init__(self):
        super(DefaultChoice, self).__init__(DefaultChoice.LABEL)
