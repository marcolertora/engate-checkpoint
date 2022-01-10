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
from twisted.logger import Logger
from datetime import datetime, timedelta
from automaton import Tasks
from commons.transit_items import Vehicle
from device import Device
from commons import AuthStatusId, AuthCode, AuthStatus
from commons.transits import TransitMember
import voluptuous as vol
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from commons.owners import Permission, PermissionType, OwnerPerson, Credential


@Tasks.register
def checkJtisRid(automaton, edge_config, **kwargs):
    assert 'identifier' in kwargs, 'identifier is required'
    transit_member = AuthenticatorJtisRID(automaton.parent, edge_config).get_transit_member(kwargs['identifier'])
    automaton.parent.transit.add_member(transit_member)
    return transit_member.auth_status.status_id


class JtisRID(Vehicle):

    def __init__(self, rid_number, plate=None, driver=None, timestamp=None):
        super(JtisRID, self).__init__(plate=plate)
        self.rid_number = rid_number
        self.driver = driver
        self.timestamp = timestamp

    @property
    def details(self):
        data = super(JtisRID, self).details
        data['rid_number'] = self.rid_number
        data['driver'] = self.driver
        data['timestamp'] = self.timestamp
        return data


class AuthenticatorJtisRID(object):

    CONFIG_SCHEMA = Device.CONFIG_SCHEMA.extend({
        vol.Required('private_key'): str,
        vol.Required('rid_valid_interval', default=24*60*60): vol.All(int,  vol.Range(min=0)),
    })

    log = Logger()

    def __init__(self, lane, config):
        config = AuthenticatorJtisRID.CONFIG_SCHEMA(config)
        self.lane = lane
        self.private_key = config['private_key']
        self.rid_valid_interval = timedelta(hours=config['rid_valid_interval'])

    def get_transit_member(self, identifier):
        member = TransitMember()
        self.log.info('checking identifier {identifier}...', identifier=identifier)

        try:
            item_rid = self.get_rid_owner(identifier.raw_code)
        except ValueError:
            self.log.info('no rid found for {identifier}...', identifier=identifier)
            return member

        transit_item = JtisRID(item_rid['ridCode'],
                               item_rid.get('plateCode'),
                               item_rid.get('driver'),
                               item_rid['ridDate'])

        self.lane.transit.add_item(transit_item)

        member.owner = OwnerPerson(item_rid.get('driver'),
                                   birth_date=None,
                                   birth_country=None)

        permission_type = PermissionType('JTIS_RID', 'JTIS RID Permission'),

        member.permission = Permission(permission_type,
                                       item_rid['ridDate'],
                                       item_rid['ridDate'] + self.rid_valid_interval,
                                       owner=member.owner)

        member.credential = Credential('JTIS_RID',
                                       item_rid['ridDate'],
                                       item_rid['ridDate'] + self.rid_valid_interval,
                                       item_rid['ridCode'],
                                       permission=member.permission)

        member.set_auth(self.validate_rid(member.owner, member.permission, member.credential))
        return member

    def get_rid_owner(self, identifier):
        item_rid = AuthenticatorJtisRID.parse(self.decrypt(identifier.raw_code))
        assert 'ridCode' in item_rid, 'rid code is required'
        assert 'ridDate' in item_rid, 'rid date is required'
        return item_rid

    def decrypt(self, data):
        if not data.startswith('ENC'):
            raise ValueError('invalid data')

        content_type, encryption_type, payload = data.split('@', 3)
        if encryption_type != 'RSASSAPKCS':
            raise ValueError('invalid encrypted type {0}'.format(encryption_type))

        cipher = PKCS1_v1_5.new(RSA.importKey(self.private_key))
        payload = cipher.decrypt(payload.decode('base64'), None)
        if not payload:
            raise ValueError('nothing decrypted')

        return payload

    @staticmethod
    def parse(message):
        values = dict()
        for item in message.split(';'):
            if item.strip():
                key, value = item.split('=', 1)
                if key == 'ridDate':
                    value = datetime.fromtimestamp(int(value))
                values[key] = value
        return values

    def validate_rid(self, owner, permission, credential):
        if not permission.valid_from or not permission.valid_to:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, 'invalid rid permission date')

        if datetime.now() < permission.valid_from:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, 'rid permission not yet valid')

        if datetime.now() > permission.valid_to:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DATE, 'rid permission in expired')

        if not credential.code:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DOCUMENT, 'invalid rid code')

        if not owner.name:
            return AuthStatus(AuthStatusId.REJECTED, AuthCode.INVALID_DRIVER, 'invalid driver name')

        return AuthStatus(AuthStatusId.ALLOWED, AuthCode.VALID, 'valid')
