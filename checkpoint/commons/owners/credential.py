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


class Credential(object):

    def __init__(self,
                 credential_type,
                 code_type,
                 valid_from,
                 valid_to,
                 code,
                 pin_code=None,
                 permission=None,
                 disabled=False):

        self.credential_type = credential_type
        self.code_type = code_type
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.code = code
        self.pin_code = pin_code
        self.disabled = disabled
        self.permission = permission

