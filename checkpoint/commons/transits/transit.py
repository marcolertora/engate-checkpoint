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
import uuid
from copy import deepcopy
from datetime import datetime
from collections import OrderedDict
from twisted.logger import Logger
from helpers import class_str, class_repr, AutoUploadMixin
from commons.transit_items import Vehicle


class Transit(AutoUploadMixin):
    __slots__ = ['transit_id', 'lane', 'members', 'last_added_member', 'items', 'status', 'operator', 'end_date',
                 'start_date', 'direction']

    log = Logger()

    def __init__(self, lane, uploader=None):
        super(Transit, self).__init__(uploader)
        self.transit_id = uuid.uuid4().hex.upper()
        self.lane = lane
        self.log.info('initializing...')
        self.members = dict()
        self.last_added_member = None
        self.items = OrderedDict()
        self.status = None
        self.operator = None
        self.end_date = None
        self.start_date = None
        self.direction = None

    @property
    def transit_short_id(self):
        return self.transit_id.encode('base64').strip()

    @property
    def current_member(self):
        # last inserted is the current one
        return self.last_added_member

    @property
    def vehicles(self):
        return filter(lambda x: isinstance(x, Vehicle), self.items.values())

    def skip_upload(self):
        if self.lane.discard_transit:
            self.log.warn('lane {lane} has discard transit flag, discarding', lane=self.lane)
            return True

        if not self.start_date:
            self.log.warn('missing start_date, discarding')
            return True

        return False

    def __repr__(self):
        return class_repr(self, self.transit_id)

    def __str__(self):
        return class_str(self, self.transit_id)

    def add_member(self, member):
        self.log.info('adding {member}...', member=member)
        if member.key in self.members:
            self.log.warn('member {member} already exists, skip', member=member)
            return

        self.members[member.key] = member
        self.last_added_member = member
        self.lane.for_any_console(lambda c: c.add_transit_member(self, member))

    def reset_members(self):
        self.log.info('resetting members...')
        self.last_added_member = None
        self.members.clear()
        self.lane.for_any_console(lambda c: c.reset_transit_members(self))

    def add_item(self, transit_item):
        self.log.info('adding {item}...', item=transit_item)
        if transit_item.item_id in self.items:
            self.log.warn('item {item} already exists, skip', item=transit_item)
            return

        for attachment in transit_item.attachments:
            self.lane.checkpoint.add_attachment(attachment)

        self.items[transit_item.item_id] = transit_item
        self.lane.for_any_console(lambda c: c.add_transit_item(self, transit_item))

    def set_status(self, status):
        self.log.info('setting status {status}...', status=status)
        if not self.status or self.status.status_id != status.status_id:
            self.status = deepcopy(status)
            self.lane.for_any_console(lambda c: c.set_transit_status(self, status))

    def set_direction(self, direction):
        self.log.info('setting {direction}', direction=direction)
        if self.direction != direction:
            self.direction = direction
            self.lane.for_any_console(lambda c: c.set_transit_direction(self, direction))

    def set_start_date(self):
        self.start_date = datetime.now()

    def set_end_date(self):
        self.end_date = datetime.now()

    def set_date(self, timestamp):
        self.start_date = timestamp
        self.end_date = timestamp

    def set_operator(self, operator):
        self.operator = operator

