#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
#
# iMilestone
#
# Copyright (C) 2011 Marco Lertora <marco.lertora@infoporto.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# iree Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# ======================================================================

import struct
from datetime import datetime
from uuid import UUID

class DataView(object):

    class IncompletePacket(Exception):
        pass

    def __init__(self, value=str(), littleEndian=False):
        self.dataBuffer = value
        self.littleEndian = True
        self.posBuffer = 0
        super(DataView, self).__init__()

    def _readChunck(self, size):
        chunck = self.dataBuffer[self.posBuffer:self.posBuffer + size]
        if len(chunck) < size: raise DataView.IncompletePacket()
        self.posBuffer = self.posBuffer + size
        return chunck

    def _readAll(self):
        chunck = self.dataBuffer[self.posBuffer:]
        self.posBuffer = self.posBuffer + len(chunck)
        return chunck

    def _read(self, size=None):
        return self._readAll() if size is None else self._readChunck(size)

    def _write(self, data):
        self.dataBuffer = self.dataBuffer + data

    def _unpack(self, fmt):
        order = '<' if self.littleEndian else '>'
        fmt = order + fmt
        size = struct.calcsize(fmt)
        value, = struct.unpack(fmt, self._read(size))
        return value

    def _pack(self, fmt, value):
        order = '<' if self.littleEndian else '>'
        fmt = order + fmt
        self._write(struct.pack(fmt, value))

    def readString(self, size):
        return self._read(size)

    def readInteger(self):
        return self._unpack('i')

    def readUInteger(self):
        return self._unpack('I')

    def readShort(self):
        return self._unpack('h')

    def readUShort(self):
        return self._unpack('H')

    def readLong(self):
        return self._unpack('q')

    def readULong(self):
        return self._unpack('Q')

    def writeChar(self, value, repeat=1):
        for index in range(repeat): self._write(value)

    def writeString(self, value):
        self._write(value)

    def writeUInteger(self, value):
        self._pack('I', value)

    def writeUShort(self, value):
        self._pack('H', value)

    def readUUID(self):
        return UUID(bytes=self.readString(16))

    def readTimestamp(self):
        microsecond = self.readULong()
        return datetime.fromtimestamp(microsecond / 1000)

    def readAll(self):
        return self._read()

    def toData(self):
        return self.dataBuffer
