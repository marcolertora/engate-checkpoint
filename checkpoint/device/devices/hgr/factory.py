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

from device import DeviceException
from helpers import SerialDeferred
from proto import HGRProto
from device.factories import DeviceClientFactory


class HGRFactory(DeviceClientFactory):

    def __init__(self, max_reconnection_delay, polling_interval, left_hand, timeout):
        DeviceClientFactory.__init__(self, max_reconnection_delay)
        self.defer = SerialDeferred()
        self.timeout = timeout
        self.protocol_factory = lambda: HGRProto(polling_interval, left_hand)

    def verify(self, template):
        self.abort()
        self.device_log.info('verify given template')
        self.connected_protocol.verify(template)
        return self.defer.new_deferred(self.timeout)

    def enroll(self):
        self.abort()
        self.device_log.info('enroll new template')
        self.connected_protocol.enroll()
        return self.defer.new_deferred(self.timeout)

    def abort(self):
        self.device_log.info('cancel pending operation')
        self.defer.cancel()
        self.connected_protocol.abort()

    def on_verify_complete(self, score, template):
        self.device_log.info('template verified! {score} {template}', score=score, template=template)
        self.defer.callback((score, template))

    def on_enroll_complete(self, template):
        self.device_log.info('new template enrolled! {template}', template=template)
        self.defer.callback(template)

    def on_failure(self, reason):
        self.device_log.warn('failure occurred')
        self.defer.errback(DeviceException(reason))
