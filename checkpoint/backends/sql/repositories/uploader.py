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
from twisted.internet.defer import inlineCallbacks, returnValue

from backends.base import ItemNotFound
from backends.base.repositories import UploaderRepository
from backends.sql.repositories.sql_message import SQLMessage
from repository import SQLRepository

QueueMessage = namedtuple('QueueMessage', ['queue_id', 'message_class', 'num_of_attempts', 'data'])


class UploaderSQLRepository(UploaderRepository, SQLRepository):

    repository_filename = 'database_uploader'

    @inlineCallbacks
    def initialize(self):
        self.log.debug('initialize database...')
        yield self.run_interaction(SQLMessage.create)

    @inlineCallbacks
    def insert_message(self, queue_id, message_class, message_data):
        self.log.debug('insert message {queue_id}...', queue_id=queue_id)
        message = SQLMessage(queue_id, message_class, self.dump_item(message_data))
        yield self.run_interaction(SQLMessage.insert, message)

    @inlineCallbacks
    def get_next_message(self):
        self.log.debug('retrieving next message...')
        item = yield self.run_interaction(SQLMessage.get_next)
        if not item:
            raise ItemNotFound('no item found!')

        returnValue(QueueMessage(item.queue_id,
                                 item.message_class,
                                 item.num_of_attempts,
                                 self.load_item(item.data)))

    @inlineCallbacks
    def count_message(self):
        count = yield self.run_interaction(SQLMessage.count)
        returnValue(count)

    @inlineCallbacks
    def update_message_num_of_attempts(self, queue_id, num_of_attempts):
        yield self.run_interaction(SQLMessage.update_num_of_attempts, queue_id, num_of_attempts)

    @inlineCallbacks
    def delete_message(self, queue_id):
        self.log.debug('deleting {message}...', message=queue_id)
        yield self.run_interaction(SQLMessage.delete, queue_id)
        yield self.run_interaction(self.vacuum)
