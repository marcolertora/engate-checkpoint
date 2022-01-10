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
import argparse
import uuid

from twisted.logger import Logger

from commons.owners.owner import OwnerVehicle
from commons.transit_items import JtisEvent
from commons.transits import Transit, TransitMember
from device.protocols.xmlrpc_auth_server import XMLRPCAuth
from twisted.web import xmlrpc, server

log = Logger()


class JTISResource(XMLRPCAuth):

    def __init__(self, username=None, password=None, **kwargs):
        XMLRPCAuth.__init__(self, username, password, **kwargs)

    def xmlrpc_notifyVehicleEvent(self, plate_code, event, timestamp, params):
        log.info('received vehicle event {event} {plate_code}', event=event, plate_code=plate_code)
        self.forward_transit(plate_code, event, timestamp, params)
        return True

    def forward_transit(self, plate_code, event, timestamp, params):
        transit = map_transit(timestamp, plate_code)
        transit.set_date(timestamp)
        transit.add_item(JtisEvent(plate_code, event, timestamp, **params))
        transit.add_member(TransitMember(OwnerVehicle(plate_code, plate_code)))


def map_transit(event, timestamp, plate_code):
    member_dict = dict(auth='UNKNOWN',
                       auth_code='',
                       auth_message='',
                       ownertype_id='OwnerVehicle',
                       people_fullname=plate_code,
                       vehicle_plate=plate_code
                       )

    transit_dict = dict(transit_id=uuid.uuid4().hex.upper(),
                        transit_start_date=timestamp,
                        transit_end_date=timestamp,
                        lanestatus_id='OPENED',
                        direction_id='TROUGHT',
                        lane_name=event,
                        transit_permissions=[member_dict],
                        )
    return transit_dict


if __name__ == '__main__':

    from twisted.internet import reactor

    parser = argparse.ArgumentParser()
    parser.add_argument('--username',
                        dest='username',
                        type=str,
                        metavar='username',
                        help='username (default: %(default)s)')
    parser.add_argument('--password',
                        dest='password',
                        type=str,
                        metavar='secret',
                        help='username (default: %(default)s)')
    parser.add_argument('--listen-port',
                        dest='listen_port',
                        type=int,
                        default=6666,
                        metavar='port',
                        help='listen port (default: %(default)d)')

    args = parser.parse_args()

    resource = JTISResource(args.username, args.password, allowNone=True, useDateTime=True)
    log.info('starting service on port: {port}...', port=args.listen_port)
    reactor.listenTCP(args.listen_port, server.Site(resource))
    reactor.run()
