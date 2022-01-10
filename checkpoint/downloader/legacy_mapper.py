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

from commons.owners import User, Photo, OwnerPerson
from commons.owners import Address, Company, PermissionType, Zone, Permission
from commons.owners import Biometric, Credential, PermissionTags
from device import BiometricType


def map_company(company_dict):
    if not company_dict.get('companyId'):
        return

    company = Company(company_dict['companyFullName'],
                      company_dict.get('companyTypeDescription'),
                      disabled=company_dict['companyStatusId'] != 'ENABLED')

    address = Address(street=company_dict.get('companyAddress'),
                      postal_code=company_dict.get('companyPostalcode'),
                      city=company_dict.get('companyCityName'),
                      province=company_dict.get('companyProvinceId'),
                      country=company_dict.get('companyCountryId'))

    company.add_address(address)
    return company


def map_zones(permission_dict):
    if permission_dict['permissionGates']:
        zone = Zone()
        for permission_gate in permission_dict['permissionGates']:
            zone.add_gate(permission_gate['gateId'], permission_gate['directionId'])
        yield zone


def map_permission_type(permission_dict):
    tags = list()
    if permission_dict.get('permissionTypeBiometricBypass'):
        tags.append(PermissionTags.biometric_bypass)
    if permission_dict.get('permissionTypeOperatorBypass'):
        tags.append(PermissionTags.operator_bypass)
    if permission_dict.get('permissionTypePinBypass'):
        tags.append(PermissionTags.pin_bypass)

    return PermissionType(permission_dict['permissionTypeId'],
                          permission_dict['permissionTypeDescription'],
                          valid_duration=None,
                          time_to_live=None,
                          tags=tags)


def map_credentials(permission_dict, permission):
    for credential_dict in permission_dict['badges'].values():
        yield Credential(credential_dict.get('badgeSupportId'),
                         credential_dict.get('badgeCodeTypeId'),
                         credential_dict.get('badgeStartDate'),
                         credential_dict.get('badgeEndDate'),
                         credential_dict.get('badgeBadgeNumberPlain'),
                         credential_dict.get('badgePinNumberPlain'),
                         permission=permission)


def map_biometrics(item_dict, owner):
    for biometric_dict in item_dict['peopleBiometrics'].values():
        if 'biometricTemplate' in biometric_dict:
            # map biometric type
            if biometric_dict['biometricTypeId'] == 'LEFTHAND':
                biometric_dict['biometricTypeId'] = BiometricType.LEFT_HAND

            yield Biometric(biometric_dict['biometricId'],
                            biometric_dict['biometricTypeId'],
                            biometric_dict['biometricTemplate'],
                            biometric_dict['biometricThreshold'],
                            biometric_dict['biometricBypass'],
                            owner=owner)


def map_permissions(item_dict, owner):
    for permission_dict in item_dict['peoplePermissions'].values():

        tags = list()
        if permission_dict.get('permissionBiometricBypass'):
            tags.append(PermissionTags.biometric_bypass)
        if permission_dict.get('permissionOperatorBypass'):
            tags.append(PermissionTags.operator_bypass)
        if permission_dict.get('permissionPinBypass'):
            tags.append(PermissionTags.pin_bypass)
        if permission_dict.get('permissionZoneAccessTypeBypass'):
            tags.append(PermissionTags.zone_bypass)

        permission = Permission(map_permission_type(permission_dict),
                                permission_dict.get('permissionStartDate'),
                                permission_dict.get('permissionEndDate'),
                                time_to_live=None,
                                tags=tags,
                                owner=owner,
                                disabled=permission_dict['permissionStatusId'] != 'VALID')

        permission.credentials = list(map_credentials(permission_dict, permission))
        permission.zones = list(map_zones(permission_dict))
        yield permission


def map_owner_person(item_dict):
    owner = OwnerPerson(item_dict['peopleFullName'],
                        item_dict.get('peopleBirthdayDate'),
                        item_dict.get('peopleBirthdayCountryId'),
                        # TODO: it should be: photo_id=item_dict.get('peoplePhotoId'). it has been temporary set None
                        #       to avoid photo_id mismatch
                        photo_id=None,
                        company=map_company(item_dict['peopleCompany']),
                        tags=None)

    owner.permissions = list(map_permissions(item_dict, owner))
    owner.add_biometrics(map_biometrics(item_dict, owner))
    return owner


def map_owner(item_dict):
    if item_dict['objectOwnerType'] == 'PEOPLE':
        return map_owner_person(item_dict)

    raise NotImplementedError('unknown object_type {0}'.format(item_dict['objectOwnerType']))


def map_user(item_dict):
    return User(item_dict['userUserName'],
                item_dict['userPassword'],
                item_dict['userCapabilities'],
                item_dict['userFirstName'],
                item_dict['userLastName'],
                item_dict['userIsActive'])


def map_photo(item_dict):
    return Photo(item_dict['photoId'],
                 item_dict['photoStream'],
                 content_type=item_dict['contentType'])
