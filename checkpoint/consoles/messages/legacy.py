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
from base import LaneMessageFactory
from commons.owners.owner import OwnerVehicle, OwnerPerson
from commons.transit_items import Vehicle
from helpers import class_name


class LegacyLaneMessageFactory(LaneMessageFactory):

    def send_message(self, packet_type, **kwargs):
        params = dict(lane_id='{0}-{1}'.format(self.lane.gate.gate_id, self.lane.lane_id),
                      lane_name=self.lane.name,
                      priority='{0}-{1}'.format(self.lane.gate.gate_id, self.lane.position),
                      lane_location=self.lane.gate.location,
                      gate_name=self.lane.gate.name,
                      gate_location=self.lane.gate.location,
                      lane_flags=self.lane.lane_type.console_tags,
                      lanetype_name=self.lane.lane_type.name,
                      direction_name=self.lane.direction,
                      securitylevel_name=self.lane.security_level.name,
                      lanestatus_name=self.lane.lane_status.name,
                      antipassback=self.lane.pass_back_interval,
                      automa_id=self.lane.automaton.name)

        params.update(kwargs)
        return self.parent.send_message(packet_type, params)

    def keep_alive(self, ready):
        self.send_message('KeepAlive',
                          ready=ready,
                          gatelink=True,
                          imageurl=self.lane.checkpoint.image_server_url)

    def set_transit_status(self, transit, status):
        self.send_message('SetTransitStatus',
                          transit_id=transit.transit_id,
                          status=status.name,
                          color=status.color,
                          timeout=status.timeout)

    def set_transit_direction(self, transit, direction):
        self.send_message('SetTransitDirection',
                          transit_id=transit.transit_id,
                          transitdirection_id=direction,
                          transitdirection_name=direction)

    def add_transit_member(self, transit, member):
        if member.is_known:

            permission = dict(auth='ALLOW' if member.is_valid else 'REJECT',
                              auth_code=member.auth_status.code,
                              auth_message=self.parent.translation.gettext(member.auth_status.message),
                              ownertype_id=class_name(member.owner),
                              people_fullname=member.owner.name,
                              people_id=member.owner.photo_id)

            permission['company_fullname'] = ''
            permission['companytype_name'] = ''

            if member.owner.company:
                permission['company_fullname'] = member.owner.company.name
                permission['companytype_name'] = member.owner.company.company_type

            if isinstance(member.owner, OwnerPerson):
                permission['people_birthday_date'] = member.owner.birth_date
                permission['people_birthday_place'] = member.owner.birth_country

            if isinstance(member.owner, OwnerVehicle):
                permission['vehicle_plate'] = member.owner.plate

            if member.permission:
                permission_type = member.permission.permission_type.name
                permission['permissiontype_name'] = self.parent.translation.gettext(permission_type)

            self.send_message('AddPermission',
                              transit_id=transit.transit_id,
                              permission=permission,
                              permission_key=member.key)

    def reset_transit_members(self, transit):
        self.send_message('CleanPermissions',
                          transit_id=transit.transit_id)

    def add_transit_item(self, transit, transit_item):
        if isinstance(transit_item, Vehicle):
            self.send_message('AddTransitItem',
                              transit_id=transit.transit_id,
                              titem_code=transit_item.plate,
                              titemclass_id='Plate',
                              titem=transit_item.details)

        for attachment in transit_item.attachments:
            self.send_message('AddAttachment',
                              transit_id=transit.transit_id,
                              attachment_id=attachment.attachment_id)

    def start_transit(self, transit):
        self.send_message('StartTransit',
                          transit_id=transit.transit_id,
                          transit_start_date=transit.start_date)

    def end_transit(self, transit):
        self.send_message('EndTransit',
                          transit_id=transit.transit_id,
                          transit_end_date=transit.end_date)

    def reset(self):
        self.send_message('Reset')
