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

PermissionTags = Namespace(operator_bypass='operator_bypass',
                           biometric_bypass='biometric_bypass',
                           pin_bypass='pin_bypass',
                           zone_bypass='zone_bypass',
                           vehicle_bypass='vehicle_bypass',
                           escort='escort',
                           carrier='carrier')


class PermissionType(object):

    def __init__(self, type_id, name, tags=None, valid_duration=None, time_to_live=None):
        self.type_id = type_id
        self.name = name
        self.tags = tags if tags else list()
        self.valid_duration = valid_duration
        self.time_to_live = time_to_live


class Permission(object):

    def __init__(self,
                 permission_type,
                 valid_from,
                 valid_to,
                 time_to_live=None,
                 reference=None,
                 tags=None,
                 owner=None,
                 disabled=False):

        self.permission_type = permission_type
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.tags = tags if tags else list()
        self.time_to_live = time_to_live
        self.reference = reference
        self.owner = owner
        self.disabled = disabled
        self.credentials = list()
        self.zones = list()

    def has_tag(self, tag):
        return tag in self.tags or tag in self.permission_type.tags

    def check_zone(self, gate_id, direction):
        return any(map(lambda x: x.has_gate(gate_id, direction), self.zones))

    def check_pass_back(self, direction, pass_back_interval):
        raise NotImplementedError

    def check_vehicle(self, vehicles):
        raise NotImplementedError

    @property
    def is_escort(self):
        return self.has_tag(PermissionTags.escort)

    @property
    def is_carrier(self):
        return self.has_tag(PermissionTags.carrier)
