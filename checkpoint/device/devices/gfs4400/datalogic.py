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


from commons.identifiers import Barcode
from device.protocols.exceptions import IncompletePacket, InvalidPacket


class DATALOGIC(object):

    class TYPES:
        barcode_types = {'V': 'CODE-39',
                         '*': 'CODE-39',
                         'T': 'CODE-128',
                         '#': 'CODE-128',
                         'B': 'EAN-13',
                         'F': 'EAN-13',
                         'A': 'EAN-8',
                         'FF': 'EAN-8',
                         'k': 'EAN-128',
                         'x': 'MAXICODE',
                         'MC': 'MAXICODE',
                         'r': 'PDF147',
                         'P': 'PDF147',
                         'y': 'QRCODE',
                         'QR': 'QRCODE',
                         '$Q': 'MICROQR',
                         'w': 'DATAMATRIX',
                         'Dm': 'DATAMATRIX',
                         'C': 'UPCA',
                         # 'A': 'UPCA',
                         'D': 'UPCE',
                         'E': 'UPCS',
                         '!': 'AZTEC',
                         'Az': 'AZTEC',
                         '8': 'MICROPDF',
                         'mP': 'MICROODF',
                         't': 'DATABAREX',
                         'Rx': 'DATABAREX',
                         '$S': 'CHINASENSIBLE',
                         'O': 'FOLLET2OF5',
                         'W': 'INDUSTRIAL2OF5',
                         }

        @staticmethod
        def get(barcode_type):
            assert barcode_type in DATALOGIC.TYPES.barcode_types, 'missing barcode type: {0}'.format(barcode_type)
            return DATALOGIC.TYPES.barcode_types.get(barcode_type)

    class CONFIG:
        TRANSMITAIMID = 'AIEN'
        TRANSMITLABELID = 'IDCO'
        GLOBALPREFIX = 'LFPR'
        GLOBALSUFFIX = 'LFSU'
        BAUDRATE = 'R2BA'
        MIRRORMODE = 'MREN'
        OPERATINGMODE = 'SNRM'
        NOREADMESSAGE = 'NRSS'
        NOREADSTRING = 'NORS'
        PHASEOFFEVENT = 'SPTO'
        PHASEOFFTIMEOUT = 'SNET'
        SERIALSTART = 'STON'
        SERIALSTOP = 'STOF'
        MANUALTRIGGER = 'SOTM'

    class CODE:
        SOP = '\x24'
        EOP = '\x0D'
        OK = '\x3E'
        ERROR = '\x25'
        BARCODE = '\x26'
        BLANK = '\x00'
        SEP = '\x5D'
        NOBARCODE = '\x18'

    class RESULT:
        OK = 'OK'
        ERROR = 'ERROR'
        VERSION = 'VERSION'
        BARCODE = 'BARCODE'
        NOBARCODE = 'NOBARCODE'

    class COMMAND:
        SETSERIAL = 'HA05'
        RESET = 'R'
        ENTERSETUPMODE = 'S'
        EXITSAVESETUPMODE = 'Ar'
        SOFTWARERELEASE = '+$!'
        READCONFIG = 'c'
        WRITECONFIG = 'C'
        ENABLEALLSYMBOL = 'AA'
        DISABLEALLSYMBOL = 'AD'
        FACTORYRESTOREEU = 'Ae'
        FACTORYRESTOREUS = 'AE'
        TRIGGER = '\x02'

    @staticmethod
    def parsePackets(data):
        packets = data.split(DATALOGIC.CODE.EOP)

        if packets.pop():
            raise IncompletePacket('last byte should be: {0}, may be incomplete'.format(DATALOGIC.CODE.EOP))

        return map(lambda packet: DATALOGIC.parsePacket(packet + DATALOGIC.CODE.EOP), packets)

    @staticmethod
    def parsePacket(data):
        if len(data) < 3:
            raise IncompletePacket('too short, must be at least three bytes')

        if not data.endswith(DATALOGIC.CODE.EOP):
            raise IncompletePacket('last byte should be: {0}, may be incomplete'.format(DATALOGIC.CODE.EOP))

        data = data[:-1]

        if data.startswith(DATALOGIC.CODE.SOP):

            if data[1] == DATALOGIC.CODE.OK:
                return DATALOGIC.RESULT.OK, data[2:]

            if data[1] == DATALOGIC.CODE.ERROR:
                return DATALOGIC.RESULT.ERROR, data[2:]

            if data[1] == DATALOGIC.CODE.BARCODE:

                if data[2] == DATALOGIC.CODE.NOBARCODE:
                    return DATALOGIC.RESULT.NOBARCODE, None

                assert DATALOGIC.CODE.SEP in data[1:], 'missing aim separator: {0}'.format(DATALOGIC.CODE.SEP)
                sep = data.find(DATALOGIC.CODE.SEP)
                b_type, b_code = data[2:sep], data[sep + 3:]
                b_aim_id, b_modifier = data[sep + 1:sep + 2], data[sep + 2:sep + 3]

                return DATALOGIC.RESULT.BARCODE, Barcode(b_code, DATALOGIC.TYPES.get(b_type))

        if data.startswith('Gryphon'):
            return DATALOGIC.RESULT.VERSION, data

        raise InvalidPacket('unknown packet: {0}'.format(data))

    @staticmethod
    def buildCommand(command, key=None, value=None):
        assert not (value and not key), 'configuration value require configuration key'
        payload = command
        if key:
            payload = command + key
        if key and value:
            payload = command + key + value
        return DATALOGIC.CODE.SOP + payload + DATALOGIC.CODE.EOP

    @staticmethod
    def ReadSoftwareRelease():
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.SOFTWARERELEASE)

    @staticmethod
    def EnterSetupMode():
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.ENTERSETUPMODE)

    @staticmethod
    def ExitAndSaveSetupMode():
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.EXITSAVESETUPMODE)

    @staticmethod
    def ResetReader():
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.RESET)

    @staticmethod
    def ReadSingleConfigurationItem(key):
        assert len(key) == 4, 'invalid configuration key, should be == 4'
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.READCONFIG, key)

    @staticmethod
    def WriteSingleConfigurationItem(key, value):
        assert len(key) == 4, 'invalid configuration key, should be == 4'
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.WRITECONFIG, key, value)

    @staticmethod
    def SetTransmitAIMID(value):
        value = '01' if value else '00'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.TRANSMITAIMID, value)

    @staticmethod
    def SetTransmitLabelID(value='PREFIX'):
        values = ['DISABLE', 'PREFIX', 'SUFFIX']
        assert value in values, 'invalid value, should be in {0}'.format(values)
        value = '%02d' % (values.index(value))
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.TRANSMITLABELID, value)

    @staticmethod
    def SetGlobalPrefix(value):
        value = value.ljust(20, DATALOGIC.CODE.BLANK).encode('hex')
        assert len(value) <= 40, 'invalid prefix, should be <= 40'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.GLOBALPREFIX, value)

    @staticmethod
    def SetGlobalSuffix(value):
        value = value.ljust(20, DATALOGIC.CODE.BLANK).encode('hex')
        assert len(value) <= 40, 'invalid suffix, should be <= 40'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.GLOBALSUFFIX, value)

    @staticmethod
    def SetMirrorMode(value):
        value = '01' if value else '00'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.MIRRORMODE, value)

    @staticmethod
    def RestoreFactory(value='EU'):
        assert value in ('EU', 'US'), 'invalid country code'
        command = DATALOGIC.COMMAND.FACTORYRESTOREUS if value == 'US' else DATALOGIC.COMMAND.FACTORYRESTOREEU
        return DATALOGIC.buildCommand(command)

    @staticmethod
    def SetEnableAllSymbol(value):
        command = DATALOGIC.COMMAND.ENABLEALLSYMBOL if value else DATALOGIC.COMMAND.DISABLEALLSYMBOL
        return DATALOGIC.buildCommand(command)

    @staticmethod
    def SetNoReadMessage(value):
        value = '01' if value else '00'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.NOREADMESSAGE, value)

    @staticmethod
    def SetNoReadString(value):
        value = value.ljust(20, DATALOGIC.CODE.BLANK).encode('hex')
        assert len(value) <= 40, 'invalid suffix, should be <= 40'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.NOREADSTRING, value)

    @staticmethod
    def SetSerial():
        return DATALOGIC.buildCommand(DATALOGIC.COMMAND.SETSERIAL)

    @staticmethod
    def SetBaudRate(value):
        values = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        assert value in values, 'invalid baudrate, should be in {0}'.format(values)
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.BAUDRATE, '%02d' % values.index(value))

    @staticmethod
    def SetOperationMode(value):
        values = ['ONLINE', 'SERIALONLINE', 'AUTOMATIC', 'AUTOMATICOBJECTSENSE']
        assert value in values, 'invalid operation mode, should be in {0}'.format(values)
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.OPERATINGMODE, '%02d' % values.index(value))

    @staticmethod
    def SetPhaseOffEvent(value):
        values = ['TRIGGERSTOP', 'TIMEOUT', 'TRIGGERSTOPTIMEOUT']
        assert value in values, 'invalid value, should be in {0}'.format(values)
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.PHASEOFFEVENT, '%02d' % values.index(value))

    @staticmethod
    def SetPhaseOffTimeout(value):
        assert 0 < value <= 255, 'invalid timeout, should be >= 1 and <= 255'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.PHASEOFFTIMEOUT, '%02X' % value)

    @staticmethod
    def SetManualTrigger(value):
        value = '01' if value else '00'
        return DATALOGIC.WriteSingleConfigurationItem(DATALOGIC.CONFIG.MANUALTRIGGER, value)

    @staticmethod
    def Trigger():
        return DATALOGIC.COMMAND.TRIGGER
