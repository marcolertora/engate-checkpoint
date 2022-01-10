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

from argparse import Namespace
from helpers import class_repr, class_str

# FIXME: status should be ALLOWED/REJECTED only.

AuthStatusId = Namespace(
    UNKNOWN='UNKNOWN',
    ALLOWED='ALLOWED',
    DUNNO='DUNNO',
    REJECTED='REJECTED',
    OPERATOR_REQUIRED='OPERATOR_REQUIRED',
    BIOMETRIC_REQUIRED='BIOMETRIC_REQUIRED',
    PIN_REQUIRED='PIN_REQUIRED',
)

AuthCode = Namespace(
    UNKNOWN='UNKNOWN',
    ALLOWED='ALLOWED',
    PIN_REQUIRED='PIN_REQUIRED',
    INVALID_PIN='INVALID_PIN',
    BIOMETRIC_REQUIRED='BIOMETRIC_REQUIRED',
    INVALID_BIOMETRIC='INVALID_BIOMETRIC',
    OPERATOR_REQUIRED='OPERATOR_REQUIRED',
    INVALID_OPERATOR='INVALID_OPERATOR',
    INVALID_LANE='INVALID_LANE',
    INVALID_STATUS='INVALID_STATUS',
    INVALID_DATE='INVALID_DATE',
    INVALID_VEHICLE='INVALID_VEHICLE',
    INVALID_COMPANY='INVALID_COMPANY',
    INVALID_DOCUMENT='INVALID_DOCUMENT',
    INVALID_DRIVER='INVALID_DRIVER',
    INVALID_PASS_BACK='INVALID_PASS_BACK',
    INVALID_PAYMENT='INVALID_PAYMENT',
)


class AuthStatus(object):

    __slots__ = ['status_id', 'code', 'message']

    # FIXME: message default should be None
    def __init__(self, status_id=None, code=None, message=''):
        self.status_id = status_id if status_id else AuthStatusId.UNKNOWN
        self.code = code if code else AuthCode.UNKNOWN
        self.message = message

    def __repr__(self):
        return class_repr(self, self.status_id, self.message)

    def __str__(self):
        return class_str(self, self.status_id, self.message)
