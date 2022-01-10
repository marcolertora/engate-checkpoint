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

from collections import namedtuple
from device import Device
from exceptions import DeviceException

AttachedEvent = namedtuple('AttachedEvent', ['lane', 'priority', 'key', 'event'])


class InputDevice(Device):

    CONFIG_SCHEMA = Device.CONFIG_SCHEMA

    def __init__(self, device_id, config, checkpoint):
        super(InputDevice, self).__init__(device_id, config, checkpoint)
        self.attached_events = list()

    def attach_event(self, link_config, lane, priority, event):
        key = self.get_event_key(link_config)
        self.add_attached_events(lane, priority, key, event)

    def get_event_key(self, link_config):
        return None

    def add_attached_events(self, lane, priority, key, event):
        if self.single_lane:
            lanes = self.get_attached_lanes()
            lanes.add(lane)
            if len(lanes) > 1:
                raise DeviceException('{0} single lane device attached to multiple lane'.format(self))

        self.log.info('attach {device} to {lane} for {event} key {key}', device=self, lane=lane, event=event, key=key)
        self.attached_events.append(AttachedEvent(lane, priority, key, event))
        self.attached_events.sort(key=lambda x: x.priority)

    def get_attached_lanes(self):
        lanes = set()
        for item in self.attached_events:
            lanes.add(item.lane)
        return lanes

    def get_attached_events(self, key=None, lane_id=None, transit=None, keys=None):
        assert key is None or keys is None, 'key or keys cannot be used together'
        keys = [key] if key else keys
        for item in self.attached_events:
            if transit is not None and item.lane.transit.transit_id != transit.transit_id:
                continue
            if lane_id is not None and item.lane.lane_id != lane_id:
                continue
            if keys is not None and item.key not in keys:
                continue
            yield item

    def detach_events(self, lane):
        for item in self.get_attached_events(lane_id=lane.lane_id):
            self.attached_events.remove(item)
            self.log.info('detach from {lane} (left {count})'.format(lane=lane, count=len(self.attached_events)))
        else:
            self.log.warn('nothing to detach from {lane}'.format(lane=lane))

    def trigger_events(self, key=None, lane_id=None, transit=None, keys=None, **kwargs):
        trigger_count = 0
        for item in self.get_attached_events(key=key, lane_id=lane_id, transit=transit, keys=keys):
            trigger_count += 1
            item.event.trigger(**kwargs)

        if trigger_count == 0:
            self.log.warn('no event attached with key {key}', key=key)
