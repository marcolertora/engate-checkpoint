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


from twisted.internet import reactor
from twisted.web.client import getPage

from device.devices import TARGET
from device.devices.target import DVS


def handle_result(message):
    results = DVS.parse_packet(message)
    plate_code = results[0]['text']
    print 'received plate_code {plate_code}'.format(plate_code=plate_code)

    # attach transit item
    attachments = list()
    for result in results:
        camera_id = int(result['id'])
        name = '{0}_{1}'.format('plate' if camera_id == self.plate_camera_id else 'overview', camera_id)
        print name, result['content_type'], len(result['stream'])
        #attachments.append(Attachment(self.get_attachment_name(name), result['content_type'], result['stream']))


def print_data(*args):
    print(args)


if __name__ == '__main__':
    config = dict(factory=TARGET, url='http://172.16.1.181:8888')
    config = TARGET.CONFIG_SCHEMA(config)

    url = config['url']
    timeout = config['timeout']
    plate_camera_id = config['plate_camera']
    context_cameras_id = config['context_camera']

    payload = DVS.get_dime_plate_array(plate_camera_id, context_cameras_id)
    defer = getPage(url, method='POST', postdata=payload, timeout=timeout)
    defer.addCallback(handle_result)
    defer.addErrback(print_data)

    reactor.run()

