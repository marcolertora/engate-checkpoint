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

from argparse import Namespace
from datetime import datetime
from commons.owners import OwnerPerson, PermissionType, Permission, Company
from commons.transits import TransitMember
from commons.identifiers import Badge
from commons.transit_items import Authorization
from commons import Attachment, AuthStatus, AuthStatusId, AuthCode
from device import InputDevice, DeviceException
from device.devices.legacy.factory import LegacyServerFactory
import voluptuous as vol
from configuration import val
from gettext import gettext as _


class LEGACY(InputDevice):

    ACTION_KEY = Namespace(OPEN_GATE='open_gate', AUTH_BADGE='auth_badge', AUTH_PERSON='auth_person')

    CONFIG_SCHEMA = InputDevice.CONFIG_SCHEMA.extend({
        vol.Required('listen_port', default=9997): val.ipv4_port,
        vol.Required('username', default='admin'): str,
        vol.Required('password', default='secret'): str,
    })

    def __init__(self, device_id, config, checkpoint):
        super(LEGACY, self).__init__(device_id, config, checkpoint)
        self.server = None

    def starting(self):
        server_factory = LegacyServerFactory(self.config['username'], self.config['password'])
        self.server = self.tcp_server(self.config['listen_port'], server_factory)
        self.server.factory.on_open_gate = self.on_open_gate
        self.server.factory.on_auth_badge = self.on_auth_badge
        self.server.factory.on_auth_person = self.on_auth_person

    def is_ready(self):
        if not self.server:
            raise DeviceException('device not started')

        return self.server.factory.is_ready()

    def get_event_key(self, link_config):
        assert 'key' in link_config, 'no key configured in link'
        return link_config['key']

    def on_open_gate(self, lane_id):
        self.trigger_events(key=LEGACY.ACTION_KEY.OPEN_GATE, lane_id=lane_id)

    def on_auth_badge(self, lane_id, code, code_type):
        identifier = Badge(code, code_type)
        self.trigger_events(key=LEGACY.ACTION_KEY.AUTH_BADGE, lane_id=lane_id, identifier=identifier)

    def on_auth_person(self, lane_id, person, operator, documents, params):
        for item in self.get_attached_events(key=LEGACY.ACTION_KEY.AUTH_PERSON):

            if not lane_id or lane_id != item.lane.legacy_lane_id:
                self.log.debug('legacy_lane_id is not {lane}, skip this lane', lane=lane_id)
                continue

            self.log.info('authorizing person to lane {lane}', lane=lane_id)

            # attach transit item
            transit_item = Authorization(operator,
                                         params.get('destination'),
                                         params.get('reason'))
            for index, document in enumerate(documents):
                filename = document.get('filename', 'untitled_{0}'.format(index))
                attachment = Attachment(self.get_attachment_name(filename),
                                        document['content_type'],
                                        document['stream'].decode('base64'))

                transit_item.attachments.append(attachment)

            # not nice but needed
            item.lane.start_transit()

            item.lane.transit.add_item(transit_item)

            # set transit operator
            item.lane.transit.set_operator(operator)

            # add transit member
            member = TransitMember()
            member.owner = OwnerPerson(person.get('name'),
                                       person.get('birth_date'),
                                       person.get('birth_country'),
                                       photo_id=person.get('photo_id'))

            if person.get('company'):
                member.owner.company = Company(person['company']['name'],
                                               person['company']['type_name'])

            member.permission = Permission(PermissionType('OPERATOR', _('Authorized by operator')),
                                           datetime.now(),
                                           datetime.now(),
                                           owner=member.owner)

            member.set_auth(AuthStatus(AuthStatusId.ALLOWED, AuthCode.ALLOWED, _('Authorized by operator')))
            item.lane.transit.add_member(member)

            # trigger event
            item.event.trigger()

