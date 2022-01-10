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
import base64
from datetime import datetime
from commons.owners import Photo, OwnerPerson, Zone
from commons.owners import Company, PermissionType, Permission
from commons.owners import Biometric, Credential


def map_company(values):
    assert isinstance(values, dict)
    return Company(values['name'],
                   values['type'],
                   vat=values['vat'],
                   disabled=values['disabled'])


def map_zone(values):
    assert isinstance(values, dict)
    zone = Zone()
    zone.add_gate(values['gate_id'], values.get('direction'))
    return zone


def map_credential(values, permission):
    assert isinstance(values, dict)
    return Credential(values['type']['id'] if values['type'] else None,
                      values['type']['code_type'] if values['type'] else None,
                      values['valid_from'],
                      values['valid_to'],
                      values['code'],
                      pin_code=values['pin_code'],
                      permission=permission,
                      disabled=values['disabled'])


def map_biometric(values, owner):
    assert isinstance(values, dict)
    return Biometric(values['id'],
                     values['type'],
                     values['template'],
                     values['threshold'],
                     values['bypass'],
                     owner=owner)


def map_permission_type(values):
    assert isinstance(values, dict)
    return PermissionType(values['id'],
                          values['description'],
                          valid_duration=values['valid_duration'],
                          time_to_live=values['time_to_live'],
                          tags=values['tags'])


def map_permission(values, owner):
    assert isinstance(values, dict)

    permission = Permission(map_permission_type(values['type']),
                            parse_date(values['valid_from']),
                            parse_date(values['valid_to']),
                            time_to_live=values['time_to_live'],
                            reference=values['reference'],
                            tags=values['tags'],
                            owner=owner,
                            disabled=values['disabled'])

    permission.credentials = map(lambda x: map_credential(x, permission), values['permission_credentials'])
    permission.zones = map(lambda x: map_zone(x), values['zones'])
    return permission


def parse_date(data):
    return datetime.strptime(data, '%Y-%m-%d') if data else None


def map_owner(values):
    if values.get('person'):
        owner = OwnerPerson(values['person']['full_name'],
                            parse_date(values['person']['birth_date']),
                            values['person']['birth_country'],
                            anonymous=values['person']['pseudonymised'],
                            photo_id=values['person']['photo']['id'],
                            company=map_company(values['company']) if values['company'] else None,
                            tags=values['tags'],
                            disabled=values['disabled'])

        owner.permissions = map(lambda x: map_permission(x, owner), values['permissions'])
        owner.add_biometrics(map(lambda x: map_biometric(x, owner), values.get('biometrics', list())))
        return owner

    raise NotImplementedError('only owner person are implemented')


def map_photo(values):
    return Photo(values['id'], base64.decodestring(values['image']))

