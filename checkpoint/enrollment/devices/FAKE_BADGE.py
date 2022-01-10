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
from twisted.internet.defer import inlineCallbacks, returnValue, CancelledError
from commons.identifiers import Badge
from badge import EnrollBadgeDevice
from device import Reader
from helpers import async_sleep


class EnrollFAKEBADGE(EnrollBadgeDevice):

    CONFIG_SCHEMA = Reader.CONFIG_SCHEMA.extend({
        vol.Required('fake_badge_code', default='1234567890'): str,
        vol.Required('fake_code_type', default='EM-4X02'): str,
        vol.Required('delay', default=3.0): float,

    })

    def __init__(self, device_id, config, checkpoint):
        super(EnrollFAKEBADGE, self).__init__(device_id, config, checkpoint)
        self.fake_badge_code = config['fake_badge_code']
        self.fake_code_type = config['fake_code_type']
        self.delay = config['delay']

    @inlineCallbacks
    def read_badge(self, timeout):
        if timeout < self.delay:
            yield async_sleep(timeout)
            raise CancelledError()
        badges = [Badge(self.fake_badge_code, code_type=self.fake_code_type)]
        yield async_sleep(self.delay)
        returnValue(badges)
