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

from device import DeviceException
from apromix import APROMIX
from device.protocols import ProtocolSerial


class FKLIGHTProto(ProtocolSerial):
    """
        SetSetup --> REPLY
        SetOutput --> REPLY
        Request --> NO_BADGE
        Request --> BADGE --> Acknowledgment
    """

    def __init__(self, units, polling_interval):
        ProtocolSerial.__init__(self, polling_interval)
        self.message_factory = APROMIX.parsePackets
        self.units = units
        self.current_unit = 0

    def connectionMade(self):
        ProtocolSerial.connectionMade(self)
        for unit in self.units:
            self.add_message(APROMIX.SetSetup(unit, tmac=4))
        self.next_message()
        self.watchdog()

    def move_to_next_unit(self):
        return (self.current_unit + 1) % len(self.units)

    def get_next_polling_message(self):
        message = APROMIX.Request(self.units[self.current_unit], APROMIX.REQUEST.READ)
        self.current_unit = self.move_to_next_unit()
        return message

    def handle_messages(self, messages):
        self.set_last_seen()

        for reply, unit, message in messages:
            if unit not in self.units:
                self.factory.device_log.warn('ignoring message, not for me')
                return

            # response of APROMIX.Request(READ) with badge
            if reply == APROMIX.REPLY.BADGE:
                self.factory.device_log.debug('unit {unit} reply badge read {badge}',
                                              unit=unit,
                                              badge=message)
                self.factory.on_badges_received(unit, message)
                # send ack and call next_message to consume no replay message
                self.add_message(APROMIX.Acknowledgment(unit))
                self.next_message()
                self.add_message(APROMIX.SetOutput(unit, buzzer=10))

            # response of APROMIX.Request(READ) without badge
            elif reply == APROMIX.REPLY.NO_BADGE:
                self.factory.device_log.debug('unit {unit} reply no badge read',
                                              unit=unit)

            # response of SetSetup, SetOutput
            elif reply == APROMIX.REPLY.EXIT:
                self.factory.device_log.debug('unit {unit} reply exit: {message}',
                                              message=APROMIX.EXIT.to_str(message),
                                              unit=unit)
                if message != APROMIX.EXIT.OK:
                    self.transport.loseConnection()
                    return

            else:
                raise DeviceException('unknown replay: {0}'.format(reply))

            self.next_message()

    def pulse(self, unit, duration):
        assert unit in self.units, 'invalid unit'
        self.add_message(APROMIX.SetOutput(unit, relay=duration * 10.0, led=duration * 10.0))
