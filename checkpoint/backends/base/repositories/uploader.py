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

from twisted.internet.defer import inlineCallbacks
from repository import RepositoryBase


class UploaderRepository(RepositoryBase):

    @inlineCallbacks
    def insert_message(self, queue_id, message_class, message_data):
        raise NotImplementedError

    @inlineCallbacks
    def get_next_message(self):
        raise NotImplementedError

    @inlineCallbacks
    def count_message(self):
        raise NotImplementedError

    @inlineCallbacks
    def update_message_num_of_attempts(self, queue_id, num_of_attempts):
        raise NotImplementedError

    @inlineCallbacks
    def delete_message(self, queue_id):
        raise NotImplementedError
