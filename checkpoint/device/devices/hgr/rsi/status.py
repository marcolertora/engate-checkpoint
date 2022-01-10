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

from types import BooleanType
from pprint import pformat


class Status(object):
    smask0 = ['H_READ', 'LED1', 'LED2', 'LED3', 'LED4', 'ANY_KEY', 'AUX_OUT1', 'AUX_OUT2']
    smask1 = ['RES_SYS', 'VERIFY_RDY', 'RSLTS_RDY', 'FAILED_CMD', 'DLOG_RDY', 'ID_NIM', 'CMD_BUSY', 'KP_ID']
    mmask = ['TAMPER', 'AUX_IN_1', 'DOOR_SW', 'AUX_IN_0', 'REX', 'NotUsed', 'AUX_OUT_0', 'LOCK']
    masks = smask0 + smask1 + mmask

    __slots__ = ['__map', '__status', '__sysmap', '__systat0', '__systat1', '__monstat']

    def __init__(self, status='\x00\x00\x00'):
        assert len(status) == 3, 'Status must be 3 bytes long'
        self.__status = status

        systat0_b = ord(status[0])
        systat1_b = ord(status[1])
        monstat_b = ord(status[2])

        self.__systat0 = map(lambda x: bool(systat0_b & pow(2, x)), range(8))
        self.__systat1 = map(lambda x: bool(systat1_b & pow(2, x)), range(8))
        self.__monstat = map(lambda x: bool(monstat_b & pow(2, x)), range(8))

        self.__sysmap = {}
        self.__updatemap()

        self.__map = zip((Status.smask0, Status.smask1, Status.mmask), (self.__systat0, self.__systat1, self.__monstat))

    def __updatemap(self):
        self.__sysmap['systat0'] = {}
        map(lambda x: self.__sysmap['systat0'].update({Status.smask0[x]: self.__systat0[x]}), range(8))
        systat0_b = reduce(lambda value, bit: value | ((self.__systat0[bit] and 1 or 0) << bit), range(8), 0)

        self.__sysmap['systat1'] = {}
        map(lambda x: self.__sysmap['systat1'].update({Status.smask1[x]: self.__systat1[x]}), range(8))
        systat1_b = reduce(lambda value, bit: value | ((self.__systat1[bit] and 1 or 0) << bit), range(8), 0)

        self.__sysmap['monstat'] = {}
        map(lambda x: self.__sysmap['monstat'].update({Status.mmask[x]: self.__monstat[x]}), range(8))
        monstat_b = reduce(lambda value, bit: value | ((self.__monstat[bit] and 1 or 0) << bit), range(8), 0)

        self.__status = ''.join(map(chr, (systat0_b, systat1_b, monstat_b)))

    def getStatus(self, attr):
        for mask, status in self.__map:
            try:
                return status[mask.index(attr)]
            except ValueError:
                pass
        assert False

    def setStatus(self, attr, value):
        if not isinstance(value, bool):
            raise TypeError('Need a boolean')

        for mask, status in self.__map:
            try:
                index = mask.index(attr)
                assert index != -1
                status[index] = value
                self.__updatemap()
                break
            except ValueError:
                pass

    def __getattribute__(self, attr):
        if attr in Status.masks:
            return self.getStatus(attr)
        return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        if attr in Status.masks:
            return self.setStatus(attr, value)
        return object.__setattr__(self, attr, value)

    def serialize(self):
        return self.__status

    def __repr__(self):
        return pformat(self.__sysmap)
