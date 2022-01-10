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
from helpers import class_repr, class_str


class Attachment(object):
    __slots__ = ['attachment_id', 'filename', 'content_type', 'stream']

    def __init__(self, filename, content_type, stream):
        self.attachment_id = uuid.uuid4().hex.upper()
        self.filename = filename
        self.content_type = content_type
        self.stream = stream

    def __repr__(self):
        return class_repr(self, self.attachment_id, filename=self.filename)

    def __str__(self):
        return class_str(self, self.attachment_id, self.filename)
