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
#
from commons import Command, LaneLog, DeviceLog
from commons.owners import OwnerPerson
from commons.owners.owner import OwnerVehicle
from commons.transits import Transit
from helpers import class_name


def map_command(item):
    return dict(id=item.command_id,
                action=item.action,
                timestamp=item.timestamp,
                params=item.params,
                )


def map_lane_log(lane_log):
    return dict(id=lane_log.lane_log_id,
                lane_id=lane_log.lane_id,
                timestamp=lane_log.timestamp,
                level=lane_log.level,
                code=lane_log.code,
                message=lane_log.message,
                )


def map_device_log(device_log):
    return dict(id=device_log.device_log_id,
                device_id=device_log.device_id,
                timestamp=device_log.timestamp,
                level=device_log.level,
                code=device_log.code,
                message=device_log.message,
                )


def map_company(company):
    data = dict(name=company.name,
                company_type=company.company_type)

    if company.default_address and company.default_address.city:
        data.update(city=company.default_address.city)

    return data


def map_owner(owner):
    data = dict(name=owner.name,
                owner_type=class_name(owner))

    if owner.company:
        data.update(company=map_company(owner.company))

    if isinstance(owner, OwnerPerson):
        if owner.birth_country:
            data.update(birthday_country=owner.birth_country)
        if owner.birth_date:
            data.update(birthday_date=owner.birth_date.isoformat())

    if isinstance(owner, OwnerVehicle):
        if owner.plate:
            data.update(plate=owner.plate)

    return data


def map_transit_member(transit_member):
    data = dict(owner=map_owner(transit_member.owner),
                status=transit_member.auth_status.status_id,
                status_message=transit_member.auth_status.message)

    if transit_member.permission:
        data.update(permission_type=transit_member.permission.permission_type.name,
                    permission_reference=transit_member.permission.reference)

    if transit_member.credential:
        data.update(credential_type=transit_member.credential.credential_type,
                    credential_code_type=transit_member.credential.code_type)

    return data


def map_attachment(attachment):
    return dict(id=attachment.attachment_id,
                filename=attachment.filename,
                content_type=attachment.content_type,
                stream=attachment.stream.encode('base64')
                )


def map_transit_item(transit_item):
    return dict(id=transit_item.item_id,
                item_type=class_name(transit_item),
                attachments=map(map_attachment, transit_item.attachments),
                details=transit_item.details
                )


def map_transit(transit):
    data = dict(id=transit.transit_id,
                granted=transit.status.granted if transit.status else None,
                status=transit.status.name if transit.status else None,
                direction=transit.direction if transit.direction else transit.lane.direction,
                start_date=transit.start_date.isoformat(),
                end_date=transit.end_date.isoformat(),
                site=transit.lane.gate.site.name,
                gate=transit.lane.gate.name,
                lane=transit.lane.name,
                lane_status=transit.lane.lane_status.name,
                lane_type=transit.lane.lane_type.name,
                security_level=transit.lane.security_level.name,
                operator=transit.operator,
                members=map(map_transit_member, transit.members.values()),
                items=map(map_transit_item, transit.items.values()),
                )

    return data


def map_message(item):
    if isinstance(item, Command):
        return map_command(item)

    if isinstance(item, LaneLog):
        return map_lane_log(item)

    if isinstance(item, DeviceLog):
        return map_device_log(item)

    if isinstance(item, Transit):
        return map_transit(item)

    raise NotImplementedError('unknown message class {0}'.format(item))
