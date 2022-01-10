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

from twisted.internet.defer import inlineCallbacks, returnValue

from device import Biometric
from device.devices import HGR
from device.devices.hgr.factory import HGRFactory
from biometric import EnrollBiometricDevice


class EnrollHGR(EnrollBiometricDevice):

    CONFIG_SCHEMA = HGR.CONFIG_SCHEMA

    def __init__(self, device_id, config, checkpoint):
        super(EnrollHGR, self).__init__(device_id, config, checkpoint)
        client_factory = HGRFactory(config['max_reconnection_delay'], config['interval'], config['left_hand'], config['timeout'])
        self.client = self.tcp_client(config['host'], config['port'], client_factory)

    @inlineCallbacks
    def verify(self, biometric_type_id, template, threshold, name):
        score, template = yield self.client.factory.verify(template)
        is_valid = Biometric.is_valid_score(score, threshold)
        returnValue((is_valid, score, template))

    @inlineCallbacks
    def enroll(self, biometric_type_id, name):
        template = yield self.client.factory.enroll()
        returnValue(template)
