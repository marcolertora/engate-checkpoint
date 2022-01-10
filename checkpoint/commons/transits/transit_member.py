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

from commons import AuthStatus, AuthStatusId
from commons.owners import OwnerUnknown
from helpers import class_repr, class_str


class TransitMember(object):
    __slots__ = ['owner', 'permission', 'credential', 'auth_status']

    def __init__(self, owner=None, auth_status=None):
        self.owner = owner if owner else OwnerUnknown()
        self.permission = None
        self.credential = None
        self.auth_status = auth_status if auth_status else AuthStatus()

    def __repr__(self):
        return class_repr(self, self.owner, auth_status=self.auth_status)

    def __str__(self):
        return class_str(self, self.owner.name, self.auth_status.status_id)

    @property
    def key(self):
        return self.owner.owner_id

    @property
    def is_auth(self):
        return self.auth_status.status_id == AuthStatusId.ALLOWED

    @property
    def is_valid(self):
        return self.auth_status.status_id in (AuthStatusId.ALLOWED,
                                              AuthStatusId.OPERATOR_REQUIRED,
                                              AuthStatusId.BIOMETRIC_REQUIRED,
                                              AuthStatusId.PIN_REQUIRED)

    @property
    def is_known(self):
        return self.auth_status.status_id != AuthStatusId.UNKNOWN

    def set_auth(self, auth_result):
        assert isinstance(auth_result, AuthStatus), 'invalid auth result'
        if auth_result.status_id != AuthStatusId.DUNNO:
            self.auth_status = auth_result
