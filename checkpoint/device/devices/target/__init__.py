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

from twisted.internet.defer import inlineCallbacks
from twisted.web.client import getPage
from device.protocols import InvalidPacket
from device import ANPR, DeviceException
from dvs import DVS
from commons.identifiers import Plate
from commons import Attachment
from commons.transit_items import Vehicle
import voluptuous as vol
from configuration import val
from helpers import dump_exception_w_payload


class TARGET(ANPR):

    CONFIG_SCHEMA = ANPR.CONFIG_SCHEMA.extend({
            vol.Required('url'): vol.Url(),
            vol.Required('timeout', default=10): val.timeout,
            vol.Required('plate_camera', default=0): vol.All(int,  vol.Range(min=0, max=4)),
            vol.Required('context_camera', default=[1]): [vol.All(int,  vol.Range(min=0, max=4))],
        })

    def __init__(self, device_id, config, checkpoint):
        super(TARGET, self).__init__(device_id, config, checkpoint)
        self.url = self.config['url']
        self.timeout = self.config['timeout']
        self.plate_camera_id = self.config['plate_camera']
        self.context_cameras_id = self.config['context_camera']

    def starting(self):
        pass

    def is_ready(self):
        if self.disabled:
            raise DeviceException('device not started')

        return True

    def handle_result(self, message, transit):
        try:
            results = DVS.parse_packet(message)
        except InvalidPacket:
            dump_exception_w_payload(message)
            return

        plate_code = results[0]['text']
        self.log.info('received plate_code {plate_code}', plate_code=plate_code)

        # attach transit item
        attachments = list()
        for result in results:
            camera_id = int(result['id'])
            name = '{0}_{1}'.format('plate' if camera_id == self.plate_camera_id else 'overview', camera_id)
            attachments.append(Attachment(self.get_attachment_name(name), result['content_type'], result['stream']))

        transit_item = Vehicle(plate_code, attachments=attachments)
        self.on_media_received(transit, transit_item)

        # trigger event
        if plate_code != DVS.UNKNOWN_PLATE:
            identifier = Plate(plate_code)
            self.on_read_plate(identifier, transit=transit)

    @inlineCallbacks
    def trigger_camera(self, transit):
        if self.disabled:
            raise DeviceException('device not started')

        payload = DVS.get_dime_plate_array(self.plate_camera_id, self.context_cameras_id)
        defer = getPage(self.url, method='POST', postdata=payload, timeout=self.timeout)
        defer.addCallback(self.handle_result, transit)
        defer.addErrback(lambda x: self.log.failure('reading plate', failure=x))
