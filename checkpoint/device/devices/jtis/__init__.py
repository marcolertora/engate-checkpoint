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


from commons.owners.owner import OwnerVehicle
from commons.transits import TransitMember
from device import InputDevice, DeviceException
from factory import JTISServerFactory
from commons.transit_items import JtisEvent
import voluptuous as vol
from configuration import val


class JTIS(InputDevice):

    CONFIG_SCHEMA = InputDevice.CONFIG_SCHEMA.extend({
        vol.Required('listen_port', default=6666): val.ipv4_port,
        vol.Required('username', default='admin'): str,
        vol.Required('password', default='secret'): str,
    })

    def __init__(self, device_id, config, checkpoint):
        super(JTIS, self).__init__(device_id, config, checkpoint)
        self.server = None

    def starting(self):
        server_factory = JTISServerFactory(self.config['username'], self.config['password'])
        self.server = self.tcp_server(self.config['listen_port'], server_factory)
        self.server.factory.on_vehicle_event = self.on_vehicle_event

    def is_ready(self):
        if not self.server:
            raise DeviceException('device not started')

        return self.server.factory.is_ready()

    def on_vehicle_event(self, plate_code, event, timestamp, params):
        for item in self.get_attached_events():
            item.lane.transit.set_date(timestamp)

            # attach transit item
            transit_item = JtisEvent(plate_code, event, timestamp, **params)
            item.lane.transit.add_item(transit_item)

            # add transit member
            member = TransitMember()
            member.owner = OwnerVehicle(plate_code, plate_code)
            item.lane.transit.add_member(member)

            # trigger event
            item.event.trigger()
