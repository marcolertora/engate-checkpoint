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
from datalogic import DATALOGIC
from device.protocols import ProtocolSerial


class GFS4400Proto(ProtocolSerial):

    def __init__(self, polling_interval, is_mirror, has_ack):
        ProtocolSerial.__init__(self, polling_interval)
        self.is_mirror = is_mirror
        self.has_ack = has_ack
        self.baud_rate = 115200
        self.message_factory = DATALOGIC.parsePackets

    def get_setup_sequence(self):
        enter_setup = [DATALOGIC.EnterSetupMode(),
                       DATALOGIC.SetSerial(),
                       DATALOGIC.SetBaudRate(self.baud_rate)]

        exit_setup = [DATALOGIC.ExitAndSaveSetupMode()]

        commands = [DATALOGIC.SetTransmitAIMID(True),
                    DATALOGIC.SetTransmitLabelID('PREFIX'),
                    DATALOGIC.SetGlobalPrefix(DATALOGIC.CODE.SOP + DATALOGIC.CODE.BARCODE),
                    DATALOGIC.SetGlobalSuffix(DATALOGIC.CODE.EOP)]

        if self.is_mirror:
            commands.append(DATALOGIC.SetMirrorMode(True))

        return enter_setup + commands + exit_setup

    def connectionMade(self):
        ProtocolSerial.connectionMade(self)
        if self.has_ack:
            self.factory.device_log.debug('has ack starting watchdog..')
            for message in self.get_setup_sequence():
                self.factory.device_log.debug(message)
                self.add_message(message)
            self.next_message()
            self.watchdog()

    def get_next_polling_message(self):
        return DATALOGIC.ReadSoftwareRelease()

    def handle_messages(self, messages):
        self.set_last_seen()

        for operation, value in messages:
            self.factory.device_log.debug('operation: {operation} value: {value}', operation=operation, value=value)

            if operation == DATALOGIC.RESULT.BARCODE:
                self.factory.on_read_barcode(value)
                continue

            if operation == DATALOGIC.RESULT.VERSION:
                self.next_message()
                continue

            if operation == DATALOGIC.RESULT.OK:
                self.next_message()
                continue

            if operation == DATALOGIC.RESULT.ERROR:
                self.factory.device_log.warn('error received from host')
                self.next_message()
                continue

            raise DeviceException('unknown operation: {0}'.format(operation))
