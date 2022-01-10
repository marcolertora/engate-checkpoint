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

import voluptuous as vol
from twisted.internet.defer import inlineCallbacks, returnValue
from device import Reader, Biometric
from enrollment.devices.biometric import EnrollBiometricDevice
from helpers import async_sleep


class EnrollFAKEBIOMETRIC(EnrollBiometricDevice):

    CONFIG_SCHEMA = Reader.CONFIG_SCHEMA.extend({
        vol.Required('fake_new_template', default='new_biometric_template'): str,
        vol.Required('fake_verify_score', default=60): int,
        vol.Optional('fake_verify_template'): str,
        vol.Required('delay', default=3.0): float,

    })

    def __init__(self, device_id, config, checkpoint):
        super(EnrollFAKEBIOMETRIC, self).__init__(device_id, config, checkpoint)
        self.fake_new_template = config['fake_new_template']
        self.fake_verify_score = config['fake_verify_score']
        self.fake_verify_template = config.get('fake_verify_template')
        self.delay = config['delay']

    @inlineCallbacks
    def verify(self, biometric_type_id, template, threshold, name):
        yield async_sleep(self.delay)

        if self.fake_verify_template:
            score = Biometric.SCORE.MAX if template == self.fake_verify_template else Biometric.SCORE.MIN
        else:
            score = self.fake_verify_score

        is_valid = Biometric.is_valid_score(score, threshold)
        returnValue((is_valid, score, self.fake_new_template))

    @inlineCallbacks
    def enroll(self, biometric_type_id, name):
        yield async_sleep(self.delay)
        returnValue(self.fake_new_template)

