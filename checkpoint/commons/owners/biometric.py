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

from helpers import class_str, class_repr


class Biometric(object):

    def __init__(self, biometric_id, biometric_type, template, threshold, bypass, owner=None):
        self.biometric_id = biometric_id
        self.biometric_type = biometric_type
        self.template = template
        self.device_templates = dict()
        self.threshold = threshold
        self.bypass = bypass
        self.owner = owner

    def __repr__(self):
        return class_repr(self, self.biometric_id)

    def __str__(self):
        return class_str(self, self.biometric_id)

    def add_device_template(self, device_id, template):
        self.device_templates[device_id] = template

    def get_template(self, device_id=None):
        return self.device_templates.get(device_id, self.template)
