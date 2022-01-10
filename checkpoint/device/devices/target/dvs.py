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

from cStringIO import StringIO
from time import time
from dime import Message, Record
from dime import TypeByUri, MediaType
from struct import pack, unpack, error as struct_error
from device.protocols.exceptions import InvalidPacket
from helpers import class_name


class DVS(object):

    UNKNOWN_PLATE = 'XXXXXXX'

    REQUEST = '''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
     xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
     xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
     xmlns:ns1="urn:dvs">
     <SOAP-ENV:Body SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <ns1:getDimePlateArray>
        <cameraId>%(cameraId)d</cameraId>
        <camerasCntx xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="xsd:int[%(size)d]">%(camerasCntx)s</camerasCntx>
       </ns1:getDimePlateArray>
     </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    RESPONSE = '''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
     xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema"
     xmlns:ns1="urn:dvs">
     <SOAP-ENV:Body SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <ns1:getDimePlateArrayResponse>
       <param-16 xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns1:DimeData[%d]">
        %s
      </param-16>
      </ns1:getDimePlateArrayResponse>
     </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    @staticmethod
    def image(stream):
        header = (12 * '\x00') + pack('<I', int(time())) + (4 * '\x00')
        return header + stream

    @staticmethod
    def get_dime_plate_array(camera_id, camera_context_ids=None):
        camera_context_ids = camera_context_ids if camera_context_ids else list()
        size = len(camera_context_ids)
        assert size < 2, 'Not supported by the Device'
        cameras_cntx = ''.join(map(lambda x: '<item>{0}</item>'.format(x), camera_context_ids))
        return DVS.REQUEST % dict(cameraId=camera_id, size=size, camerasCntx=cameras_cntx)

    @staticmethod
    def get_dime_plate_array_response(plates):
        records = list()
        items = map(lambda x: '<item href="{0}s"/>'.format(x['id']), plates)
        records.append(Record(id='cid:id0',
                              type=TypeByUri('http://schemas.xmlsoap.org/soap/envelope/'),
                              data=DVS.RESPONSE % (len(items) + 1, '\n'.join(items)),
                              mb=True))

        for plate in plates:
            records.append(Record(id=plate['id'],
                                  type=MediaType(plate['content_type']),
                                  data=DVS.image(plate['stream'])))

        message = StringIO()
        Message(records).save(message)
        return message.getvalue()

    @staticmethod
    def get_image(record):
        if len(record.options) == 0:
            return None

        ts = unpack('<I', record.data[12:16])[0]
        stream = record.data[20:]
        text = record.options[0]
        image_id = record.id
        content_type = str(record.type)
        return dict(id=image_id, text=text, ts=ts, stream=stream, content_type=content_type)

    @staticmethod
    def parse_packet(data):
        try:
            msg = Message.load(StringIO(data))
        except struct_error:
            raise InvalidPacket('error parsing record structures')
        except (Record.FaultyRecord, Record.UnsupportedVersion) as dime_error:
            raise InvalidPacket('{0} {1}'.format(class_name(dime_error), dime_error.message))

        results = map(lambda x: DVS.get_image(x), msg)
        return filter(lambda x: x is not None, results)
